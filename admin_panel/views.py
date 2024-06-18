from io import BytesIO

from aiogram import Bot
from aiogram.types import BufferedInputFile
from asgiref.sync import sync_to_async

from backend.settings import ENV
from users.models import TgUser
from bot.misc.mailing import send_message_mailing
from bot.utils import get_all_admins_id


async def get_file_id(file, file_type: str):

    if not file:
        return None

    if isinstance(file.file, BytesIO):
        file_input = BufferedInputFile(file.file.getvalue(), filename=file.name)
    else:
        bytes_file = BytesIO(file.read())
        file_input = BufferedInputFile(bytes_file.getvalue(), filename=file.name)

    bot = Bot(token=ENV('TG_TOKEN_BOT'), parse_mode='HTML')
    file_id = -1
    admins = await get_all_admins_id()

    if len(admins) != 0:
        if file_type == 'image':
            message = await bot.send_photo(chat_id=admins[0], photo=file_input)
            file_id = message.photo[-1].file_id
            await message.delete()
        elif file_type == "video":
            message = await bot.send_video(chat_id=admins[0], video=file_input)
            file_id = message.video.file_id
            await message.delete()
        else:
            message = await bot.send_document(chat_id=admins[0], document=file_input)
            file_id = message.document.file_id
            await message.delete()
    return file_id


async def mailing_django(media, text, file_id):
    users = await sync_to_async(TgUser.objects.all)()
    bot = Bot(token=ENV('TG_TOKEN_BOT'), parse_mode='HTML')
    count_send = 0
    async for user in users:
        args = [user.telegram_id]
        kwargs = {}
        if media in ['photo', 'video', 'document']:
            args.append(file_id)
            kwargs["caption"] = text
        else:
            args.append(text)
        status = await send_message_mailing(bot, media, args, kwargs)
        if status:
            count_send += 1
    return count_send
