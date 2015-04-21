from datetime import datetime, date

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import six
from django.core.files.base import File
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from options.models import Option, OptionValue
from fs.core.loading import get_model
from fs.models.fields import AutoSlugField

class Group(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True)
    icon = models.ImageField(upload_to='self._meta.app_label' + '/icon/', blank=True)
    option = models.ManyToManyField(Option)
    enable = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class ItemOptionContainer(object):
    """
    Stolen liberally from django-eav, but simplified to be item-specific

    To set options on a item, use the `attr` option:

        item.attr.weight = 125
    """

    def __setstate__(self, state):
        self.__dict__ = state
        self.initialised = False

    def __init__(self, item):
        self.item = item
        self.initialised = False

    def __getattr__(self, name):
        if not name.startswith('_') and not self.initialised:
            values = self.get_values().select_related('option')
            for v in values:
                setattr(self, v.option.code, v.value)
            self.initialised = True
            return getattr(self, name)
        raise AttributeError(
            _("%(obj)s has no option named '%(attr)s'") % {
                'obj': self.item.get_item_class(), 'attr': name})

    def validate_options(self):
        for option in self.get_all_options():
            value = getattr(self, option.code, None)
            if value is None:
                if option.required:
                    raise ValidationError(
                        _("%(attr)s option cannot be blank") %
                        {'attr': option.code})
            else:
                try:
                    option.validate_value(value)
                except ValidationError as e:
                    raise ValidationError(
                        _("%(attr)s option %(err)s") %
                        {'attr': option.code, 'err': e})

    def get_values(self):
        return self.item.option_values.all()

    def get_value_by_option(self, option):
        return self.get_values().get(option=option)

    def get_all_options(self):
        return self.item.get_item_class().options.all()

    def get_option_by_code(self, code):
        return self.get_all_options().get(code=code)

    def __iter__(self):
        return iter(self.get_values())

    def save(self):
        for option in self.get_all_options():
            if hasattr(self, option.code):
                value = getattr(self, option.code)
                option.save_value(self.item, value)

