from django.core.management.base import BaseCommand
from mailings.scheduler import start

class Command(BaseCommand):
    help = "Run APScheduler"

    def handle(self, *args, **options):
        self.stdout.write("Starting scheduler...")
        start()