from typing import Iterable
from django.db import models
from django.utils import timezone
from datetime import datetime

from users.models import TgUser


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, verbose_name='ID')
    tg_user = models.ForeignKey(TgUser,
                                on_delete=models.PROTECT,
                                verbose_name='Пользователь телеграм',
                                related_name='payment')
    status = models.CharField(max_length=20, verbose_name='Статус')
    paid = models.BooleanField()
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Размер платежа')
    currency = models.CharField(max_length=4, verbose_name='Валюта')
    description = models.CharField(max_length=100, verbose_name='Описание')
    confirm_url = models.URLField(verbose_name='Ссылка на Юкассу')
    created_at = models.DateTimeField()
    paid_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs) -> None:
        if self.paid and not self.paid_at:
            self.paid_at = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'id: {self.id} Пользователь: {self.tg_user}'


class PaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, verbose_name='ID')
    payment_type = models.CharField(max_length=50, verbose_name='Тип')
    saved = models.BooleanField()
    title = models.CharField(max_length=100, verbose_name='Название платежного метода')
    card_first6 = models.CharField(max_length=6, verbose_name='Первые 6 цифр карты')
    card_last4 = models.CharField(max_length=6, verbose_name='Последние 4 цифры карты')
    expiry_year = models.CharField(max_length=4, verbose_name='Год экспирации')
    expiry_month = models.CharField(max_length=2, verbose_name='Месяц экспирации')
    card_type = models.CharField(max_length=50, verbose_name='Тип карты')
    tg_user = models.OneToOneField(TgUser,
                                   on_delete=models.CASCADE,
                                   verbose_name='Пользователь телеграм',
                                   related_name='payment_method')

    class Meta:
        verbose_name = 'Платежный метод'
        verbose_name_plural = 'Платежные методы'

    def __str__(self):
        return f'Пользователь: {self.tg_user}/{self.card_first6}******{self.card_last4}'
