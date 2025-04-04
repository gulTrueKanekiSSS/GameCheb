import os
import sys
from dotenv import load_dotenv

# Загрузка .env
load_dotenv(override=True)

# Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quest_bot.settings")

# Добавляем корень проекта в path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, BASE_DIR)

# Django setup
import django
django.setup()

# Импорт и запуск бота
from bot.bot import start_bot

if __name__ == "__main__":
    import asyncio
    asyncio.run(start_bot())
