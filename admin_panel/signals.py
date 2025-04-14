from aiogram import Bot
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from admin_panel.models import Attachment, Mailing
from backend.config import URL_CONFIG
from aiogram.types import BufferedInputFile
from io import BytesIO


async def send_file(file, file_type: str):
    file_id = -1
    async with Bot(settings.ENV.str('TG_TOKEN_BOT')) as bot:
        if isinstance(file.file, BytesIO):
            file_input = BufferedInputFile(file.file.getvalue(), filename=file.name)
        else:
            bytes_file = BytesIO(file.read())
            file_input = BufferedInputFile(bytes_file.getvalue(), filename=file.name)
        if file_type == Attachment.FileType.PHOTO:
            message = await bot.send_photo(await URL_CONFIG.UC_ADMIN_ID, photo=file_input)
            file_id = message.photo[-1].file_id
            await message.delete()
        elif file_type == Attachment.FileType.VIDEO:
            message = await bot.send_video(await URL_CONFIG.UC_ADMIN_ID, video=file_input)
            file_id = message.video.file_id
            await message.delete()
        elif file_type == Attachment.FileType.DOCUMENT:
            message = await bot.send_document(await URL_CONFIG.UC_ADMIN_ID, document=file_input)
            file_id = message.document.file_id
            await message.delete()
    return file_id


@receiver(post_save, sender=Attachment)
def preload_file(sender, instance: Attachment, created, **kwargs):
    if not instance.file_id:
        instance.file_id = async_to_sync(send_file)(file=instance.file, file_type=instance.file_type)
        instance.save()


@receiver(post_save, sender=Mailing)
def validate_att(sender, instance: Mailing, created, **kwargs):
    if instance.date_time:
        all_types = set([attachment.file_type for attachment in instance.attachments.all()])
        if Attachment.FileType.DOCUMENT in all_types and len(all_types) > 1:
            instance.date_time = None
            instance.save()
