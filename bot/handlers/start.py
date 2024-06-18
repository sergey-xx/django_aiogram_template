from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from django.conf import settings

import bot.keyboards as kb
from liveconfigs.config import TEXT_CONFIG
from users.models import TgUser

ENV = settings.ENV
router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    db_user = await TgUser.objects.filter(telegram_id=message.from_user.id).afirst()
    await message.answer(text=await TEXT_CONFIG.HI_MSG)
    if not db_user:
        await message.answer(text=await TEXT_CONFIG.FIO_MSG,)
        await state.set_state(UserState.username)
    else:
        await message.answer(text=await TEXT_CONFIG.MENU_MSG,
                             reply_markup=await kb.get_menu_inline())
