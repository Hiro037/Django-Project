from django.db import models


class Recipient(models.Model):
    # Получатель рассылки
    email = models.EmailField(
        unique=True,
        verbose_name="email",
        help_text="Электронная почта получателя рассылки",
    )
    full_name = models.CharField(
        verbose_name="ФИО", help_text="ФИО получателя рассылки"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    owner = models.ForeignKey(
        to="users.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель рассылки (клиент)"
        verbose_name_plural = "Получатели рассылки (клиенты)"
        permissions = [
            ("can_view_all_recipients", "Может просматривать всех получателей рассылок")
        ]


class Message(models.Model):
    # Сообщение
    subject = models.CharField(verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма", null=True, blank=True)
    owner = models.ForeignKey(
        to="users.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [("can_view_all_messages", "Может просматривать все сообщения")]


class Mailing(models.Model):
    # Рассылка
    start_time = models.DateTimeField(verbose_name="Начало рассылки")
    end_time = models.DateTimeField(verbose_name="Окончание рассылки")
    status = models.CharField(
        choices=[
            ("CREATED", "Создана"),
            ("FINISHED", "Завершена"),
            ("STARTED", "Запущена"),
        ],
        verbose_name="Статус рассылки",
    )
    message = models.ForeignKey(to="Message", on_delete=models.CASCADE)
    recipients = models.ManyToManyField(
        to="Recipient", verbose_name="Получатель рассылки"
    )
    owner = models.ForeignKey(
        to="users.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_view_all_mailings", "Может просматривать все рассылки"),
            ("can_disable_mailings", "Может отключать чужие рассылки"),
        ]


class MailingAttempt(models.Model):
    # Попытка рассылки
    timestamp = models.DateTimeField(auto_now_add=True)  # Дата и время попытки
    status = models.CharField(
        choices=[("SUCCESS", "Успешно"), ("FAILURE", "Не успешно")],
        verbose_name="Статус попытки рассылки",
    )
    server_response = models.TextField(verbose_name="Ответ сервера")
    mailing = models.ForeignKey(
        to="Mailing", on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
