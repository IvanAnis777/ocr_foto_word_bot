import pytesseract
from PIL import Image

from bot.config import TESSERACT_LANG
from bot.services.image_prep import preprocess_image, preprocess_cell


def recognize_text(image_path: str) -> str:
    """Распознать текст на изображении через Tesseract OCR."""
    img = preprocess_image(image_path)
    text = pytesseract.image_to_string(img, lang=TESSERACT_LANG)
    return text.strip()


def recognize_table(image_path: str) -> list[list[str]] | None:
    """Попробовать распознать таблицу на изображении.

    Возвращает список строк, каждая строка — список ячеек.
    Если таблица не найдена — возвращает None.
    """
    from img2table.document import Image as Img2Image

    doc = Img2Image(image_path)
    tables = doc.extract_tables(
        ocr=None,
        implicit_rows=False,
        implicit_columns=False,
        borderless_tables=False,
    )
    if not tables:
        return None

    # Берём первую (самую большую) таблицу
    table = tables[0]

    # Открываем оригинал в grayscale для кропа ячеек
    img = Image.open(image_path).convert("L")

    result = []
    for row in table.content.values():
        row_texts = []
        for cell in row:
            b = cell.bbox
            # Кропаем с отступом от линий таблицы
            cell_img = img.crop((b.x1 + 3, b.y1 + 3, b.x2 - 3, b.y2 - 3))
            cell_img = preprocess_cell(cell_img)
            text = pytesseract.image_to_string(
                cell_img, lang=TESSERACT_LANG, config="--psm 6"
            ).strip()
            # Убираем пустые строки
            lines = [l for l in text.split("\n") if l.strip()]
            row_texts.append("\n".join(lines))
        result.append(row_texts)

    return result


def recognize_smart(image_path: str) -> dict:
    """Умное распознавание: пробует найти таблицу, иначе — обычный текст.

    Возвращает:
        {"type": "table", "data": [[cell, ...], ...]}
        или
        {"type": "text", "data": "распознанный текст"}
    """
    table = recognize_table(image_path)
    if table:
        return {"type": "table", "data": table}
    text = recognize_text(image_path)
    return {"type": "text", "data": text}


def recognize_multiple(image_paths: list[str]) -> list[str]:
    """Распознать текст на нескольких изображениях (простой режим)."""
    return [recognize_text(path) for path in image_paths]
