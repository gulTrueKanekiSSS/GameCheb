from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command

from bot.handlers_core import (
    cmd_start, handle_contact,
    get_quest, my_promocodes,
    handle_photo
)
import admin_commands

def register_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(handle_contact, lambda m: m.contact is not None)
    dp.message.register(get_quest, lambda m: m.text == "🎯 Получить квест")
    dp.message.register(my_promocodes, lambda m: m.text == "🎁 Мои промокоды")
    dp.message.register(handle_photo, lambda m: m.photo is not None)

    dp.message.register(admin_commands.handle_approve, Command("approve"))
    dp.message.register(admin_commands.handle_reject, Command("reject"))
