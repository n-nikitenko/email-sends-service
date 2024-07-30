from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
]
