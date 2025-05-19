from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class TgUser(models.Model):
    """Класс Пользователей ТГ."""

    tg_id = models.PositiveBigIntegerField(
        unique=True,
        verbose_name='Идентификатор Telegram',
    )
    username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Юзернейм телеграм'
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Фамилия'
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )
    is_admin = models.BooleanField(default=False)
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name='Номер телефона'
    )
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
        return f'{self.first_name} {self.last_name}/{self.tg_id}'
