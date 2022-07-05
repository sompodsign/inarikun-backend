from django.contrib import admin

# Register your models here.
from django.contrib.admin.options import InlineModelAdmin

from blog.models import Category, Topic, Article, ArticleTag, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']
    fields = ['name']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['name', 'category']
    search_fields = ['name', 'category']
    ordering = ['name']
    fields = ['name', 'category']
    readonly_fields = ['name', 'category']


class ArticleTagInline(InlineModelAdmin):
    model = ArticleTag
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'topic']
    list_filter = ['title', 'author', 'topic']
    search_fields = ['title', 'author', 'topic']
    ordering = ['title']
    fields = ['title', 'content', 'author', 'topic']


@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'body']
