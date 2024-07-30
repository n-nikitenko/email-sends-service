from django.core.cache import cache

from blog.models import Article
from config import settings


def get_last_three_articles():
    """Возвращает последние три статьи из кеша, если включен, или из БД"""

    key = 'last_articles'
    if settings.CACHE_ENABLED:
        last_articles = cache.get(key)
        if last_articles is not None:
            return last_articles

    ordered_articles = Article.objects.order_by("-created_at")
    if ordered_articles.count() >= 3:
        ret = ordered_articles[:3]
    else:
        ret = ordered_articles
    if settings.CACHE_ENABLED:
        cache.set(key, ret)
    return ret
