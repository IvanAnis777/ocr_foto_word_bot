from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message, CallbackQuery

from bot.config import ADMIN_ID, ALLOWED_USERS

# Чтобы не спамить админа — запоминаем кому уже отказали
_notified_users: set[int] = set()


class WhitelistMiddleware(BaseMiddleware):
    """Пропускает только пользователей из ALLOWED_USERS.

    Если ALLOWED_USERS пустой — доступ открыт всем.
    Новым пользователям — инструкция + уведомление админу.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        # Если whitelist пустой — пропускаем всех
        if not ALLOWED_USERS:
            return await handler(event, data)

        # Определяем user_id
        user_id = None
        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
            # /myid доступна всем
            if event.text and event.text.strip() == "/myid":
                return await handler(event, data)
            # Админ всегда проходит
            if user_id == ADMIN_ID:
                return await handler(event, data)
        elif isinstance(event, CallbackQuery) and event.from_user:
            user_id = event.from_user.id

        if user_id and user_id in ALLOWED_USERS:
            return await handler(event, data)

        # Не в whitelist — сообщаем пользователю и уведомляем админа
        if isinstance(event, Message) and user_id and user_id not in _notified_users:
            _notified_users.add(user_id)
            bot: Bot = data["bot"]

            # Сообщение пользователю
            name = event.from_user.full_name or "—"
            await event.answer(
                f"У тебя пока нет доступа к боту.\n\n"
                f"Твой ID: `{user_id}`\n"
                f"Отправь этот ID администратору для получения доступа.",
                parse_mode="Markdown",
            )

            # Уведомление админу
            username = f"@{event.from_user.username}" if event.from_user.username else "нет"
            await bot.send_message(
                ADMIN_ID,
                f"Запрос доступа:\n"
                f"Имя: {name}\n"
                f"Username: {username}\n"
                f"ID: `{user_id}`\n\n"
                f"Чтобы добавить:\n`/adduser {user_id}`",
                parse_mode="Markdown",
            )

        return None
