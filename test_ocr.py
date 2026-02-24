"""Тестовый скрипт: распознаёт фото и собирает .docx (с поддержкой таблиц)."""
import os

from bot.services.ocr import recognize_smart
from bot.services.docx_builder import build_single_docx, build_separate_docx


def main():
    os.makedirs("temp", exist_ok=True)

    image_path = "temp/image.png"
    if not os.path.exists(image_path):
        print(f"Файл {image_path} не найден. Положи тестовую картинку в temp/")
        return

    print(f"Распознаю {image_path}...")
    result = recognize_smart(image_path)

    if result["type"] == "table":
        table = result["data"]
        print(f"\nНайдена таблица: {len(table)} строк x {len(table[0])} колонок\n")
        for ri, row in enumerate(table):
            print(f"--- Строка {ri + 1} ---")
            for ci, cell in enumerate(row):
                preview = cell[:100].replace("\n", " | ")
                print(f"  [{ci}]: {preview}")
        print()
    else:
        print(f"\nОбычный текст ({len(result['data'])} символов):")
        print(result["data"][:500])
        print()

    # Генерация .docx
    pages = [result]
    single = build_single_docx(pages)
    print(f"Файл создан: {single}")

    separate = build_separate_docx(pages)
    print(f"Отдельные файлы: {separate}")

    print("\nГотово! Открой файлы в temp/ и проверь результат.")


if __name__ == "__main__":
    main()
