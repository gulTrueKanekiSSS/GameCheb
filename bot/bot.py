import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from django.conf import settings
from asgiref.sync import sync_to_async

from .handlers_core import cmd_start, handle_contact, get_quest, my_promocodes, handle_photo
from core.models import User, Quest, UserQuestProgress
from bot import admin_commands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен из settings
token = settings.TELEGRAM_BOT_TOKEN
bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Регистрируем административные команды
dp.message.register(admin_commands.handle_approve, Command("approve"))
dp.message.register(admin_commands.handle_reject, Command("reject"))

# ... все хендлеры как есть ...

async def start_bot():
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(handle_contact, lambda msg: msg.contact is not None)
    dp.message.register(get_quest, lambda msg: msg.text == "🎯 Получить квест")
    dp.message.register(my_promocodes, lambda msg: msg.text == "🎁 Мои промокоды")
    dp.message.register(handle_photo, lambda msg: msg.photo is not None)

    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
