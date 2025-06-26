from django.core.mail import send_mail

from .models import Mailing, MailingAttempt

from config.settings import EMAIL_HOST_USER

def send_mailing(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    recipients = list(mailing.recipients.values_list('email', flat=True)) # Список всех клиентов в данной рассылке
    subject = mailing.message.subject
    message = mailing.message.body
    if recipients:
        mailing.status = ("STARTED")
        mailing.save()
        try:
            result = send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=recipients, fail_silently=False)
            mailing_attempt = MailingAttempt(status='SUCCESS',
                                              server_response=f'Рассылка успешно завершена. Было отправлено {result} сообщений из {len(recipients)}.',
                                              mailing=mailing)
            mailing_attempt.save()
            mailing.status = ("FINISHED")
            mailing.save()
        except Exception as e:
            mailing_attempt = MailingAttempt(status='FAILED',
                                             server_response=f'Ошибка: {str(e)}',
                                             mailing=mailing)
            mailing_attempt.save()
    else:
        mailing_attempt = MailingAttempt(status='FAILED',
                                         server_response='В рассылке нет клиентов',
                                         mailing=mailing)
        mailing_attempt.save()

    return mailing_attempt