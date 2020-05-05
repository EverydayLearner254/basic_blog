from django.contrib import admin
from .models import Author, Category, Post, Comment, PostView
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', 'text')


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)
# admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostView)
