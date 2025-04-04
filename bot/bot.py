import os
import sys
import django
from dotenv import load_dotenv

# Загружаем .env
load_dotenv(override=True)

# Путь до проекта
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quest_bot.settings")
django.setup()

# Логирование и Aiogram
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from django.conf import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(
    token=os.getenv('TELEGRAM_BOT_TOKEN'),
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

# Регистрируем хендлеры
from bot.handlers import register_handlers

async def start_bot():
    register_handlers(dp, bot)
    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(start_bot())
