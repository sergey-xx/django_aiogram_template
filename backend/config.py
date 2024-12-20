import logging
from enum import Enum

from django.conf import settings
from liveconfigs.models import BaseConfig

logger = logging.getLogger()

DESCRIPTION_SUFFIX = "_DESCRIPTION"
TAGS_SUFFIX = "_TAGS"
VALIDATORS_SUFFIX = "_VALIDATORS"


class ConfigTags(str, Enum):
    urls = "Ссылки"
    payment = "Платежи"
    basic = "Основные"
    other = "Прочее"
    text = "Тексты"


class URL_CONFIG(BaseConfig):
    __topic__ = 'Настройки ссылок'

    __exported__ = [
        'DAYS',
        'FIRST_DAY_OF_WEEK',
        'TYPES_OF_LOADING',
        'USE_CALENDAR',
        'CONSOLIDATION_GROUPS',
    ]

    SITE_LINK: str = 'https://www.python.org/'
    SITE_LINK_DESCRIPTION = "Настройка ссылки на сайт"
    SITE_LINK_TAGS = [ConfigTags.urls]

    BOT_URL = settings.ENV.str('BOT_URL')
    BOT_LINK_DESCRIPTION = "Настройка ссылки на этот бот"
    BOT_LINK_LINK_TAGS = [ConfigTags.urls]


class TEXT_CONFIG(BaseConfig):
    __topic__ = 'Настройки текстов'

    HI_MSG: str = 'Рады приветствовать вас!'
    HI_MSG_DESCRIPTION = "Приветственное сообщение"
    HI_MSG_TAGS = [ConfigTags.text]


class BUTT_CONFIG(BaseConfig):
    __topic__ = 'Настройки текстов кнопок'

    BACK: str = 'Назад'
    BACK_DESCRIPTION = "Текст кнопки Назад"
    BACK_TAGS = [ConfigTags.text]
