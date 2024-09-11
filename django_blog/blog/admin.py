from django.contrib import admin
from .models import Post, Comment, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    filter_horizontal = ('tags',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)