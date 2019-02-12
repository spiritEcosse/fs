from django.contrib import admin
from ex_user.models import ExUser


class ExUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'img_preview')

admin.site.register(ExUser, ExUserAdmin)