# OCR Фото → Word Bot

Telegram-бот, который распознаёт текст на фотографиях и возвращает `.docx` файл.

Поддерживает русский и английский текст. Автоматически определяет таблицы на фото и сохраняет их как таблицы в Word.

## Возможности

- Приём одного или нескольких фото (media group)
- OCR через Tesseract (русский + английский)
- Автоматическое определение таблиц (img2table)
- Генерация `.docx` с таблицами или обычным текстом
- Выбор: один документ или отдельные файлы
- Whitelist доступа с админ-командами

## Быстрый старт

### Локально

```bash
# 1. Установить Tesseract
brew install tesseract tesseract-lang   # macOS
# apt install tesseract-ocr tesseract-ocr-rus   # Ubuntu/Debian

# 2. Клонировать и настроить
git clone https://github.com/IvanAnis777/ocr_foto_word_bot.git
cd ocr_foto_word_bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Создать .env файл
cp .env.example .env
# Заполнить BOT_TOKEN и ADMIN_ID

# 4. Запустить
python -m bot.main
```

### Docker

```bash
git clone https://github.com/IvanAnis777/ocr_foto_word_bot.git
cd ocr_foto_word_bot
cp .env.example .env
# Заполнить BOT_TOKEN и ADMIN_ID

docker compose up -d
```

## Настройка (.env)

```
BOT_TOKEN=токен_от_BotFather
TESSERACT_LANG=rus+eng
MEDIA_GROUP_TIMEOUT=2
TEMP_DIR=./temp
ADMIN_ID=ваш_telegram_id
```

## Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие и инструкция |
| `/help` | Справка |
| `/myid` | Узнать свой Telegram ID |
| `/adduser ID` | Добавить пользователя (админ) |
| `/removeuser ID` | Удалить пользователя (админ) |
| `/users` | Список пользователей (админ) |

## Стек

- Python 3.11+
- aiogram 3 (Telegram Bot API)
- Tesseract OCR + pytesseract
- img2table (определение таблиц)
- Pillow + numpy (предобработка изображений)
- python-docx (генерация Word)

## Лицензия

MIT
