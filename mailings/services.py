import logging

from django.conf import settings
from django.core.mail import send_mail

from .models import Mailing, MailingAttempt

logger = logging.getLogger(__name__)


def send_mailing(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    recipients = list(mailing.recipients.values_list("email", flat=True))
    subject = mailing.message.subject
    message = mailing.message.body

    if not recipients:
        attempt = MailingAttempt.objects.create(
            status="FAILURE", server_response="В рассылке нет клиентов", mailing=mailing
        )
        return attempt

    mailing.status = "STARTED"
    mailing.save()

    try:
        result = send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipients,
            fail_silently=False,
        )
        attempt = MailingAttempt.objects.create(
            status="SUCCESS",
            server_response=f"Успешно отправлено {result} сообщений из {len(recipients)}.",
            mailing=mailing,
        )
        mailing.status = "FINISHED"
        mailing.save()
    except Exception as e:
        attempt = MailingAttempt.objects.create(
            status="FAILURE", server_response=f"Ошибка: {str(e)}", mailing=mailing
        )
        logger.exception(f"Ошибка при отправке рассылки {mailing_id}")
    return attempt
