# Generated by Django 4.2.13 on 2024-06-25 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_sends', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='комментарий'),
        ),
    ]
