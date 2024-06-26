from smtplib import SMTPSenderRefused

from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from email_sends.models import MailingSettings, MailingLog


def send_mailing(mailing: MailingSettings):
    """Отправить рассылку, если она не завершена и записать результат отправки в лог.
    Также обновить статус при необходимости"""

    def create_or_update_mailing_log(mailing: MailingSettings, status):
        """Создать или обновить лог рассылки"""

        try:
            mailing_log = mailing.mailing_log
        except MailingLog.DoesNotExist:
            mailing_log = None

        if mailing_log:
            mailing_log.status = status
            mailing_log.save()
        else:
            MailingLog.objects.create(mailing=mailing, status=status)
        return mailing.mailing_log

    if mailing.status == MailingSettings.CREATED:
        mailing.status = MailingSettings.STARTED
        mailing.save()
    elif mailing.status == MailingSettings.FINISHED:
        return

    recipient_list = [client.email for client in mailing.clients.all()]
    try:
        send_mail(
            mailing.message.theme,
            mailing.message.body,
            EMAIL_HOST_USER,
            recipient_list,
            fail_silently=False, )
        create_or_update_mailing_log(mailing=mailing, status=MailingLog.SUCCESS)
    except SMTPSenderRefused as e:
        log = create_or_update_mailing_log(mailing=mailing, status=MailingLog.ERROR)
        log.server_response = str(e)
        log.save()


def process_mailings():
    """выбирает все незавершенные рассылки со временем начала не больше текущего и для каждой
    1. если подошло время завершения рассылки - она останавливается,
    2. если рассылка еще ни разу не отправлена - она отправляется,
    3. если прошел указанный период отправки рассылки - она отправляется"""

    mailings = MailingSettings.objects.filter(
        status__in={MailingSettings.CREATED, MailingSettings.STARTED}, start_at__lte=timezone.now())
    frequency_to_days = {MailingSettings.EVERY_DAY: 1, MailingSettings.EVERY_WEEK: 7,
                         MailingSettings.EVERY_MONTH: 30}
    for mailing in mailings:
        now = timezone.now()
        if mailing.stop_at:
            if now >= mailing.stop_at:
                # остановить рассылку
                mailing.status = MailingSettings.FINISHED
                mailing.save()
                break

        try:
            mailing_log = mailing.mailing_log
        except MailingLog.DoesNotExist:
            mailing_log = None

        if mailing_log:
            if mailing_log.status == MailingLog.SUCCESS:
                delta = now - mailing_log.last_sent
                if delta.days >= frequency_to_days[mailing.frequency]:  # пора повторить отправку
                    send_mailing(mailing)
            else:  # повторить отправку
                send_mailing(mailing)
        else:  # первая попытка отправки
            send_mailing(mailing)
