from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from fs import settings

class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    parent = models.ForeignKey('self', verbose_name=_('Parent'), related_name='groups', blank=True, null=True)
    sort = models.IntegerField(verbose_name=_('Sort'), blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    def __unicode__(self):
        return self.title

    def clean(self):
        super(Group, self).clean()

        if self.parent == self:
            raise ValidationError({'parent': _('Object can not refer to itself')})

        if self.parent in self.groups.all():
            raise ValidationError({'parent': _('Object can not refer to objects that reference it')})

    def is_root(self):
        return self.groups.exists()

    def get_parent(self):
        return self.parent

    def get_depth(self, depth=0):
        if self.parent:
            depth += 2
            return self.parent.get_depth(depth)
        return depth

    def get_children_count(self):
        return self.groups.count()

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
    groups = models.ManyToManyField('Group', verbose_name=_('Group'), related_name='items', blank=True, null=True)
    main_group = models.ForeignKey('Group', verbose_name=_('Main Group'))
    enable = models.BooleanField(_('Enable'), default=True)
    recommend_item = models.ManyToManyField('self', verbose_name=_('Recommended item'), blank=True)
    main_image = models.ImageField(_('Main Image'), upload_to='images/materials/%Y/%m/', blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, verbose_name=_('Tags'))
    date_create = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    item_class = models.ForeignKey('ItemClass', blank=True, null=True)
    popular = models.BigIntegerField(_('Popular'), editable=False, blank=True, default=0)
    description = models.TextField(verbose_name=_('Description'))

    class Meta:
        ordering = ['-date_create']
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_item', kwargs={'slug': self.slug, 'group': self.main_group})

    def attribute_summary(self):
        item_attr_relate = ItemAttributeRelationship.objects.filter(item=self, attribute=self.attributes.all())
        attributes = ['%s: %s' % (value, ', '.join([attr_value.title for attr_value in value.attribute_values.all()])) for value in item_attr_relate]
        return '; '.join(attributes)

class ItemImages(models.Model):
    image = models.ImageField(verbose_name=_('Image item'), upload_to='images/materials/%Y/%m/')
    title = models.CharField(verbose_name=_('Title image'), blank=True, max_length=200)
    item = models.ForeignKey('Item', related_name='images')

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
        return self.attribute.title