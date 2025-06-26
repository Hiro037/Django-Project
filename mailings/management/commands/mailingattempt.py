from django.core.management import BaseCommand
from mailings.services import send_mailing

# Команда создает попытку рассылки
class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) < 1:
            raise ValueError("Не указан mailing_id")
        mailing_id = args[0]
        send_mailing(mailing_id=mailing_id)