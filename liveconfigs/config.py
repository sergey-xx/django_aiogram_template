from enum import Enum

from liveconfigs import models

from django.conf import settings


class ConfigTags(str, Enum):
    urls = "Ссылки"
    payment = "Платежи"
    basic = "Основные"
    other = "Прочее"
    text = "Тексты"


class URL_CONFIG(models.BaseConfig):
    __topic__ = 'Настройки ссылок'

    __exported__ = [
        'DAYS',
        'FIRST_DAY_OF_WEEK',
        'TYPES_OF_LOADING',
        'USE_CALENDAR',
        'CONSOLIDATION_GROUPS',
    ]

    BOT_URL = settings.ENV.str('BOT_URL')
    BOT_LINK_DESCRIPTION = "Настройка ссылки на этот бот"
    BOT_LINK_LINK_TAGS = [ConfigTags.urls]


class PAY_CONFIG(models.BaseConfig):
    __topic__ = 'Настройки платежей'

    __exported__ = [
        'DAYS',
        'FIRST_DAY_OF_WEEK',
        'TYPES_OF_LOADING',
        'USE_CALENDAR',
        'CONSOLIDATION_GROUPS',
    ]

    PRICE: float = 100.02
    PRICE_DESCRIPTION = "Настройка величины платежа (руб.)"
    PRICE_TAGS = [ConfigTags.payment]

    PAYMENT_PERIOD: int = 30
    PAYMENT_PERIOD_DESCRIPTION = "Настройка периода платежа (дней)"
    PAYMENT_PERIOD_TAGS = [ConfigTags.payment]

    PAYMENT_BLOCK_PERIOD: int = 37
    PAYMENT_BLOCK_PERIOD_DESCRIPTION = "Настройка периода блокировки после последнего платежа (дней)"
    PAYMENT_BLOCK_PERIOD_TAGS = [ConfigTags.payment]

    TRIAL_PERIOD: int = 7
    TRIAL_BLOCK_PERIOD_DESCRIPTION = "Настройка пробного периода (дней)"
    TRIAL_BLOCK_PERIOD_TAGS = [ConfigTags.payment]


class TEXT_CONFIG(models.BaseConfig):
    __topic__ = 'Настройки текстов'

    HI_MSG: str = 'Рады приветствовать вас!'
    HI_MSG_DESCRIPTION = "Приветственное сообщение"
    HI_MSG_TAGS = [ConfigTags.text]



class BUTT_CONFIG(models.BaseConfig):
    __topic__ = 'Настройки текстов кнопок'

    BACK: str = 'Назад'
    BACK_DESCRIPTION = "Текст кнопки Назад"
    BACK_TAGS = [ConfigTags.text]

    SKIP: str = 'Пропустить'
    SKIP_DESCRIPTION = "Текст кнопки Пропустить"
    SKIP_TAGS = [ConfigTags.text]

    SKIP: str = 'Пропустить'
    SKIP_DESCRIPTION = "Текст кнопки Пропустить"
    SKIP_TAGS = [ConfigTags.text]

    SEND_PHONE: str = 'Отправить номер телефона'
    SEND_PHONE_DESCRIPTION = "Текст кнопки Отправить номер телефона"
    SEND_PHONE_TAGS = [ConfigTags.text]

    ADD_CARD: str = 'Привязать карту'
    ADD_CARD_DESCRIPTION = "Текст кнопки Привязать карту"
    ADD_CARD_TAGS = [ConfigTags.text]

    DELETE_CARD: str = 'Отвязать карту'
    DELETE_CARD_DESCRIPTION = "Текст кнопки Отвязать карту"
    DELETE_CARD_TAGS = [ConfigTags.text]

    SIGNUP: str = 'Получить тренировку'
    SIGNUP_DESCRIPTION = 'Получить тренировку'
    SIGNUP_TAGS = [ConfigTags.text]

    TEXT: str = 'Написать'
    TEXT_DESCRIPTION = 'Написать'
    TEXT_TAGS = [ConfigTags.text]

    CALL: str = 'Позвонить'
    CALL_DESCRIPTION = 'Позвонить'
    CALL_TAGS = [ConfigTags.text]

    YES: str = 'Да'
    YES_DESCRIPTION = 'Текст кнопки Да'
    YES_TAGS = [ConfigTags.text]

    NO: str = 'Нет'
    NO_DESCRIPTION = 'Текст кнопки Нет'
    NO_TAGS = [ConfigTags.text]

    PAY: str = 'Оплатить'
    PAY_DESCRIPTION = 'Текст кнопки перехода на Юкассу'
    PAY_TAGS = [ConfigTags.text]
