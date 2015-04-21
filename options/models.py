from django.db import models

# Create your models here.

class Option(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='icon/', blank=True)
    enable = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class OptionValue(models.Model):
    name = models.CharField(max_length=100)
    option = models.ForeignKey(Option)

    def __unicode__(self):
        return self.name
