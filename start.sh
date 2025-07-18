#!/bin/bash

# Start script для Render

echo "🚀 Starting GiftRoom Marketplace..."

# Встановлюємо змінні середовища
export PYTHONPATH=/app
export PYTHONUNBUFFERED=1

# Перевіряємо наявність основних файлів
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found!"
    exit 1
fi

if [ ! -f "app/main.py" ]; then
    echo "❌ app/main.py not found!"
    exit 1
fi

# Запускаємо сервер
echo "🌐 Starting server on port $PORT..."
exec uvicorn main:app --host 0.0.0.0 --port $PORT