class Item(models.Model):
    title = models.CharField(_('Title'), max_length=100)
    origin_title = models.CharField(max_length=100)
    slug = models.SlugField(_('Slug'), max_length=255, unique=False)
    main_image = models.ImageField(upload_to='/item/main_image/%Y/%m/%d/')
    trailer_link = models.URLField(blank=True)
    trailer_image = models.ImageField(upload_to='/item/trailer_image/', blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    enable = models.BooleanField(default=True)
    description = models.TextField()
    group = models.ForeignKey(Group)
    images = ArrayField(models.ImageField(upload_to='/item/images/%Y/%m/%d/'), blank=True)
    tags = ArrayField(models.CharField(max_length=100), blank=True)
    option_value = models.ManyToManyField(OptionValue)
    related_items = models.ManyToManyField('self', blank=True)
    item_class = models.ForeignKey(
        'materials.ItemClass', null=True, on_delete=models.PROTECT,
        verbose_name=_('Item type'), related_name="items",
        help_text=_("Choose what type of item this is"))
    options = models.ManyToManyField(
        'materials.ItemOption',
        through='ItemOptionValue',
        verbose_name=_("Options"),
        help_text=_("A item option is something that this item may "
                    "have, such as a size, as specified by its class"))

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.attr = ItemOptionContainer(item=self)

    def __unicode__(self):
        if self.title:
            return self.title
        if self.option_summary:
            return u"%s (%s)" % (self.get_title(), self.option_summary)
        else:
            return self.get_title()

    def get_absolute_url(self):
        """
        Return a item's absolute url
        """
        return reverse('catalogue:detail',
                       kwargs={'item_slug': self.slug, 'pk': self.id})

    def clean(self):
        """
        Validate a item. Those are the rules:

        +---------------+-------------+--------------+--------------+
        |               | stand alone | parent       | child        |
        +---------------+-------------+--------------+--------------+
        | title         | required    | required     | optional     |
        +---------------+-------------+--------------+--------------+
        | item class | required    | required     | must be None |
        +---------------+-------------+--------------+--------------+
        | parent        | forbidden   | forbidden    | required     |
        +---------------+-------------+--------------+--------------+
        | stockrecords  | 0 or more   | forbidden    | 0 or more    |
        +---------------+-------------+--------------+--------------+
        | categories    | 1 or more   | 1 or more    | forbidden    |
        +---------------+-------------+--------------+--------------+
        | options    | optional    | optional     | optional     |
        +---------------+-------------+--------------+--------------+
        | rec. items | optional    | optional     | unsupported  |
        +---------------+-------------+--------------+--------------+
        | options       | optional    | optional     | forbidden    |
        +---------------+-------------+--------------+--------------+

        Because the validation logic is quite complex, validation is delegated
        to the sub method appropriate for the item's structure.
        """
        getattr(self, '_clean_%s' % self.structure)()
        if not self.is_parent:
            self.attr.validate_options()

    def _clean_standalone(self):
        """
        Validates a stand-alone item
        """
        if not self.title:
            raise ValidationError(_("Your item must have a title."))
        if not self.item_class:
            raise ValidationError(_("Your item must have a item class."))
        if self.parent_id:
            raise ValidationError(_("Only child items can have a parent."))

    def _clean_child(self):
        """
        Validates a child item
        """
        if not self.parent_id:
            raise ValidationError(_("A child item needs a parent."))
        if self.parent_id and not self.parent.is_parent:
            raise ValidationError(
                _("You can only assign child items to parent items."))
        if self.item_class:
            raise ValidationError(
                _("A child item can't have a item class."))
        if self.pk and self.categories.exists():
            raise ValidationError(
                _("A child item can't have a category assigned."))
        # Note that we only forbid options on item level
        if self.pk and self.item_options.exists():
            raise ValidationError(
                _("A child item can't have options."))

    def _clean_parent(self):
        """
        Validates a parent item.
        """
        self._clean_standalone()
        if self.has_stockrecords:
            raise ValidationError(
                _("A parent item can't have stockrecords."))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_title())
        super(AbstractProduct, self).save(*args, **kwargs)
        self.attr.save()

    # Properties

    @property
    def is_standalone(self):
        return self.structure == self.STANDALONE

    @property
    def is_parent(self):
        return self.structure == self.PARENT

    @property
    def is_child(self):
        return self.structure == self.CHILD

    def can_be_parent(self, give_reason=False):
        """
        Helps decide if a the item can be turned into a parent item.
        """
        reason = None
        if self.is_child:
            reason = _('The specified parent item is a child item.')
        if self.has_stockrecords:
            reason = _(
                "One can't add a child item to a item with stock"
                " records.")
        is_valid = reason is None
        if give_reason:
            return is_valid, reason
        else:
            return is_valid

    @property
    def options(self):
        """
        Returns a set of all valid options for this item.
        It's possible to have options item class-wide, and per item.
        """
        pclass_options = self.get_item_class().options.all()
        return set(pclass_options) or set(self.item_options.all())

    @property
    def is_shipping_required(self):
        return self.get_item_class().requires_shipping

    @property
    def has_stockrecords(self):
        """
        Test if this item has any stockrecords
        """
        return self.stockrecords.exists()

    @property
    def num_stockrecords(self):
        return self.stockrecords.count()

    @property
    def option_summary(self):
        """
        Return a string of all of a item's options
        """
        options = self.option_values.all()
        pairs = [option.summary() for option in options]
        return ", ".join(pairs)

    # The two properties below are deprecated because determining minimum
    # price is not as trivial as it sounds considering multiple stockrecords,
    # currencies, tax, etc.
    # The current implementation is very naive and only works for a limited
    # set of use cases.
    # At the very least, we should pass in the request and
    # user. Hence, it's best done as an extension to a Strategy class.
    # Once that is accomplished, these properties should be removed.

    @property
    @deprecated
    def min_child_price_incl_tax(self):
        """
        Return minimum child item price including tax.
        """
        return self._min_child_price('incl_tax')

    @property
    @deprecated
    def min_child_price_excl_tax(self):
        """
        Return minimum child item price excluding tax.

        This is a very naive approach; see the deprecation notice above. And
        only use it for display purposes (e.g. "new Oscar shirt, prices
        starting from $9.50").
        """
        return self._min_child_price('excl_tax')

    def _min_child_price(self, prop):
        """
        Return minimum child item price.

        This is for visual purposes only. It ignores currencies, most of the
        Strategy logic for selecting stockrecords, knows nothing about the
        current user or request, etc. It's only here to ensure
        backwards-compatibility; the previous implementation wasn't any
        better.
        """
        strategy = Selector().strategy()

        children_stock = strategy.select_children_stockrecords(self)
        prices = [
            strategy.pricing_policy(child, stockrecord)
            for child, stockrecord in children_stock]
        raw_prices = sorted([getattr(price, prop) for price in prices])
        return raw_prices[0] if raw_prices else None

    # Wrappers for child items

    def get_title(self):
        """
        Return a item's title or it's parent's title if it has no title
        """
        title = self.title
        if not title and self.parent_id:
            title = self.parent.title
        return title
    get_title.short_description = pgettext_lazy(u"Product title", u"Title")

    def get_item_class(self):
        """
        Return a item's item class. Child items inherit their parent's.
        """
        if self.is_child:
            return self.parent.item_class
        else:
            return self.item_class
    get_item_class.short_description = _("Product class")

    def get_is_discountable(self):
        """
        At the moment, is_discountable can't be set individually for child
        items; they inherit it from their parent.
        """
        if self.is_child:
            return self.parent.is_discountable
        else:
            return self.is_discountable

    def get_categories(self):
        """
        Return a item's categories or parent's if there is a parent item.
        """
        if self.is_child:
            return self.parent.categories
        else:
            return self.categories
    get_categories.short_description = _("Categories")

    # Images

    def get_missing_image(self):
        """
        Returns a missing image object.
        """
        # This class should have a 'name' property so it mimics the Django file
        # field.
        return MissingProductImage()

    def primary_image(self):
        """
        Returns the primary image for a item. Usually used when one can
        only display one item image, e.g. in a list of items.
        """
        images = self.images.all()
        ordering = self.images.model.Meta.ordering
        if not ordering or ordering[0] != 'display_order':
            # Only apply order_by() if a custom model doesn't use default
            # ordering. Applying order_by() busts the prefetch cache of
            # the ProductManager
            images = images.order_by('display_order')
        try:
            return images[0]
        except IndexError:
            # We return a dict with fields that mirror the key properties of
            # the ProductImage class so this missing image can be used
            # interchangeably in templates.  Strategy pattern ftw!
            return {
                'original': self.get_missing_image(),
                'caption': '',
                'is_missing': True}

    # Updating methods

    def update_rating(self):
        """
        Recalculate rating field
        """
        self.rating = self.calculate_rating()
        self.save()
    update_rating.alters_data = True

    def calculate_rating(self):
        """
        Calculate rating value
        """
        result = self.reviews.filter(
            status=self.reviews.model.APPROVED
        ).aggregate(
            sum=Sum('score'), count=Count('id'))
        reviews_sum = result['sum'] or 0
        reviews_count = result['count'] or 0
        rating = None
        if reviews_count > 0:
            rating = float(reviews_sum) / reviews_count
        return rating

    def has_review_by(self, user):
        if user.is_anonymous():
            return False
        return self.reviews.filter(user=user).exists()

    def is_review_permitted(self, user):
        """
        Determines whether a user may add a review on this item.

        Default implementation respects OSCAR_ALLOW_ANON_REVIEWS and only
        allows leaving one review per user and item.

        Override this if you want to alter the default behaviour; e.g. enforce
        that a user purchased the item to be allowed to leave a review.
        """
        if user.is_authenticated() or settings.OSCAR_ALLOW_ANON_REVIEWS:
            return not self.has_review_by(user)
        else:
            return False

    @cached_property
    def num_approved_reviews(self):
        return self.reviews.filter(
            status=self.reviews.model.APPROVED).count()

