from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from django.conf import settings
from asgiref.sync import sync_to_async

from backend.config import TEXT_CONFIG

ENV = settings.ENV
router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    text = await sync_to_async(lambda: TEXT_CONFIG.HI_MSG)()
    await message.answer(text=text)
