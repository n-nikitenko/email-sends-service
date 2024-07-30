from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'preview', 'views_count', 'created_at')
    list_filter = ('views_count', 'created_at')
    search_fields = ('title', 'content',)
