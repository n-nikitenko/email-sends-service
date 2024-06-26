from django.core.management import BaseCommand

from email_sends.services import process_mailings


class Command(BaseCommand):

    def handle(self, *args, **options):
        process_mailings()
