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

### Локально (macOS)

```bash
# 1. Установить Tesseract
brew install tesseract tesseract-lang

# 2. Клонировать и настроить
git clone https://github.com/IvanAnis777/ocr_foto_word_bot.git
cd ocr_foto_word_bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Создать .env файл
cp .env.example .env
# Заполнить BOT_TOKEN и ADMIN_ID (см. раздел Настройка)

# 4. Создать whitelist
echo '[ваш_telegram_id]' > whitelist.json

# 5. Запустить
python -m bot.main
```

### Docker (рекомендуется)

```bash
git clone https://github.com/IvanAnis777/ocr_foto_word_bot.git
cd ocr_foto_word_bot
cp .env.example .env
# Заполнить BOT_TOKEN и ADMIN_ID
echo '[ваш_telegram_id]' > whitelist.json

docker compose up -d
```

## Ежедневное использование (Docker)

```bash
cd /Users/ivan/home-git/ocr_foto_word_bot

# Запустить бота (работает в фоне)
docker compose up -d

# Остановить бота
docker compose down

# Проверить статус
docker compose ps

# Посмотреть логи
docker compose logs -f

# Пересобрать после изменений в коде
docker compose up -d --build
```

## Настройка

### Получить токен бота
1. Открой Telegram, найди @BotFather
2. Напиши `/newbot`
3. Задай имя и username (должен заканчиваться на `bot`)
4. Скопируй токен

### Узнать свой Telegram ID
Напиши боту `/myid`

### Файл .env
```
BOT_TOKEN=токен_от_BotFather
TESSERACT_LANG=rus+eng
MEDIA_GROUP_TIMEOUT=2
TEMP_DIR=./temp
ADMIN_ID=ваш_telegram_id
```

### Файл whitelist.json
Создаётся автоматически при использовании `/adduser`. Или вручную:
```json
[123456789, 987654321]
```

## Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие и инструкция |
| `/help` | Справка |
| `/myid` | Узнать свой Telegram ID (доступна всем) |
| `/adduser ID` | Добавить пользователя (только админ) |
| `/removeuser ID` | Удалить пользователя (только админ) |
| `/users` | Список пользователей (только админ) |

## Управление доступом

Бот работает только для пользователей из whitelist.

### Как добавить нового человека
1. Дай ему ссылку на бота
2. Он пишет боту что угодно — получает сообщение "нет доступа" со своим ID
3. Тебе приходит уведомление с его именем и готовой командой
4. Нажимаешь `/adduser его_id` — готово

## Деплой на сервер

Работает на любом Linux-сервере с Docker:
```bash
# На сервере:
git clone https://github.com/IvanAnis777/ocr_foto_word_bot.git
cd ocr_foto_word_bot
cp .env.example .env
nano .env                    # заполнить BOT_TOKEN и ADMIN_ID
echo '[ваш_id]' > whitelist.json
docker compose up -d
```

## Структура проекта

```
ocr_foto_word_bot/
├── bot/
│   ├── main.py              # Точка входа
│   ├── config.py            # Настройки из .env
│   ├── middleware.py         # Whitelist фильтр
│   ├── handlers/
│   │   ├── start.py         # /start, /help, /myid
│   │   ├── photo.py         # Приём фото, media group
│   │   ├── callbacks.py     # Кнопки выбора формата
│   │   └── admin.py         # /adduser, /removeuser, /users
│   └── services/
│       ├── image_prep.py    # Предобработка (бинаризация)
│       ├── ocr.py           # OCR + определение таблиц
│       └── docx_builder.py  # Генерация .docx
├── docs/
│   └── admin-guide.md       # Краткая инструкция админа
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── whitelist.json           # Список разрешённых пользователей
```

## Стек

- Python 3.11+
- aiogram 3 (Telegram Bot API)
- Tesseract OCR + pytesseract
- img2table (определение таблиц)
- Pillow + numpy (предобработка изображений)
- python-docx (генерация Word)
- Docker

## Лицензия

MIT
