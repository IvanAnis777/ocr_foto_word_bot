import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import BOT_TOKEN, ALLOWED_USERS
from bot.handlers import start, photo, callbacks, admin
from bot.middleware import WhitelistMiddleware


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан! Проверь .env файл.")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Whitelist — фильтр доступа
    dp.message.middleware(WhitelistMiddleware())
    dp.callback_query.middleware(WhitelistMiddleware())

    # Подключаем хендлеры
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(photo.router)
    dp.include_router(callbacks.router)

    if ALLOWED_USERS:
        logging.info("Whitelist: %s", ALLOWED_USERS)
    else:
        logging.info("Whitelist отключён — доступ открыт всем")
    logging.info("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
