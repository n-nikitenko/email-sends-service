from django.views.generic import DetailView

from blog.models import Article


class ArticleDetailView(DetailView):
    """представление для статьи блога"""
    model = Article

    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        article.views_count += 1
        article.save()
        return article