class ItemClass(models.Model):
    """
    Used for defining options and options for a subset of items.
    E.g. Books, DVDs and Toys. A item can only belong to one item class.

    At least one item class must be created when setting up a new
    Oscar deployment.

    Not necessarily equivalent to top-level categories but usually will be.
    """
    name = models.CharField(_('Name'), max_length=128)
    slug = AutoSlugField(_('Slug'), max_length=128, unique=True,
                         populate_from='name')

    #: Some item type don't require shipping (eg digital items) - we use
    #: this field to take some shortcuts in the checkout.
    requires_shipping = models.BooleanField(_("Requires shipping?"),
                                            default=True)

    #: Digital items generally don't require their stock levels to be
    #: tracked.
    track_stock = models.BooleanField(_("Track stock levels?"), default=True)

    #: These are the options (set by the user when they add to basket) for this
    #: item class.  For instance, a item class of "SMS message" would always
    #: require a message to be specified before it could be bought.
    #: Note that you can also set options on a per-item level.
    options = models.ManyToManyField(
        'materials.OptionClass', blank=True, verbose_name=_("Options"))

    class Meta:
        ordering = ['name']
        verbose_name = _("Item class")
        verbose_name_plural = _("Item classes")

    def __str__(self):
        return self.name

    @property
    def has_options(self):
        return self.options.exists()

