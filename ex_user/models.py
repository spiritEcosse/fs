from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from materials.models import Item


class ExUser(models.Model):
    user = models.OneToOneField(User, related_name='ex_user')
    img = models.ImageField(verbose_name=_('Image'), upload_to='images/ex_user/')
    liked = models.ManyToManyField(Item, verbose_name=_('My Favorites'), related_name='users_liked')
    defer = models.ManyToManyField(Item, verbose_name=_('For the future'), related_name='users_defer')
    like_item = models.ManyToManyField(Item, verbose_name=_('Like this'), related_name='user_like')
    not_like_item = models.ManyToManyField(Item, verbose_name=_('Not like this'), related_name='user_not_like')

    class Meta:
        verbose_name = _('Extend user')
        verbose_name_plural = _('Extends user')

    def img_preview(self):
        return u'<img src="%s" style="max-width:100px; max-height:100px" >' % self.img.url
    img_preview.short_description = _('Image')
    img_preview.allow_tags = True