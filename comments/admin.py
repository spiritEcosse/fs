from django.contrib import admin
from comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'content_object', 'date_create')

admin.site.register(Comment, CommentAdmin)