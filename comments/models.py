from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Comment(models.Model):
    text = models.TextField(_('Text comment'), max_length=2000)
    user = models.ForeignKey(User)
    date_create = models.DateTimeField(auto_now_add=True)
    enable = models.BooleanField(_('Enable'), default=False)
    complaint = models.TextField(_('Complaint on comment'), blank=True)
    like = models.BigIntegerField(_('Like'), default=0)
    not_like = models.BigIntegerField(_('Not like'), default=0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    like_object = models.BooleanField(_('Like'))

    class Meta:
        ordering = ['-date_create']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __unicode__(self):
        return self.text[:100]