from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from mailings.models import Mailing, Message, Recipient
from users.models import User


class Command(BaseCommand):
    help = "Создает пользователя-модератора с нужными правами"

    def handle(self, *args, **options):
        email = "manager@example.com"
        password = "qwerty"
        group_name = "Менеджеры"

        # Создание или получение пользователя
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_password(password)
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Пользователь {email} создан."))
        else:
            self.stdout.write(
                self.style.WARNING(f"Пользователь {email} уже существует.")
            )

        # Получаем или создаем группу
        group, _ = Group.objects.get_or_create(name=group_name)

        # Получаем права
        try:
            ct_recipient = ContentType.objects.get_for_model(Recipient)
            view_all_recipients_perm = Permission.objects.get(
                codename="can_view_all_recipients", content_type=ct_recipient
            )
            ct_message = ContentType.objects.get_for_model(Message)
            view_all_messages_perm = Permission.objects.get(
                codename="can_view_all_messages", content_type=ct_message
            )
            ct_mailing = ContentType.objects.get_for_model(Mailing)
            view_all_mailings_perm = Permission.objects.get(
                codename="can_view_all_mailings", content_type=ct_mailing
            )
            disable_mailings_perm = Permission.objects.get(
                codename="can_disable_mailings", content_type=ct_mailing
            )
            ct_user = ContentType.objects.get_for_model(User)
            see_all_users_perm = Permission.objects.get(
                codename="can_see_all_users", content_type=ct_user
            )
            deactivate_users_perm = Permission.objects.get(
                codename="can_deactivate_users", content_type=ct_user
            )
        except Permission.DoesNotExist as e:
            self.stderr.write(self.style.ERROR(f"Ошибка: {e}"))
            return

        # Добавляем права группе
        group.permissions.add(
            view_all_recipients_perm,
            view_all_messages_perm,
            view_all_mailings_perm,
            disable_mailings_perm,
            see_all_users_perm,
            deactivate_users_perm,
        )

        # Добавляем пользователя в группу
        user.groups.add(group)

        self.stdout.write(
            self.style.SUCCESS(
                f'Пользователь {email} добавлен в группу "{group_name}" с нужными правами.'
            )
        )
