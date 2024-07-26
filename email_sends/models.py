from django.db import models
from django.utils.datetime_safe import datetime

from users.models import User


class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name="ФИО")
    email = models.EmailField(unique=True, verbose_name="email")
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name="комментарий")
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Создатель")

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"


class Message(models.Model):
    theme = models.CharField(max_length=200, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Текст письма")
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Создатель")

    def __str__(self):
        return f"{self.theme}"

    class Meta:
        verbose_name = "сообщение для рассылки"
        verbose_name_plural = "сообщения для рассылки"


class MailingSettings(models.Model):
    EVERY_DAY = "EVERY_DAY"
    EVERY_WEEK = "EVERY_WEEK"
    EVERY_MONTH = "EVERY_MONTH"

    CREATED = "CREATED"
    FINISHED = "FINISHED"
    STARTED = "STARTED"

    MAILING_FREQUENCY_CHOICES = ((EVERY_DAY, "Раз в день"),
                                 (EVERY_WEEK, "Раз в неделю"),
                                 (EVERY_MONTH, "Раз в месяц"))

    MAILING_STATUS_CHOICES = ((CREATED, "Создана"),
                              (FINISHED, "Завершена"),
                              (STARTED, "Запущена"))

    name = models.CharField(max_length=200, verbose_name="Название рассылки")
    start_at = models.DateTimeField(default=datetime.now, verbose_name="Дата и время начала рассылки")
    stop_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время окончания рассылки")
    frequency = models.CharField(choices=MAILING_FREQUENCY_CHOICES, max_length=200,
                                 verbose_name="Периодичность рассылки", default=EVERY_DAY)
    status = models.CharField(choices=MAILING_STATUS_CHOICES, max_length=200, default=CREATED,
                              verbose_name="Статус рассылки")

    clients = models.ManyToManyField(Client, verbose_name="Клиенты", blank=True, related_name="mailing_settings", )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение для рассылки",
                                related_name="mailing_settings")

    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Создатель")

    def __str__(self):
        return (f"{self.name}. Тема: {self.message.theme}, периодичность "
                f"'{self.get_frequency_display()}'.")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ('can_change_status', 'может менять статус')
        ]
        ordering = ["id"]


class MailingLog(models.Model):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    MAILING_LOG_STATUS_CHOICES = ((SUCCESS, "Успешно"), (ERROR, "Ошибка"))

    last_sent = models.DateTimeField(auto_now_add=True, verbose_name="Дата/время последней попытки отправки")
    status = models.CharField(choices=MAILING_LOG_STATUS_CHOICES, max_length=200, verbose_name="Статус отправки")
    server_response = models.TextField(null=True, blank=True, verbose_name="Ответ почтового сервера")
    mailing = models.OneToOneField(MailingSettings, on_delete=models.CASCADE, verbose_name="Рассылка",
                                related_name="mailing_log")

    def __str__(self):
        return (f"{self.mailing.name}. Статус: {self.get_status_diplay()}. "
                f"Дата/время последней попытки отправки: {self.last_sent}")

    class Meta:
        verbose_name = "Лог рассылки"
        verbose_name_plural = "Логи рассылки"
