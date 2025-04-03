import subprocess
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GameCheb.quest_bot.settings")
# Запускаем Django
django = subprocess.Popen(["gunicorn", "GameCheb.quest_bot.wsgi"])

# Запускаем бота
bot = subprocess.Popen(["python", "bot/bot.py"])  # путь до твоего bot.py

django.wait()
bot.wait()