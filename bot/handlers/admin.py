from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import ADMIN_ID, ALLOWED_USERS, _save_whitelist

router = Router()


def _is_admin(message: Message) -> bool:
    return message.from_user and message.from_user.id == ADMIN_ID


@router.message(Command("adduser"))
async def cmd_adduser(message: Message):
    if not _is_admin(message):
        return

    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Использование: /adduser 123456789")
        return

    user_id = int(args[1])
    ALLOWED_USERS.add(user_id)
    _save_whitelist(ALLOWED_USERS)
    await message.answer(f"Пользователь {user_id} добавлен.")


@router.message(Command("removeuser"))
async def cmd_removeuser(message: Message):
    if not _is_admin(message):
        return

    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Использование: /removeuser 123456789")
        return

    user_id = int(args[1])
    ALLOWED_USERS.discard(user_id)
    _save_whitelist(ALLOWED_USERS)
    await message.answer(f"Пользователь {user_id} удалён.")


@router.message(Command("users"))
async def cmd_users(message: Message):
    if not _is_admin(message):
        return

    if not ALLOWED_USERS:
        await message.answer("Whitelist пуст — доступ открыт всем.")
        return

    lines = [str(uid) for uid in sorted(ALLOWED_USERS)]
    await message.answer(f"Разрешённые пользователи ({len(lines)}):\n" + "\n".join(lines))
