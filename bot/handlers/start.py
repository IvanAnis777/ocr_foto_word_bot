from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()

HELP_TEXT = (
    "Я распознаю текст на фотографиях и возвращаю .docx файл.\n\n"
    "Как пользоваться:\n"
    "1. Отправь одно или несколько фото\n"
    "2. Подожди пока я распознаю текст\n"
    "3. Выбери формат: отдельные файлы или один документ\n"
    "4. Получи .docx файл(ы)\n\n"
    "Поддерживаю русский и английский текст.\n"
    "Если на фото таблица — она сохранится как таблица в Word."
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет! {HELP_TEXT}"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_TEXT)


@router.message(Command("myid"))
async def cmd_myid(message: Message):
    await message.answer(f"Твой Telegram ID: `{message.from_user.id}`", parse_mode="Markdown")
