from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class ExUser(models.Model):
    user = models.OneToOneField(User, related_name='ex_user')
    img = models.ImageField(verbose_name=_('Image'), upload_to='images/ex_user/')

    class Meta:
        verbose_name = _('Extend user')
        verbose_name_plural = _('Extends user')

    def img_preview(self):
        return u'<img src="%s" style="max-width:100px; max-height:100px" >' % self.img.url
    img_preview.short_description = _('Image')
    img_preview.allow_tags = True