# Generated by Django 4.2.13 on 2024-07-30 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('content', models.TextField(verbose_name='Содержимое')),
                ('preview', models.ImageField(null=True, upload_to='', verbose_name='Изображение')),
                ('views_count', models.IntegerField(default=0, verbose_name='Кол-во просмотров')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата/время публикации')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]
