import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator
from django.conf import settings
from django.core.management import BaseCommand

from bot.commands import set_commands
from bot.handlers import start_router
from bot.misc.logging import configure_logger
from bot.misc.mailing import start_mailing

ENV = settings.ENV
REDIS_HOST = ENV.str('REDIS_HOST')
REDIS_PORT = ENV.str('REDIS_PORT')


async def on_startup(bot: Bot):
    await set_commands(bot)
    configure_logger(True)


async def main():
    logger = logging.getLogger('Tg')
    logger.info("Starting bot")

    bot = Bot(ENV.str('TG_TOKEN_BOT'))

    storage = RedisStorage.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}/0')

    dp = Dispatcher(storage=storage)
    dp.include_routers(start_router,)

    jobstores = {
        'default': RedisJobStore(
            host=ENV('REDIS_HOST'),
            port=ENV('REDIS_PORT')
        )
    }

    scheduler = ContextSchedulerDecorator(
        AsyncIOScheduler(
            timezone="Europe/Moscow",
            jobstores=jobstores
        )
    )

    scheduler.ctx.add_instance(bot, declared_class=Bot)

    scheduler.add_job(
        start_mailing,
        'interval',
        minutes=ENV.int('MAILING_PERIOD', 1),
        replace_existing=True,
        id='mailing'
    )

    # scheduler.start()
    # scheduler.print_jobs()

    try:
        await on_startup(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except TelegramNetworkError:
        logging.critical('Нет интернета')


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            pass
