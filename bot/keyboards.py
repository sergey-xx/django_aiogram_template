from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_calendar import SimpleCalendarCallback
from aiogram_calendar.schemas import SimpleCalAct

from bot.callbacks import (CategoryTranslator, LevelCallbackData,
                           MenuCallbackData, TraumaCallbackData,
                           TypeCallbackData, FormCallbackData)
from bot.utils import get_day_training_list
from users.models import TgUser, TrainingFormat, TrainingType
from payments.models import PaymentMethod
from liveconfigs.config import BUTT_CONFIG


async def get_level_inline():
    markup = InlineKeyboardBuilder()
    for level in TgUser.Level:
        markup.button(text=level,
                      callback_data=LevelCallbackData(level=level).pack())
    markup.adjust(1)
    return markup.as_markup()


async def get_form_inline():
    markup = InlineKeyboardBuilder()
    for form in TrainingFormat:
        markup.button(text=form,
                      callback_data=FormCallbackData(form=form).pack())
    markup.adjust(1)
    return markup.as_markup()


async def get_type_inline():
    markup = InlineKeyboardBuilder()
    for training_type in TrainingType:
        markup.button(text=training_type,
                      callback_data=TypeCallbackData(training_type=training_type).pack())
    markup.adjust(1)
    return markup.as_markup()


async def get_skip_inline():
    markup = InlineKeyboardBuilder()
    markup.button(text=await BUTT_CONFIG.SKIP,
                  callback_data=TraumaCallbackData(skip=True).pack())
    return markup.as_markup()


async def get_phone_inline():
    button_contact = KeyboardButton(text=await BUTT_CONFIG.SEND_PHONE,
                                    request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_contact]],
                                   resize_keyboard=True)
    return keyboard


async def get_menu_inline():
    markup = InlineKeyboardBuilder()
    for category in MenuCallbackData.Category:
        markup.button(text=CategoryTranslator[category.value],
                      callback_data=MenuCallbackData(category=category,
                                                     action=MenuCallbackData.Action.root).pack())
    markup.adjust(1)
    return markup.as_markup()


async def get_card_inline(tg_user: TgUser):
    markup = InlineKeyboardBuilder()
    payment_method = await PaymentMethod.objects.filter(tg_user=tg_user).afirst()
    if not payment_method:
        markup.button(text=await BUTT_CONFIG.ADD_CARD,
                      callback_data=MenuCallbackData(category=MenuCallbackData.Category.profile,
                                                     action=MenuCallbackData.Action.card).pack())
    else:
        markup.button(text=await BUTT_CONFIG.DELETE_CARD,
                      callback_data=MenuCallbackData(category=MenuCallbackData.Category.profile,
                                                     action=MenuCallbackData.Action.delete).pack())
    markup.button(text=await BUTT_CONFIG.BACK,
                  callback_data=MenuCallbackData(menu_root=True).pack())
    markup.adjust(1)
    return markup.as_markup()


async def get_training_inline(date, training_id):
    markup = InlineKeyboardBuilder()
    markup.button(text=await BUTT_CONFIG.SIGNUP,
                  callback_data=MenuCallbackData(category=MenuCallbackData.Category.sign_up,
                                                 action=MenuCallbackData.Action.confirm,
                                                 id=training_id,
                                                 date=date).pack())
    markup.button(text=await BUTT_CONFIG.BACK,
                  callback_data=SimpleCalendarCallback(act=SimpleCalAct.day,
                                                       year=date.year,
                                                       month=date.month,
                                                       day=date.day).pack())
    markup.adjust(1)
    return markup.as_markup()


async def get_training_list_inline(date, tg_user: TgUser):
    markup = InlineKeyboardBuilder()
    trainings = await get_day_training_list(date=date,
                                            tg_user=tg_user)
    for training in trainings:
        markup.button(text=f'{training.title}',
                      callback_data=MenuCallbackData(category=MenuCallbackData.Category.sign_up,
                                                     action=MenuCallbackData.Action.get,
                                                     id=training.id,
                                                     date=date).pack())
    markup.button(text=await BUTT_CONFIG.BACK,
                  callback_data=MenuCallbackData(category=MenuCallbackData.Category.sign_up,
                                                 action=MenuCallbackData.Action.root).pack())
    markup.adjust(1)
    return markup.as_markup()


async def get_programs_inline():
    markup = InlineKeyboardBuilder()
    markup.button(text=await BUTT_CONFIG.BACK,
                  callback_data=MenuCallbackData(menu_root=True).pack())
    markup.adjust(1)
    return markup.as_markup()


async def get_support_inline():
    markup = InlineKeyboardBuilder()
    markup.button(text=await BUTT_CONFIG.CALL,
                  callback_data=MenuCallbackData(category=MenuCallbackData.Category.support,
                                                 action=MenuCallbackData.Action.call).pack())
    markup.button(text=await BUTT_CONFIG.TEXT,
                  callback_data=MenuCallbackData(category=MenuCallbackData.Category.support,
                                                 action=MenuCallbackData.Action.text).pack())
    markup.button(text=await BUTT_CONFIG.BACK,
                  callback_data=MenuCallbackData(menu_root=True).pack())
    markup.adjust(2)
    return markup.as_markup()


async def get_support_root_inline():
    markup = InlineKeyboardBuilder()
    markup.button(text=await BUTT_CONFIG.BACK,
                  callback_data=MenuCallbackData(category=MenuCallbackData.Category.support,
                                                 action=MenuCallbackData.Action.root).pack())
    markup.adjust(2)
    return markup.as_markup()


async def get_back_to_profile_inline(url):
    markup = InlineKeyboardBuilder()
    markup.button(text=await BUTT_CONFIG.PAY,
                  web_app=WebAppInfo(url=url))
    markup.button(text=await BUTT_CONFIG.BACK,
                  callback_data=MenuCallbackData(category=MenuCallbackData.Category.profile,
                                                 action=MenuCallbackData.Action.root).pack())
    markup.adjust(1)
    return markup.as_markup()


async def get_delete_card_confirm_inline():
    markup = InlineKeyboardBuilder()
    markup.button(text=await BUTT_CONFIG.YES,
                  callback_data=MenuCallbackData(category=MenuCallbackData.Category.profile,
                                                 action=MenuCallbackData.Action.confirm).pack())
    markup.button(text=await BUTT_CONFIG.NO,
                  callback_data=MenuCallbackData(category=MenuCallbackData.Category.profile,
                                                 action=MenuCallbackData.Action.root).pack())
    markup.adjust(2)
    return markup.as_markup()
