from datetime import datetime

import pytz
from asgiref.sync import sync_to_async
from django.db.models import Model, Q

from admin_panel.models import Mailing
from backend import settings
from users.models import TgUser


@sync_to_async
def get_all_objects(Model):
    return list(Model.objects.all())


@sync_to_async
def get_all_users():
    return list(TgUser.objects.filter(tg_id__isnull=False))


@sync_to_async
def get_all_maling() -> list:
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    return list(Mailing.objects.filter(is_sent=False, date_malling__lte=now))


def convert_date(date_str: str):
    date_obj = datetime.strptime(date_str, '%d.%m.%Y')
    return date_obj


def convert_time(time_str: str):
    date_obj = datetime.strptime(time_str, '%H:%M')
    return date_obj


def joint_convert_datetime(date_str: str, time_str: str):
    datetime_str = ' '.join([date_str, time_str])
    datetime_obj = datetime.strptime(datetime_str, '%d.%m.%Y %H:%M')
    datetime_obj = pytz.timezone(settings.TIME_ZONE).localize(datetime_obj)
    return datetime_obj


@sync_to_async
def get_all_admins_id() -> list:
    return list(TgUser.objects
                .filter(tg_id__isnull=False)
                .filter(is_admin=True)
                .values_list('tg_id', flat=True))


def get_verbose_fields_info(obj, splitter: str = '\n', max_field_length: int = 20):
    fields_info = []
    fields = obj._meta.get_fields(include_parents=False,
                                  include_hidden=False)
    for field in fields:
        try:
            verbose_name = field.verbose_name[:max_field_length]
            value = getattr(obj, field.name, None)
            value_str = str(value) if value is not None else "----"
            fields_info.append(f"{verbose_name}: {value_str[:max_field_length]}")
        except AttributeError:
            pass
    return splitter.join(fields_info)


@sync_to_async
def get_user_permisssion(tg_id):
    if TgUser.objects.filter(tg_id=tg_id):
        return True
    return False


@sync_to_async
def get_admin_permisssion(tg_id):
    if TgUser.objects.filter(telegram_id=tg_id).filter(is_admin=True):
        return True
    return False


@sync_to_async
def get_filtered_objects(Model: Model,
                         **kwargs):
    query = Q()
    for key, value in kwargs.items():
        query &= Q(**{key: value})
    return list(Model.objects.filter(query))