class OptionClass(models.Model):
    """
    An option that can be selected for a particular item when the item
    is added to the basket.

    For example,  a list ID for an SMS message send, or a personalised message
    to print on a T-shirt.

    This is not the same as an 'option' as options do not have a fixed value
    for a particular item.  Instead, option need to be specified by a customer
    when they add the item to their basket.
    """
    name = models.CharField(_("Name"), max_length=128)
    code = AutoSlugField(_("Code"), max_length=128, unique=True,
                         populate_from='name')

    REQUIRED, OPTIONAL = ('Required', 'Optional')
    TYPE_CHOICES = (
        (REQUIRED, _("Required - a value for this option must be specified")),
        (OPTIONAL, _("Optional - a value for this option can be omitted")),
    )
    type = models.CharField(_("Status"), max_length=128, default=REQUIRED,
                            choices=TYPE_CHOICES)

    class Meta:
        verbose_name = _("Option class")
        verbose_name_plural = _("Options class")

    def __str__(self):
        return self.name

    @property
    def is_required(self):
        return self.type == self.REQUIRED

class ItemOption(models.Model):
    """
    Defines an option for a item class. (For example, number_of_pages for
    a 'book' class)
    """
    name = models.CharField(_('Name'), max_length=128)
    code = models.SlugField(
        _('Code'), max_length=128,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z\-_][0-9a-zA-Z\-_]*$',
            message=_("Code can only contain the letters a-z, A-Z, digits, "
                      "minus and underscores, and can't start with a digit"))])

    # Attribute types
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    RICHTEXT = "richtext"
    DATE = "date"
    OPTION = "option"
    ENTITY = "entity"
    FILE = "file"
    IMAGE = "image"
    TYPE_CHOICES = (
        (TEXT, _("Text")),
        (INTEGER, _("Integer")),
        (BOOLEAN, _("True / False")),
        (FLOAT, _("Float")),
        (RICHTEXT, _("Rich Text")),
        (DATE, _("Date")),
        (OPTION, _("Option")),
        (ENTITY, _("Entity")),
        (FILE, _("File")),
        (IMAGE, _("Image")),
    )
    type = models.CharField(
        choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],
        max_length=20, verbose_name=_("Type"))

    required = models.BooleanField(_('Required'), default=False)

    class Meta:
        ordering = ['code']
        verbose_name = _('Item option')
        verbose_name_plural = _('Item options')

    @property
    def is_option(self):
        return self.type == self.OPTION

    @property
    def is_file(self):
        return self.type in [self.FILE, self.IMAGE]

    def __str__(self):
        return self.name

    def save_value(self, item, value):
        ItemOptionValue = get_model('materials', 'ItemOptionValue')
        try:
            value_obj = item.option_values.get(option=self)
        except ItemOptionValue.DoesNotExist:
            # FileField uses False for announcing deletion of the file
            # not creating a new value
            delete_file = self.is_file and value is False
            if value is None or value == '' or delete_file:
                return
            value_obj = ItemOptionValue.objects.create(
                item=item, option=self)

        if self.is_file:
            # File fields in Django are treated differently, see
            # django.db.models.fields.FileField and method save_form_data
            if value is None:
                # No change
                return
            elif value is False:
                # Delete file
                value_obj.delete()
            else:
                # New uploaded file
                value_obj.value = value
                value_obj.save()
        else:
            if value is None or value == '':
                value_obj.delete()
                return
            if value != value_obj.value:
                value_obj.value = value
                value_obj.save()

    def validate_value(self, value):
        validator = getattr(self, '_validate_%s' % self.type)
        validator(value)

    # Validators

    def _validate_text(self, value):
        if not isinstance(value, six.string_types):
            raise ValidationError(_("Must be str or unicode"))
    _validate_richtext = _validate_text

    def _validate_float(self, value):
        try:
            float(value)
        except ValueError:
            raise ValidationError(_("Must be a float"))

    def _validate_integer(self, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError(_("Must be an integer"))

    def _validate_date(self, value):
        if not (isinstance(value, datetime) or isinstance(value, date)):
            raise ValidationError(_("Must be a date or datetime"))

    def _validate_boolean(self, value):
        if not type(value) == bool:
            raise ValidationError(_("Must be a boolean"))

    def _validate_entity(self, value):
        if not isinstance(value, models.Model):
            raise ValidationError(_("Must be a model instance"))

    def _validate_file(self, value):
        if value and not isinstance(value, File):
            raise ValidationError(_("Must be a file field"))
    _validate_image = _validate_file

class ItemOptionValue(models.Model):
    """
    The "through" model for the m2m relationship between catalogue.Product and
    catalogue.ProductAttribute.  This specifies the value of the option for
    a particular item

    For example: number_of_pages = 295
    """
    option = models.ForeignKey(
        'materials.ItemOption', verbose_name=_("Option"))
    item = models.ForeignKey(
        'materials.Item', related_name='option_values',
        verbose_name=_("Item"))

    value_text = models.TextField(_('Text'), blank=True, null=True)
    value_integer = models.IntegerField(_('Integer'), blank=True, null=True)
    value_boolean = models.NullBooleanField(_('Boolean'), blank=True)
    value_float = models.FloatField(_('Float'), blank=True, null=True)
    value_richtext = models.TextField(_('Richtext'), blank=True, null=True)
    value_date = models.DateField(_('Date'), blank=True, null=True)
    value_file = models.FileField(
        upload_to='self._meta.app_label', max_length=255,
        blank=True, null=True)
    value_image = models.ImageField(
        upload_to='self._meta.app_label', max_length=255,
        blank=True, null=True)
    value_entity = GenericForeignKey(
        'entity_content_type', 'entity_object_id')

    entity_content_type = models.ForeignKey(
        ContentType, null=True, blank=True, editable=False)
    entity_object_id = models.PositiveIntegerField(
        null=True, blank=True, editable=False)

    def _get_value(self):
        return getattr(self, 'value_%s' % self.option.type)

    def _set_value(self, new_value):
        if self.option.is_option and isinstance(new_value, str):
            # Need to look up instance of AttributeOption
            new_value = self.option.option_group.options.get(
                option=new_value)
        setattr(self, 'value_%s' % self.option.type, new_value)

    value = property(_get_value, _set_value)

    class Meta:
        unique_together = ('option', 'item')
        verbose_name = _('Item option value')
        verbose_name_plural = _('Item option values')

    def __str__(self):
        return self.summary()

    def summary(self):
        """
        Gets a string representation of both the option and it's value,
        used e.g in item summaries.
        """
        return u"%s: %s" % (self.option.name, self.value_as_text)

    @property
    def value_as_text(self):
        """
        Returns a string representation of the option's value. To customise
        e.g. image option values, declare a _image_as_text property and
        return something appropriate.
        """
        property_name = '_%s_as_text' % self.option.type
        return getattr(self, property_name, self.value)

    @property
    def _richtext_as_text(self):
        return strip_tags(self.value)

    @property
    def _entity_as_text(self):
        """
        Returns the unicode representation of the related model. You likely
        want to customise this (and maybe _entity_as_html) if you use entities.
        """
        return six.text_type(self.value)

    @property
    def value_as_html(self):
        """
        Returns a HTML representation of the option's value. To customise
        e.g. image option values, declare a _image_as_html property and
        return e.g. an <img> tag.  Defaults to the _as_text representation.
        """
        property_name = '_%s_as_html' % self.option.type
        return getattr(self, property_name, self.value_as_text)

    @property
    def _richtext_as_html(self):
        return mark_safe(self.value)
