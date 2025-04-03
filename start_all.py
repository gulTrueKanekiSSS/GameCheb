import subprocess

# Запускаем Django через gunicorn
django = subprocess.Popen(["gunicorn", "GameCheb.wsgi"])

# Запускаем aiogram-бота
bot = subprocess.Popen(["python", "bot/bot.py"])

# Ждём завершения
django.wait()
bot.wait()
