# Generated by Django 4.2.13 on 2024-07-30 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email_sends', '0008_alter_mailingsettings_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailingsettings',
            options={'ordering': ['id'], 'permissions': [('can_change_status', 'может менять статус')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]
