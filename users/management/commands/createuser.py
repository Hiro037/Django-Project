from django.core.management import BaseCommand
from users.models import User

# Команда создает пользователя
class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User(email='user@example.com')
        user.set_password('qwerty')
        user.save()