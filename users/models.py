from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class TgUser(models.Model):
    """Класс Пользователей ТГ."""

    telegram_id = models.PositiveBigIntegerField(
        unique=True,
        verbose_name='Идентификатор Telegram',
        blank=True,
        null=True
    )
    username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Юзернейм телеграм'
    )
    first_last_name = models.CharField(
        max_length=255,
        verbose_name='ФИО'
    )
    phone_number = PhoneNumberField(verbose_name='Номер телефона',
                                    unique=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.first_last_name}'
