FROM python:3.11-slim

# Устанавливаем Tesseract + языковые пакеты
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-rus \
        tesseract-ocr-eng \
        libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Зависимости отдельным слоем (кэшируется при пересборке)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Код бота
COPY bot/ bot/

# Директория для временных файлов
RUN mkdir -p /app/temp

CMD ["python", "-m", "bot.main"]
