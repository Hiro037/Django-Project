from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone

import logging
from datetime import datetime

from .services import send_mailing
from .models import Mailing
logger = logging.getLogger(__name__)



def check_mailings():
    logger.info(f"Фоновая задача запущена: {datetime.now()}")
    mailings = Mailing.objects.filter(status="CREATED", is_active=True)
    now = timezone.now()

    for mailing in mailings:
        if mailing.end_time <= now:
            mailing.status = "FINISHED"
            mailing.save()
            logger.info(f"Рассылка {mailing.id} завершена по времени")
            continue
        if mailing.start_time <= now:
            try:
                send_mailing(mailing_id=mailing.id)
            except Exception as e:
                logger.exception(f"Ошибка при отправке рассылки {mailing.id}: {e}")



def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(
        check_mailings,
        trigger="interval",
        minutes=10,
        id="test_job",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Запущен APScheduler.")
