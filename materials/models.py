from datetime import datetime, date

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import six
from django.core.files.base import File
from django.contrib.contenttypes.admin import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.utils.functional import cached_property
from django.utils.encoding import python_2_unicode_compatible

from fs import settings
from fs.core.decorators import deprecated
from fs.core.loading import get_model
from fs.models.fields import AutoSlugField

class ItemClass(models.Model):
    title = models.CharField(max_length=200)
    attributes = models.ManyToManyField('Attribute', related_name='item_classes')

    class Meta:
        ordering = ['title']
        verbose_name = _('Item class')
        verbose_name_plural = _('Item classes')

    def __unicode__(self):
        return self.title

class Item(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    origin_title = models.CharField(_('Origin title'), max_length=200, blank=True)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    attributes = models.ManyToManyField('Attribute', verbose_name=_('Attributes'), through='ItemAttributeRelationship', related_name='items')
    enable = models.BooleanField(_('Enable'), default=True)
    recommend_item = models.ManyToManyField('self', verbose_name=_('Recommended item'), blank=True)
    main_image = models.ImageField(_('Main Image'), upload_to=settings.IMAGE_FOLDER, blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, verbose_name=_('Tags'))
    date_create = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    item_class = models.ForeignKey('ItemClass', blank=True, null=True)

    class Meta:
        ordering = ['-date_create']
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def __unicode__(self):
        return self.title

    def attribute_summary(self):
        attributes = ['%s' % attribute.item_attributes.all() for attribute in self.attributes.all()]
        return '; '.join(attributes)

class Attribute(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    enable = models.BooleanField(_('Enable'), default=True)

    class Meta:
        ordering = ['title']
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    def __unicode__(self):
        return self.title

class AttributeValue(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    attribute = models.ForeignKey('Attribute', verbose_name=_('Attribute'), related_name="attribute_values")

    class Meta:
        ordering = ['title']
        verbose_name = _('Attribute value')
        verbose_name_plural = _('Attribute values')

    def __unicode__(self):
        return self.title

class ItemAttributeRelationship(models.Model):
    item = models.ForeignKey('Item')
    attribute = models.ForeignKey('Attribute', related_name='item_attributes')
    attribute_values = models.ManyToManyField('AttributeValue')

    def __unicode__(self):
        return self.get()

    def get_a(self):
        item_attribute_values = [value.title for value in self.attribute_values.all()]
        return '%s:  %s' % (self.attribute.title, ', '.join(item_attribute_values))

# class Group(models.Model):
#     name = models.CharField(max_length=100)
#     parent = models.ForeignKey('self', blank=True, null=True)
#     icon = models.ImageField(upload_to=settings.IMAGE_FOLDER, blank=True)
#     enable = models.BooleanField(default=True)
#     date_create = models.DateTimeField(auto_now_add=True)
#     date_last_modified = models.DateTimeField(auto_now=True)
#
#     def __unicode__(self):
#         return self.name
#
# class ItemAttributesContainer(object):
#     """
#     Stolen liberally from django-eav, but simplified to be item-specific
#
#     To set options on a item, use the `attr` option:
#
#         item.attr.weight = 125
#     """
#
#     def __setstate__(self, state):
#         self.__dict__ = state
#         self.initialised = False
#
#     def __init__(self, item):
#         self.item = item
#         self.initialised = False
#
#     def __getattr__(self, name):
#         if not name.startswith('_') and not self.initialised:
#             values = self.get_values().select_related('attribute')
#             for v in values:
#                 setattr(self, v.attribute.code, v.value)
#             self.initialised = True
#             return getattr(self, name)
#         raise AttributeError(
#             _("%(obj)s has no attribute named '%(attr)s'") % {
#                 'obj': self.item.get_item_class(), 'attr': name})
#
#     def validate_attributes(self):
#         for attribute in self.get_all_attributes():
#             value = getattr(self, attribute.code, None)
#             if value is None:
#                 if attribute.required:
#                     raise ValidationError(
#                         _("%(attr)s attribute cannot be blank") %
#                         {'attr': attribute.code})
#             # else:
#             #     try:
#             #         attribute.validate_value(value)
#             #     except ValidationError as e:
#             #         raise ValidationError(
#             #             _("%(attr)s attribute %(err)s") %
#             #             {'attr': attribute.code, 'err': e})
#
#     def get_values(self):
#         return self.item.attribute_values.all()
#
#     def get_value_by_attribute(self, attribute):
#         return self.get_values().get(attribute=attribute)
#
#     def get_all_attributes(self):
#         return self.item.get_item_class().attributes.all()
#
#     def get_attribute_by_code(self, code):
#         return self.get_all_attributes().get(code=code)
#
#     def __iter__(self):
#         return iter(self.get_values())
#
#     def save(self):
#         for attribute in self.get_all_attributes():
#             if hasattr(self, attribute.code):
#                 value = getattr(self, attribute.code)
#                 attribute.save_value(self.item, value)
#
# @python_2_unicode_compatible
# class Item(models.Model):
#     STANDALONE, PARENT, CHILD = 'standalone', 'parent', 'child'
#     STRUCTURE_CHOICES = (
#         (STANDALONE, _('Stand-alone item')),
#         (PARENT, _('Parent item')),
#         (CHILD, _('Child item'))
#     )
#     structure = models.CharField(
#         _("Item structure"), max_length=10, choices=STRUCTURE_CHOICES,
#         default=STANDALONE)
#
#     parent = models.ForeignKey(
#         'self', null=True, blank=True, related_name='children',
#         verbose_name=_("Parent item"),
#         help_text=_("Only choose a parent item if you're creating a child "
#                     "item.  For example if this is a size "
#                     "4 of a particular t-shirt.  Leave blank if this is a "
#                     "stand-alone item (i.e. there is only one version of"
#                     " this item)."))
#
#     item_class = models.ForeignKey(
#         'materials.ItemClass', null=True, blank=True, on_delete=models.PROTECT,
#         verbose_name=_('Item class'), related_name="items",
#         help_text=_("Choose what type of item this is"))
#
#     group = models.ForeignKey('materials.Group', blank=True, null=True)
#     title = models.CharField(_('Title'), max_length=100)
#     slug = models.SlugField(_('Slug'), max_length=255, unique=False)
#     origin_title = models.CharField(max_length=100, blank=True)
#     enable = models.BooleanField(default=True)
#     main_image = models.ImageField(upload_to=settings.IMAGE_FOLDER, blank=True, null=True)
#     trailer_link = models.URLField(blank=True, null=True)
#     trailer_image = models.ImageField(upload_to=settings.IMAGE_FOLDER, blank=True, null=True)
#     date_create = models.DateTimeField(auto_now_add=True)
#     date_last_modified = models.DateTimeField(auto_now=True)
#     description = models.TextField(blank=True)
#     images = ArrayField(models.ImageField(upload_to=settings.IMAGE_FOLDER), blank=True)
#     tags = ArrayField(models.CharField(max_length=100), blank=True)
#     related_items = models.ManyToManyField('self', blank=True)
#
#     attributes = models.ManyToManyField(
#         'materials.ItemAttribute',
#         through='ItemAttributeValue',
#         verbose_name=_("Attributes"),
#         help_text=_("A item attribute is something that this item may "
#                     "have, such as a size, as specified by its class"))
#
#     item_options = models.ManyToManyField(
#         'materials.Option', blank=True, verbose_name=_("Item options"),
#         help_text=_("Options are values that can be associated with a item "
#                     "when it is added to a customer's basket.  This could be "
#                     "something like a personalised message to be printed on "
#                     "a T-shirt."))
#
#     class Meta:
#         ordering = ['-date_create']
#         verbose_name = _('Item')
#         verbose_name_plural = _('Items')
#
#     def __init__(self, *args, **kwargs):
#         super(Item, self).__init__(*args, **kwargs)
#         self.attr = ItemAttributesContainer(item=self)
#
#     def __str__(self):
#         if self.title:
#             return self.title
#         if self.attribute_summary:
#             return u"%s (%s)" % (self.get_title(), self.attribute_summary)
#         else:
#             return self.get_title()
#
#     def get_absolute_url(self):
#         """
#         Return a item's absolute url
#         """
#         return reverse('materials:detail',
#                        kwargs={'item_slug': self.slug, 'pk': self.id})
#
#     def clean(self):
#         """
#         Validate a item. Those are the rules:
#
#         +---------------+-------------+--------------+--------------+
#         |               | stand alone | parent       | child        |
#         +---------------+-------------+--------------+--------------+
#         | title         | required    | required     | optional     |
#         +---------------+-------------+--------------+--------------+
#         | item class | required    | required     | must be None |
#         +---------------+-------------+--------------+--------------+
#         | parent        | forbidden   | forbidden    | required     |
#         +---------------+-------------+--------------+--------------+
#         | categories    | 1 or more   | 1 or more    | forbidden    |
#         +---------------+-------------+--------------+--------------+
#         | attributes    | optional    | optional     | optional     |
#         +---------------+-------------+--------------+--------------+
#         | rec. items | optional    | optional     | unsupported  |
#         +---------------+-------------+--------------+--------------+
#         | options       | optional    | optional     | forbidden    |
#         +---------------+-------------+--------------+--------------+
#
#         Because the validation logic is quite complex, validation is delegated
#         to the sub method appropriate for the item's structure.
#         """
#         getattr(self, '_clean_%s' % self.structure)()
#         if not self.is_parent:
#             self.attr.validate_attributes()
#
#     def _clean_standalone(self):
#         """
#         Validates a stand-alone item
#         """
#         validate_dict = {}
#
#         if not self.item_class:
#             validate_dict["item_class"] = _("Your item must have a item class.")
#         if self.parent_id:
#             validate_dict["parent"] = _("Only child items can have a parent.")
#
#         if validate_dict:
#             raise ValidationError(validate_dict)
#
#     def _clean_child(self):
#         """
#         Validates a child item
#         """
#         validate_dict = {}
#
#         if not self.parent_id:
#             validate_dict["parent"] = _("A child item needs a parent")
#         if self.parent_id and not self.parent.is_parent:
#             validate_dict["parent"] = _("You can only assign child items to parent items")
#         if self.item_class:
#             validate_dict["item_class"] = _("A child item can't have a item class.")
#         if self.pk and self.group.exists():
#             validate_dict["group"] = _("A child item can't have a category assigned.")
#         # Note that we only forbid options on item level
#         if self.pk and self.item_options.exists():
#             validate_dict["item_options"] = _("A child item can't have options.")
#
#         if validate_dict:
#             raise ValidationError(validate_dict)
#
#     def _clean_parent(self):
#         """
#         Validates a parent item.
#         """
#         self._clean_standalone()
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.get_title())
#         super(Item, self).save(*args, **kwargs)
#         self.attr.save()
#
#     # Properties
#
#     @property
#     def is_standalone(self):
#         return self.structure == self.STANDALONE
#
#     @property
#     def is_parent(self):
#         return self.structure == self.PARENT
#
#     @property
#     def is_child(self):
#         return self.structure == self.CHILD
#
#     def can_be_parent(self, give_reason=False):
#         """
#         Helps decide if a the item can be turned into a parent item.
#         """
#         reason = None
#         if self.is_child:
#             reason = _('The specified parent item is a child item.')
#         is_valid = reason is None
#         if give_reason:
#             return is_valid, reason
#         else:
#             return is_valid
#
#     @property
#     def options(self):
#         """
#         Returns a set of all valid options for this item.
#         It's possible to have options item class-wide, and per item.
#         """
#         pclass_options = self.get_item_class().options.all()
#         return set(pclass_options) or set(self.item_options.all())
#
#     @property
#     def is_shipping_required(self):
#         return self.get_item_class().requires_shipping
#
#     @property
#     def attribute_summary(self):
#         """
#         Return a string of all of a item's attributes
#         """
#         attributes = self.attribute_values.all()
#         pairs = [attribute.summary() for attribute in attributes]
#         return ", ".join(pairs)
#
#     # Wrappers for child items
#
#     def get_title(self):
#         """
#         Return a item's title or it's parent's title if it has no title
#         """
#         title = self.title
#         if not title and self.parent_id:
#             title = self.parent.title
#         return title
#     get_title.short_description = pgettext_lazy(u"Item title", u"Title")
#
#     def get_item_class(self):
#         """
#         Return a item's item class. Child items inherit their parent's.
#         """
#         if self.is_child:
#             return self.parent.item_class
#         else:
#             return self.item_class
#     get_item_class.short_description = _("Item class")
#
#     def get_is_discountable(self):
#         """
#         At the moment, is_discountable can't be set individually for child
#         items; they inherit it from their parent.
#         """
#         if self.is_child:
#             return self.parent.is_discountable
#         else:
#             return self.is_discountable
#
#     def get_categories(self):
#         """
#         Return a item's categories or parent's if there is a parent item.
#         """
#         if self.is_child:
#             return self.parent.categories
#         else:
#             return self.categories
#     get_categories.short_description = _("Categories")
#
#     # Images
#
#     # def get_missing_image(self):
#     #     """
#     #     Returns a missing image object.
#     #     """
#     #     # This class should have a 'name' property so it mimics the Django file
#     #     # field.
#     #     return MissingProductImage()
#
#     def primary_image(self):
#         """
#         Returns the primary image for a item. Usually used when one can
#         only display one item image, e.g. in a list of items.
#         """
#         images = self.images.all()
#         ordering = self.images.model.Meta.ordering
#         if not ordering or ordering[0] != 'display_order':
#             # Only apply order_by() if a custom model doesn't use default
#             # ordering. Applying order_by() busts the prefetch cache of
#             # the ProductManager
#             images = images.order_by('display_order')
#         try:
#             return images[0]
#         except IndexError:
#             # We return a dict with fields that mirror the key properties of
#             # the ProductImage class so this missing image can be used
#             # interchangeably in templates.  Strategy pattern ftw!
#             return {
#                 'original': self.get_missing_image(),
#                 'caption': '',
#                 'is_missing': True}
#
#     # Updating methods
#
#     def update_rating(self):
#         """
#         Recalculate rating field
#         """
#         self.rating = self.calculate_rating()
#         self.save()
#     update_rating.alters_data = True
#
#     def has_review_by(self, user):
#         if user.is_anonymous():
#             return False
#         return self.reviews.filter(user=user).exists()
#
#     def is_review_permitted(self, user):
#         """
#         Determines whether a user may add a review on this item.
#
#         Default implementation respects OSCAR_ALLOW_ANON_REVIEWS and only
#         allows leaving one review per user and item.
#
#         Override this if you want to alter the default behaviour; e.g. enforce
#         that a user purchased the item to be allowed to leave a review.
#         """
#         if user.is_authenticated(): #... or settings.OSCAR_ALLOW_ANON_REVIEWS
#             return not self.has_review_by(user)
#         else:
#             return False
#
#     @cached_property
#     def num_approved_reviews(self):
#         return self.reviews.filter(
#             status=self.reviews.model.APPROVED).count()
#
# @python_2_unicode_compatible
# class ItemClass(models.Model):
#     """
#     Used for defining options and options for a subset of items.
#     E.g. Books, DVDs and Toys. A item can only belong to one item class.
#
#     At least one item class must be created when setting up a new
#     Oscar deployment.
#
#     Not necessarily equivalent to top-level categories but usually will be.
#     """
#     name = models.CharField(_('Name'), max_length=128)
#     slug = AutoSlugField(_('Slug'), max_length=128, unique=True,
#                          populate_from='name')
#
#     #: Some item type don't require shipping (eg digital items) - we use
#     #: this field to take some shortcuts in the checkout.
#     requires_shipping = models.BooleanField(_("Requires shipping?"),
#                                             default=True)
#
#     #: Digital items generally don't require their stock levels to be
#     #: tracked.
#     track_stock = models.BooleanField(_("Track stock levels?"), default=True)
#
#     #: These are the options (set by the user when they add to basket) for this
#     #: item class.  For instance, a item class of "SMS message" would always
#     #: require a message to be specified before it could be bought.
#     #: Note that you can also set options on a per-item level.
#     options = models.ManyToManyField(
#         'materials.Option', blank=True, verbose_name=_("Options"))
#
#     class Meta:
#         ordering = ['name']
#         verbose_name = _("Item class")
#         verbose_name_plural = _("Item classes")
#
#     def __str__(self):
#         return self.name
#
#     @property
#     def has_attributes(self):
#         return self.attributes.exists()
#
# @python_2_unicode_compatible
# class Option(models.Model):
#     """
#     An option that can be selected for a particular item when the item
#     is added to the basket.
#
#     For example,  a list ID for an SMS message send, or a personalised message
#     to print on a T-shirt.
#
#     This is not the same as an 'option' as options do not have a fixed value
#     for a particular item.  Instead, option need to be specified by a customer
#     when they add the item to their basket.
#     """
#     name = models.CharField(_("Name"), max_length=128)
#     code = AutoSlugField(_("Code"), max_length=128, unique=True,
#                          populate_from='name')
#
#     REQUIRED, OPTIONAL = ('Required', 'Optional')
#     TYPE_CHOICES = (
#         (REQUIRED, _("Required - a value for this option must be specified")),
#         (OPTIONAL, _("Optional - a value for this option can be omitted")),
#     )
#     type = models.CharField(_("Status"), max_length=128, default=REQUIRED,
#                             choices=TYPE_CHOICES)
#
#     class Meta:
#         verbose_name = _("Option")
#         verbose_name_plural = _("Options")
#
#     def __str__(self):
#         return self.name
#
#     @property
#     def is_required(self):
#         return self.type == self.REQUIRED
#
# @python_2_unicode_compatible
# class ItemAttribute(models.Model):
#     """
#     Defines an option for a item class. (For example, number_of_pages for
#     a 'book' class)
#     """
#     item_class = models.ForeignKey(
#         'materials.ItemClass', related_name='attributes', blank=True,
#         null=True, verbose_name=_("Item type"))
#     name = models.CharField(_('Name'), max_length=128)
#     code = models.SlugField(
#         _('Code'), max_length=128,
#         validators=[RegexValidator(
#             regex=r'^[a-zA-Z\-_][0-9a-zA-Z\-_]*$',
#             message=_("Code can only contain the letters a-z, A-Z, digits, "
#                       "minus and underscores, and can't start with a digit"))])
#
#     # Attribute types
#     TEXT = "text"
#     INTEGER = "integer"
#     BOOLEAN = "boolean"
#     FLOAT = "float"
#     RICHTEXT = "richtext"
#     DATE = "date"
#     OPTION = "option"
#     ENTITY = "entity"
#     FILE = "file"
#     IMAGE = "image"
#     TYPE_CHOICES = (
#         (TEXT, _("Text")),
#         (INTEGER, _("Integer")),
#         (BOOLEAN, _("True / False")),
#         (FLOAT, _("Float")),
#         (RICHTEXT, _("Rich Text")),
#         (DATE, _("Date")),
#         (OPTION, _("Option")),
#         (ENTITY, _("Entity")),
#         (FILE, _("File")),
#         (IMAGE, _("Image")),
#     )
#     type = models.CharField(
#         choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],
#         max_length=20, verbose_name=_("Type"))
#
#     option_group = models.ForeignKey(
#         'materials.AttributeOptionGroup', blank=True, null=True,
#         verbose_name=_("Option Group"),
#         help_text=_('Select an option group if using type "Option"'))
#     required = models.BooleanField(_('Required'), default=False)
#
#     class Meta:
#         ordering = ['code']
#         verbose_name = _('Item attribute')
#         verbose_name_plural = _('Item attributes')
#
#     @property
#     def is_option(self):
#         return self.type == self.OPTION
#
#     @property
#     def is_file(self):
#         return self.type in [self.FILE, self.IMAGE]
#
#     def __str__(self):
#         return self.name
#
#     def save_value(self, item, value):
#         ItemAttributeValue = get_model('materials', 'ItemAttributeValue')
#         try:
#             value_obj = item.attribute_values.get(attribute=self)
#         except ItemAttributeValue.DoesNotExist:
#             # FileField uses False for announcing deletion of the file
#             # not creating a new value
#             delete_file = self.is_file and value is False
#             if value is None or value == '' or delete_file:
#                 return
#             value_obj = ItemAttributeValue.objects.create(
#                 item=item, attribute=self)
#
#         if self.is_file:
#             # File fields in Django are treated differently, see
#             # django.db.models.fields.FileField and method save_form_data
#             if value is None:
#                 # No change
#                 return
#             elif value is False:
#                 # Delete file
#                 value_obj.delete()
#             else:
#                 # New uploaded file
#                 value_obj.value = value
#                 value_obj.save()
#         else:
#             if value is None or value == '':
#                 value_obj.delete()
#                 return
#             if value != value_obj.value:
#                 value_obj.value = value
#                 value_obj.save()
#
#     def validate_value(self, value):
#         validator = getattr(self, '_validate_%s' % self.type)
#         validator(value)
#
#     # Validators
#
#     def _validate_text(self, value):
#         if not isinstance(value, six.string_types):
#             raise ValidationError(_("Must be str or unicode"))
#     _validate_richtext = _validate_text
#
#     def _validate_float(self, value):
#         try:
#             float(value)
#         except ValueError:
#             raise ValidationError(_("Must be a float"))
#
#     def _validate_integer(self, value):
#         try:
#             int(value)
#         except ValueError:
#             raise ValidationError(_("Must be an integer"))
#
#     def _validate_date(self, value):
#         if not (isinstance(value, datetime) or isinstance(value, date)):
#             raise ValidationError(_("Must be a date or datetime"))
#
#     def _validate_boolean(self, value):
#         if not type(value) == bool:
#             raise ValidationError(_("Must be a boolean"))
#
#     def _validate_entity(self, value):
#         if not isinstance(value, models.Model):
#             raise ValidationError(_("Must be a model instance"))
#
#     def _validate_option(self, value):
#         if not isinstance(value, get_model('materials', 'AttributeOption')):
#             raise ValidationError(
#                 _("Must be an AttributeOption model object instance"))
#         if not value.pk:
#             raise ValidationError(_("AttributeOption has not been saved yet"))
#         valid_values = self.option_group.options.values_list(
#             'option', flat=True)
#         if value.option not in valid_values:
#             raise ValidationError(
#                 _("%(enum)s is not a valid choice for %(attr)s") %
#                 {'enum': value, 'attr': self})
#
#     def _validate_file(self, value):
#         if value and not isinstance(value, File):
#             raise ValidationError(_("Must be a file field"))
#     _validate_image = _validate_file
#
# @python_2_unicode_compatible
# class ItemAttributeValue(models.Model):
#     """
#     The "through" model for the m2m relationship between materials.Product and
#     materials.ProductAttribute.  This specifies the value of the option for
#     a particular item
#
#     For example: number_of_pages = 295
#     """
#     attribute = models.ForeignKey(
#         'materials.ItemAttribute', verbose_name=_("Attribute"))
#     item = models.ForeignKey(
#         'materials.Item', related_name='attribute_values',
#         verbose_name=_("Item"))
#
#     value_text = models.TextField(_('Text'), blank=True, null=True)
#     value_integer = models.IntegerField(_('Integer'), blank=True, null=True)
#     value_boolean = models.NullBooleanField(_('Boolean'), blank=True)
#     value_float = models.FloatField(_('Float'), blank=True, null=True)
#     value_richtext = models.TextField(_('Richtext'), blank=True, null=True)
#     value_date = models.DateField(_('Date'), blank=True, null=True)
#     value_option = models.ForeignKey(
#         'materials.AttributeOption', blank=True, null=True,
#         verbose_name=_("Value option"))
#     value_file = models.FileField(
#         upload_to=settings.IMAGE_FOLDER, max_length=255,
#         blank=True, null=True)
#     value_image = models.ImageField(
#         upload_to=settings.IMAGE_FOLDER, max_length=255,
#         blank=True, null=True)
#     value_entity = GenericForeignKey(
#         'entity_content_type', 'entity_object_id')
#
#     entity_content_type = models.ForeignKey(
#         ContentType, null=True, blank=True, editable=False)
#     entity_object_id = models.PositiveIntegerField(
#         null=True, blank=True, editable=False)
#
#     class Meta:
#         unique_together = ('attribute', 'item')
#         verbose_name = _('Item attribute value')
#         verbose_name_plural = _('Item attribute values')
#
#     def _get_value(self):
#         return getattr(self, 'value_%s' % self.attribute.type)
#
#     def _set_value(self, new_value):
#         if self.attribute.is_option and isinstance(new_value, str):
#             # Need to look up instance of AttributeOption
#             new_value = self.attribute.option_group.options.get(
#                 option=new_value)
#         setattr(self, 'value_%s' % self.attribute.type, new_value)
#
#     value = property(_get_value, _set_value)
#
#     def __str__(self):
#         return self.summary()
#
#     def summary(self):
#         """
#         Gets a string representation of both the attribute and it's value,
#         used e.g in item summaries.
#         """
#         return u"%s: %s" % (self.attribute.name, self.value_as_text)
#
#     @property
#     def value_as_text(self):
#         """
#         Returns a string representation of the attribute's value. To customise
#         e.g. image attribute values, declare a _image_as_text property and
#         return something appropriate.
#         """
#         property_name = '_%s_as_text' % self.attribute.type
#         return getattr(self, property_name, self.value)
#
#     @property
#     def _richtext_as_text(self):
#         return strip_tags(self.value)
#
#     @property
#     def _entity_as_text(self):
#         """
#         Returns the unicode representation of the related model. You likely
#         want to customise this (and maybe _entity_as_html) if you use entities.
#         """
#         return six.text_type(self.value)
#
#     @property
#     def value_as_html(self):
#         """
#         Returns a HTML representation of the attribute's value. To customise
#         e.g. image attribute values, declare a _image_as_html property and
#         return e.g. an <img> tag.  Defaults to the _as_text representation.
#         """
#         property_name = '_%s_as_html' % self.attribute.type
#         return getattr(self, property_name, self.value_as_text)
#
#     @property
#     def _richtext_as_html(self):
#         return mark_safe(self.value)
#
# @python_2_unicode_compatible
# class AttributeOptionGroup(models.Model):
#     """
#     Defines a group of options that collectively may be used as an
#     attribute type
#
#     For example, Language
#     """
#     name = models.CharField(_('Name'), max_length=128)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         app_label = 'materials'
#         verbose_name = _('Attribute option group')
#         verbose_name_plural = _('Attribute option groups')
#
#     @property
#     def option_summary(self):
#         options = [o.option for o in self.options.all()]
#         return ", ".join(options)
#
# @python_2_unicode_compatible
# class AttributeOption(models.Model):
#     """
#     Provides an option within an option group for an attribute type
#     Examples: In a Language group, English, Greek, French
#     """
#     group = models.ForeignKey(
#         'materials.AttributeOptionGroup', related_name='options',
#         verbose_name=_("Group"))
#     option = models.CharField(_('Option'), max_length=255)
#
#     def __str__(self):
#         return self.option
#
#     class Meta:
#         app_label = 'materials'
#         verbose_name = _('Attribute option')
#         verbose_name_plural = _('Attribute options')