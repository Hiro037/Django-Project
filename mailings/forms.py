from django.forms import DateTimeInput, ModelForm

from .models import Mailing, Message, Recipient


class RecipientForm(ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "comment"]

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)

        # Настройка атрибутов виджета для поля 'email'
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "email клиента",  # Текст подсказки внутри поля
            }
        )

        # Настройка атрибутов виджета для поля 'full_name'
        self.fields["full_name"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "ФИО клиента",  # Текст подсказки внутри поля
                "type": "text",
            }
        )

        # Настройка атрибутов виджета для поля 'comment'
        self.fields["comment"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Комментарий",  # Текст подсказки внутри поля
                "type": "text",
            }
        )


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        # Настройка атрибутов виджета для поля 'subject'
        self.fields["subject"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Тема сообщения",  # Текст подсказки внутри поля
            }
        )

        # Настройка атрибутов виджета для поля 'body'
        self.fields["body"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Тело сообщения",  # Текст подсказки внутри поля
                "type": "text",
            }
        )


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "recipients"]
        widgets = {
            "start_time": DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": DateTimeInput(attrs={"type": "datetime-local"}),
        }
