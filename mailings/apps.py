import os

from django.apps import AppConfig


class MailingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailings"

    def ready(self):
        from .scheduler import start

        if os.getenv("RUN_MAIN") == "true":
            start()
