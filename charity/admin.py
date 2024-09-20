from django.contrib import admin
from .models import Tag, Article, Category, Volunteer
from django.contrib.admin import ModelAdmin


class ArticleAdmin(ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }


class TagAdmin(ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }


class CategoryAdmin(ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Volunteer)

