#!/bin/bash

# Build script для Render

echo "🔧 Starting build process..."

# Встановлюємо залежності
echo "📦 Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# Створюємо необхідні папки
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p frontend

# Встановлюємо права на виконання
echo "🔐 Setting permissions..."
chmod +x run.py

# Перевіряємо структуру проєкту
echo "🔍 Checking project structure..."
ls -la

echo "✅ Build completed successfully!"
