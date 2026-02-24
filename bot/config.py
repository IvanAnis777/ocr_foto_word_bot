import json
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TESSERACT_LANG = os.getenv("TESSERACT_LANG", "rus+eng")
MEDIA_GROUP_TIMEOUT = int(os.getenv("MEDIA_GROUP_TIMEOUT", "2"))
TEMP_DIR = os.getenv("TEMP_DIR", "./temp")

# Админ бота — может управлять whitelist. Задаётся в .env.
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Файл для хранения whitelist (переживает перезапуски)
_WHITELIST_FILE = os.path.join(os.path.dirname(__file__), "..", "whitelist.json")


def _load_whitelist() -> set[int]:
    """Загрузить whitelist из файла."""
    if os.path.exists(_WHITELIST_FILE):
        with open(_WHITELIST_FILE) as f:
            return set(json.load(f))
    return set()


def _save_whitelist(users: set[int]) -> None:
    """Сохранить whitelist в файл."""
    with open(_WHITELIST_FILE, "w") as f:
        json.dump(sorted(users), f)


# Глобальный whitelist — мутабельный set
ALLOWED_USERS: set[int] = _load_whitelist()
