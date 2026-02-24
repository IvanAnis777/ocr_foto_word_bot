import os
import uuid

from aiogram import Router, Bot
from aiogram.types import CallbackQuery, FSInputFile

from bot.services.docx_builder import build_single_docx, build_separate_docx
from bot.config import TEMP_DIR

router = Router()

# Хранилище результатов OCR: {group_key: [result, ...]}
_results_store: dict[str, list[dict]] = {}


def save_results(chat_id: int, results: list[dict]) -> str:
    """Сохранить результаты OCR, вернуть ключ для callback."""
    key = str(uuid.uuid4())[:8]
    _results_store[key] = results
    return key


def _cleanup_files(paths: list[str]):
    """Удалить временные файлы."""
    for path in paths:
        if os.path.exists(path):
            os.remove(path)


@router.callback_query(lambda c: c.data.startswith("single:"))
async def cb_single(callback: CallbackQuery, bot: Bot):
    """Отправить все фото в одном .docx файле."""
    key = callback.data.split(":")[1]
    results = _results_store.pop(key, None)

    if not results:
        await callback.answer("Результаты устарели, отправь фото заново.")
        return

    filepath = build_single_docx(results)
    await bot.send_document(
        callback.message.chat.id,
        FSInputFile(filepath),
        caption=f"📑 Объединённый документ ({len(results)} стр.)",
    )
    await callback.message.edit_text("📑 Отправлено одним документом.")
    await callback.answer()

    _cleanup_files([filepath])


@router.callback_query(lambda c: c.data.startswith("separate:"))
async def cb_separate(callback: CallbackQuery, bot: Bot):
    """Отправить каждое фото как отдельный .docx файл."""
    key = callback.data.split(":")[1]
    results = _results_store.pop(key, None)

    if not results:
        await callback.answer("Результаты устарели, отправь фото заново.")
        return

    paths = build_separate_docx(results)
    for i, filepath in enumerate(paths, start=1):
        await bot.send_document(
            callback.message.chat.id,
            FSInputFile(filepath),
            caption=f"📄 Страница {i} из {len(paths)}",
        )
    await callback.message.edit_text(f"📄 Отправлено {len(paths)} файл(ов).")
    await callback.answer()

    _cleanup_files(paths)
