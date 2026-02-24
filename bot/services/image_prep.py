import numpy as np
from PIL import Image, ImageFilter, ImageOps


def preprocess_image(image_path: str) -> Image.Image:
    """Подготовка изображения для OCR: убираем фон, адаптивная бинаризация, резкость."""
    img = Image.open(image_path).convert("L")
    img = _binarize(img)
    img = img.filter(ImageFilter.SHARPEN)
    img = _upscale_if_small(img)
    return img


def preprocess_cell(cell_img: Image.Image) -> Image.Image:
    """Предобработка отдельной ячейки таблицы для OCR."""
    cell_img = _binarize(cell_img)
    cell_img = cell_img.filter(ImageFilter.SHARPEN)
    # Увеличиваем в 2 раза — ячейки обычно маленькие
    w, h = cell_img.size
    cell_img = cell_img.resize((w * 2, h * 2), Image.LANCZOS)
    # Белые поля — Tesseract работает лучше с отступами
    cell_img = ImageOps.expand(cell_img, border=40, fill=255)
    return cell_img


def _binarize(img: Image.Image) -> Image.Image:
    """Адаптивная бинаризация: убирает цветной фон, оставляет текст."""
    img_array = np.array(img)
    blurred = img.filter(ImageFilter.BoxBlur(15))
    mean_array = np.array(blurred)
    binary = np.where(img_array < mean_array - 10, 0, 255).astype(np.uint8)
    return Image.fromarray(binary)


def _upscale_if_small(img: Image.Image) -> Image.Image:
    """Увеличиваем маленькие изображения в 2 раза для лучшего OCR."""
    width, height = img.size
    if width < 1000 or height < 1000:
        img = img.resize((width * 2, height * 2), Image.LANCZOS)
    return img
