from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """команда создания суперпользователя"""

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email адрес')
        parser.add_argument('--password', type=str, help='Пароль')

    def handle(self, *args, **options):
        """Создание суперпользователя:
        python manage.py createadmin --email admin@example.com --password admin"""

        email = options.get('email', )
        password = options.get('password', 'admin')
        user = User.objects.create(email=email if email is not None else 'admin@example.com')
        user.set_password(password if password is not None else 'admin')
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
