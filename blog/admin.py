from django.contrib import admin
from .models import Post
from .models import Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'published_date', 'author_id', 'cat_id')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
