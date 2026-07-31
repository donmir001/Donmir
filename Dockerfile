# Использование официального легкого образа Python
FROM python:3.12-slim

# Настройки Python для стабильной работы в контейнере
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Рабочая директория внутри контейнера
WORKDIR /app

# Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода проекта
COPY . .

# Открытие порта
EXPOSE 8000

# Команда запуска агента
CMD ["python", "main.py"]
