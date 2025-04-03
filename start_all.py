import subprocess
import os

# Запускаем Django
django = subprocess.Popen(["gunicorn", "quest_bot.wsgi"])

# Запускаем бота
bot = subprocess.Popen(["python", "api/bot/bot.py"])  # путь до твоего bot.py

django.wait()
bot.wait()