from django.core.exceptions import ValidationError
from django.db import models


class Mailing(models.Model):

    text = models.TextField(
        max_length=4096,
        help_text='Текст рассылки',
        verbose_name='Текст',
        blank=True,
        null=True,
    )

    date_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Дата/время рассылки',
        verbose_name='Дата/время',
    )
    is_sent = models.BooleanField(
        help_text='Статус отправки',
        verbose_name='Статус отправки',
        default=False
    )

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        abstract = True

    def clean(self) -> None:
        if self.date_time and not self.id:
            raise ValidationError('Сперва сохраните объект, а потом поставьте дату рассылки')
        if self.id:
            all_types = set([attachment.file_type for attachment in self.attachments.all()])
            if Attachment.FileType.DOCUMENT in all_types and len(all_types) > 1:
                raise ValidationError('Нельзя совмещать в рассылке документы и другие типы')
            if self.attachments.exists() and len(self.text) > 1024:
                raise ValidationError(f'Текст слишком длинный для отправки с вложениями ({len(self.text)} из 1024)')
        return super().clean()


class Attachment(models.Model):

    class FileType(models.TextChoices):
        PHOTO = "photo", 'Фото'
        VIDEO = "video", 'Видео'
        DOCUMENT = "document", 'Документ'

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attachments', verbose_name='Рассылка')
    file_type = models.CharField(max_length=10, choices=FileType, verbose_name='Тип вложения')
    file = models.FileField(verbose_name='Прикрепленный файл/видео/картинка')
    file_id = models.CharField(
        max_length=255,
        help_text='Оставьте пустым. Для обновления медиа-удалите.',
        verbose_name='File ID',
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs) -> None:
        all_types = set([attachment.file_type for attachment in self.mailing.attachments.all()])
        if (
            Attachment.FileType.DOCUMENT in all_types and self.file_type != Attachment.FileType.DOCUMENT
            or Attachment.FileType.PHOTO in all_types and self.file_type == Attachment.FileType.DOCUMENT
            or Attachment.FileType.VIDEO in all_types and self.file_type == Attachment.FileType.DOCUMENT
        ):
            raise ValidationError('Нельзя совмещать в рассылке документы и другие типы')
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'
        abstract = True
