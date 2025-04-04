import logging
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.command import Command
from asgiref.sync import sync_to_async
from core.models import User, Quest, UserQuestProgress

logger = logging.getLogger(__name__)

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎯 Получить квест")],
            [KeyboardButton(text="🎁 Мои промокоды")]
        ],
        resize_keyboard=True
    )

@sync_to_async
def get_or_create_user(telegram_id, name):
    return User.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={'name': name}
    )

@sync_to_async
def get_user(telegram_id):
    return User.objects.get(telegram_id=telegram_id)

@sync_to_async
def get_available_quest(user):
    return Quest.objects.filter(
        is_active=True
    ).exclude(
        userquestprogress__user=user
    ).first()

@sync_to_async
def save_user(user):
    user.save()

@sync_to_async
def get_completed(user):
    return list(UserQuestProgress.objects.filter(
        user=user,
        status=UserQuestProgress.Status.APPROVED,
        promo_code__isnull=False
    ).select_related('quest', 'promo_code'))

@sync_to_async
def create_progress(user, quest, file_id):
    return UserQuestProgress.objects.create(
        user=user,
        quest=quest,
        photo=file_id
    )


# === HANDLERS ===

async def cmd_start(message: types.Message):
    user, created = await get_or_create_user(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name
    )

    if not user.is_verified:
        contact_keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)]],
            resize_keyboard=True
        )
        await message.answer(
            "Добро пожаловать! Поделитесь номером телефона для начала.",
            reply_markup=contact_keyboard
        )
    else:
        await message.answer(
            "Добро пожаловать в систему квестов! Выберите действие:",
            reply_markup=get_main_keyboard()
        )

async def handle_contact(message: types.Message):
    user = await get_user(message.from_user.id)
    user.phone_number = message.contact.phone_number
    user.is_verified = True
    await save_user(user)

    await message.answer(
        "Спасибо! Теперь вы можете начать выполнять квесты.",
        reply_markup=get_main_keyboard()
    )

async def get_quest(message: types.Message):
    user = await get_user(message.from_user.id)

    if not user.is_verified:
        await message.answer("Пожалуйста, подтвердите номер телефона.")
        return

    quest = await get_available_quest(user)
    if not quest:
        await message.answer("К сожалению, нет доступных квестов.")
        return

    await message.answer(
        f"🎯 Квест: {quest.name}\n\n"
        f"📍 Локация: {quest.location}\n\n"
        f"📝 Описание:\n{quest.description}\n\n"
        "Для подтверждения выполнения квеста отправьте фото."
    )

    try:
        if quest.latitude and quest.longitude:
            await message.answer_location(
                latitude=float(quest.latitude),
                longitude=float(quest.longitude)
            )
    except Exception as e:
        logger.error(f"Ошибка при отправке локации: {e}")
        await message.answer("Не удалось отправить карту.")

async def my_promocodes(message: types.Message):
    user = await get_user(message.from_user.id)
    completed = await get_completed(user)

    if not completed:
        await message.answer("У вас пока нет полученных промокодов.")
        return

    text = "Ваши промокоды:\n\n"
    for p in completed:
        text += f"🎁 Квест: {p.quest.name}\n🎫 Промокод: {p.promo_code.code}\n\n"

    await message.answer(text)

async def handle_photo(message: types.Message):
    from django.conf import settings

    user = await get_user(message.from_user.id)
    quest = await get_available_quest(user)

    if not quest:
        await message.answer("У вас нет активного квеста.")
        return

    file_id = message.photo[-1].file_id
    progress = await create_progress(user, quest, file_id)

    await message.answer("Фото получено! Админ проверит выполнение.")

    await message.bot.send_photo(
        chat_id=settings.ADMIN_GROUP_ID,
        photo=file_id,
        caption=(
            f"Новое выполнение квеста!\n\n"
            f"👤 Пользователь: {user.name}\n"
            f"🎯 Квест: {quest.name}\n"
            f"🆔 ID прогресса: {progress.id}\n\n"
            f"/approve {progress.id}\n/reject {progress.id} причина"
        )
    )
