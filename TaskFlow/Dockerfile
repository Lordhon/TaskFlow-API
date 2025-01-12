FROM python:3.10-slim

# Установка системных пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальной части проекта
COPY . .

# Указание команды по умолчанию для использования daphne
ENTRYPOINT ["sh", "-c", "python manage.py migrate && daphne TaskFlow.asgi:application --bind 0.0.0.0 --port 8000"]