from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Author, Article


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['nickname']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['headline', 'author', 'get_html_photo']
    prepopulated_fields = {'slug': ('headline',)}
    fields = ('headline', 'photo', 'slug', 'author', 'date_create')
    readonly_fields = ('date_create',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'Фото'
