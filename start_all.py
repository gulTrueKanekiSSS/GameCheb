import subprocess
import os
import sys

# Добавляем папку GameCheb в PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'GameCheb'))

# Указываем правильный путь к settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quest_bot.settings")

# Запускаем Django через gunicorn
django = subprocess.Popen(["gunicorn", "quest_bot.wsgi"])

# Запускаем aiogram-бота
bot = subprocess.Popen(["python", "GameCheb/bot/bot.py"])

# Ожидаем завершения обоих
django.wait()
bot.wait()
