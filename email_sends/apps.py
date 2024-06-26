from time import sleep

from django.apps import AppConfig
from django.core.management import call_command


class EmailSendsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'email_sends'
    verbose_name = 'Рассылки'

    def ready(self):
        super(EmailSendsConfig, self).ready()
        sleep(2)
        call_command('crontab', 'add')

