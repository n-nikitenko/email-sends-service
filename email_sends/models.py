from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name="ФИО")
    email = models.EmailField(unique=True, verbose_name="email")
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name="комментарий")

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
