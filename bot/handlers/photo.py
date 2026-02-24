import asyncio
import logging
import os
from collections import defaultdict

from aiogram import Router, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import MEDIA_GROUP_TIMEOUT, TEMP_DIR
from bot.services.ocr import recognize_smart

log = logging.getLogger(__name__)

router = Router()

# Хранилище для media group: {media_group_id: [message, ...]}
_media_groups: dict[str, list[Message]] = defaultdict(list)
# Флаг что обработка уже запущена для группы
_processing: dict[str, bool] = {}


async def _download_photo(bot: Bot, message: Message) -> str:
    """Скачать фото из сообщения, вернуть путь к файлу."""
    os.makedirs(TEMP_DIR, exist_ok=True)
    photo = message.photo[-1]  # Наибольший размер
    file = await bot.get_file(photo.file_id)
    filepath = os.path.join(TEMP_DIR, f"{photo.file_unique_id}.jpg")
    await bot.download_file(file.file_path, filepath)
    return filepath


async def _process_photos(messages: list[Message], bot: Bot, chat_id: int):
    """Обработать пачку фото: скачать, OCR, отправить кнопки выбора."""
    # Скачиваем все фото
    paths = []
    for msg in messages:
        path = await _download_photo(bot, msg)
        paths.append(path)

    # OCR каждого фото
    results = []
    for path in paths:
        log.info("OCR: %s (%d bytes)", path, os.path.getsize(path))
        result = await asyncio.to_thread(recognize_smart, path)
        log.info("Результат: type=%s", result["type"])
        results.append(result)

    # Сохраняем результаты в памяти для callback
    from bot.handlers.callbacks import save_results
    group_key = save_results(chat_id, results)

    # Кнопки выбора формата
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📄 Отдельные файлы",
                callback_data=f"separate:{group_key}",
            ),
            InlineKeyboardButton(
                text="📑 Один документ",
                callback_data=f"single:{group_key}",
            ),
        ]
    ])

    count = len(results)
    tables = sum(1 for r in results if r["type"] == "table")
    text_msg = f"✅ Готово! Распознал текст из {count} фото."
    if tables:
        text_msg += f"\n📊 Найдено таблиц: {tables}"
    text_msg += "\nКак отправить?"

    await bot.send_message(chat_id, text_msg, reply_markup=keyboard)

    # TODO: временно не удаляем фото для диагностики
    # for path in paths:
    #     if os.path.exists(path):
    #         os.remove(path)


@router.message(lambda m: m.photo is not None)
async def handle_photo(message: Message, bot: Bot):
    """Обработка входящих фото. Поддерживает одиночные и media group."""
    if message.media_group_id:
        # Фото из media group — собираем пачку
        group_id = message.media_group_id
        _media_groups[group_id].append(message)

        if group_id in _processing:
            return  # Уже ждём остальные фото

        _processing[group_id] = True

        # Ждём пока все фото придут
        await asyncio.sleep(MEDIA_GROUP_TIMEOUT)

        messages = _media_groups.pop(group_id)
        _processing.pop(group_id, None)

        status = await bot.send_message(
            message.chat.id,
            f"⏳ Получил {len(messages)} фото. Распознаю текст...",
        )
        await _process_photos(messages, bot, message.chat.id)
        await status.delete()
    else:
        # Одиночное фото
        status = await message.answer("⏳ Получил фото. Распознаю текст...")
        await _process_photos([message], bot, message.chat.id)
        await status.delete()
