from django.db import models

class Article(models.Model):
    """модель статьи блога"""

    title = models.CharField(max_length=150, verbose_name='Название')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(null=True, verbose_name="Изображение")
    views_count = models.IntegerField(default=0, verbose_name="Кол-во просмотров")

    created_at = models.DateTimeField(verbose_name='Дата/время публикации', auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'