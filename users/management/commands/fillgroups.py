import os

from django.contrib.auth.models import Group
from django.core import management
from django.core.management import BaseCommand
from django.core.management.commands import loaddata

from config.settings import BASE_DIR


class Command(BaseCommand):
    path: str

    def __init__(self):
        super().__init__()
        self.path = os.path.join(BASE_DIR, "fixtures", "groups.json")

    def handle(self, *args, **options):
        """Заполнение групп из фикстур"""

        Group.objects.all().delete()

        management.call_command(loaddata.Command(), self.path, verbosity=0)
