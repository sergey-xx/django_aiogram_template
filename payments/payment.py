import logging
import uuid

from asgiref.sync import sync_to_async
from django.conf import settings
from yookassa import Configuration, Payment
from yookassa.domain.response import PaymentResponse

from bot.utils import (get_need_to_repeat_users,
                       get_waiting_for_capture_paiments)
from liveconfigs.config import PAY_CONFIG
from payments.models import Payment as DBPayment
from payments.models import PaymentMethod
from users.models import TgUser

logger = logging.getLogger('Import')


SHOP_ID = settings.ENV.str('SHOP_ID')
API_KEY = settings.ENV.str('API_KEY')
BOT_URL = settings.ENV.str('BOT_URL')

Configuration.account_id = SHOP_ID
Configuration.secret_key = API_KEY


def create_repeated_payment(value: float, tg_user: TgUser, payment_method_id):
    idempotence_key = str(uuid.uuid4())
    data = {
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "capture": True,
        "metadata": {
            "user_id": str(tg_user.id),
            "subscription_type": "monthly"
        },
        "description": f"Оплата подписки пользователем {tg_user.id} {tg_user.first_last_name}",
        'payment_method_id': payment_method_id
    }
    payment = Payment.create(data, idempotence_key)
    return payment.id


def create_payment(value: float, tg_user: TgUser):
    idempotence_key = str(uuid.uuid4())
    data = {
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "capture": True,
        "metadata": {
            "user_id": str(tg_user.id),
            "subscription_type": "monthly"
        },
        "description": f"Оплата подписки пользователем {tg_user.id} {tg_user.first_last_name}",
        "save_payment_method": True,
        "payment_method_data": {
            "type": "bank_card"},
        "confirmation": {
            "type": "redirect",
            "return_url": BOT_URL
        },
    }
    payment = Payment.create(data, idempotence_key)

    confirmation_url = payment.confirmation.confirmation_url
    payment_id = payment.id
    return confirmation_url, payment_id


def get_payment(payment_id: str) -> PaymentResponse:
    payment = Payment.find_one(payment_id)
    return payment


async def update_payments():
    payments = await get_waiting_for_capture_paiments()
    logger.info(f'Начало обновления платежей. Количество: {len(payments)}')
    for payment in payments:
        await sync_to_async(update_payment)(payment.id)


def update_payment(payment_id: str):
    db_payment = DBPayment.objects.filter(id=payment_id).first()
    if db_payment:
        logger.info(f'Обновляем Платеж: {db_payment}')
        payment = get_payment(str(payment_id))
        logger.info(f'Получен платеж: {payment.id}')
        if payment.status == 'canceled':
            logger.info(f'Платеж {payment.id} был отменен и удален из БД')
            db_payment.delete()
        else:
            db_payment.created_at = payment.created_at
            db_payment.status = payment.status
            db_payment.paid = payment.paid
            db_payment.amount = payment.amount.value
            db_payment.currency = payment.amount.currency
            db_payment.description = payment.description
            db_payment.save()
        db_payment_method = PaymentMethod.objects.filter(tg_user=db_payment.tg_user,
                                                         id=payment.payment_method.id).first()
        if not db_payment_method:
            db_payment_method = PaymentMethod.objects.filter(
                tg_user=db_payment.tg_user).first()
            if db_payment_method:
                db_payment_method.delete()
            if payment.payment_method and payment.payment_method.card:
                db_payment_method = PaymentMethod(
                    id=payment.payment_method.id,
                    saved=payment.payment_method.saved,
                    title=payment.payment_method.title,
                    payment_type=payment.payment_method.type,
                    card_first6=payment.payment_method.card.first6,
                    card_last4=payment.payment_method.card.last4,
                    expiry_year=payment.payment_method.card.expiry_year,
                    expiry_month=payment.payment_method.card.expiry_month,
                    card_type=payment.payment_method.card.card_type,
                    tg_user=db_payment.tg_user)
                db_payment_method.save()


async def repeat_payments():
    tg_users = await get_need_to_repeat_users(days=await PAY_CONFIG.PAYMENT_PERIOD)
    logger.info(f'Платеж повторяем для количества: {len(tg_users)}')
    for tg_user in tg_users:
        logger.info(f'Платеж повторяем для: {tg_user}')
        payment_id = create_repeated_payment(value=await PAY_CONFIG.PRICE,
                                             tg_user=tg_user,
                                             payment_method_id=str(tg_user.payment_method.id))
        payment = get_payment(payment_id)
        db_payment = DBPayment(
            id=payment.id,
            tg_user=tg_user,
            created_at=payment.created_at,
            status=payment.status,
            paid=payment.paid,
            amount=payment.amount.value,
            currency=payment.amount.currency,
            description=payment.description, )
        await db_payment.asave()
        logger.info(f'Платеж для пользователя {tg_user} успешно повторен')
