import asyncio
import threading
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import uvicorn

# Конфігурація
BOT_TOKEN = "7878078707:AAEnd1_7b5JFw9hsEX71DKWbPiJNyW4xB2k"
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://telegram-miniapp-cmol.onrender.com")  # ЗМІНІТЬ НА СВІЙ ДОМЕН

app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@app.get("/", response_class=HTMLResponse)
async def miniapp():
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Міні-додаток</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 400px;
            width: 100%;
            animation: fadeIn 0.6s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .logo {
            font-size: 64px;
            margin-bottom: 20px;
            animation: bounce 2s infinite;
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .subtitle {
            color: #666;
            font-size: 16px;
            margin-bottom: 30px;
        }
        .status {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            padding: 15px 25px;
            border-radius: 50px;
            font-size: 18px;
            font-weight: 600;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }
        .button {
            background: linear-gradient(45deg, #2196F3, #21CBF3);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            margin: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
        }
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4);
        }
        .button:active {
            transform: translateY(0);
        }
        .success {
            background: linear-gradient(45deg, #4CAF50, #8BC34A);
            color: white;
            padding: 15px;
            border-radius: 15px;
            font-weight: 600;
            margin-top: 20px;
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        .footer {
            margin-top: 30px;
            color: #888;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🚀</div>
        <h1>Міні-додаток</h1>
        <div class="subtitle">Telegram Web App</div>
        
        <div class="status">✨ Все працює відмінно!</div>
        
        <button class="button" onclick="showMessage()">🎯 Перевірити</button>
        <button class="button" onclick="closeApp()">❌ Закрити</button>
        
        <div id="result"></div>
        
        <div class="footer">
            Працює на FastAPI + Aiogram
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        function showMessage() {
            document.getElementById('result').innerHTML = 
                '<div class="success">🎉 Міні-додаток працює ідеально!</div>';
            tg.showAlert('Все працює!');
        }
        
        function closeApp() {
            tg.close();
        }
        
        // Головна кнопка
        tg.MainButton.text = "✅ Готово";
        tg.MainButton.show();
        tg.MainButton.onClick(() => { tg.close(); });
        
        // Адаптація до теми
        if (tg.colorScheme === 'dark') {
            document.body.style.background = 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)';
        }
    </script>
</body>
</html>
    """

@app.get("/api/status")
async def get_status():
    return {
        "status": "online",
        "app": "Telegram MiniApp",
        "version": "1.0.0"
    }

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="🚀 Відкрити додаток",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]]
    )
    
    await message.answer(
        f"🎉 Привіт {message.from_user.first_name}!\n\n"
        f"Це міні-додаток в Telegram!\n"
        f"Натисни кнопку щоб відкрити:",
        reply_markup=keyboard
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "📋 Доступні команди:\n"
        "/start - Відкрити міні-додаток\n"
        "/help - Показати цю допомогу\n"
        "/status - Перевірити статус"
    )

@dp.message(Command("status"))
async def status_command(message: types.Message):
    await message.answer(
        "✅ Міні-додаток працює!\n"
        f"🌐 URL: {WEBAPP_URL}\n"
        "🤖 Бот онлайн!"
    )

async def run_bot():
    print("🤖 Запуск Telegram бота...")
    await dp.start_polling(bot)

def start_bot():
    asyncio.run(run_bot())

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    
    print("🚀 Запуск міні-додатка...")
    
    # Запускаємо бота
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("=" * 50)
    print("✅ МІНІ-ДОДАТОК ГОТОВИЙ!")
    print("=" * 50)
    print(f"🌐 URL: {WEBAPP_URL}")
    print(f"📱 Порт: {port}")
    print("🤖 Telegram бот працює!")
    print("=" * 50)
    
    # Запускаємо веб-сервер
    uvicorn.run(app, host="0.0.0.0", port=port)
