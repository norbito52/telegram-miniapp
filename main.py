# main.py - без емодзі, на російській мові
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
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://telegram-miniapp-cmol.onrender.com")

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
    <title>GiftRoom Market</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: #1a1a2e;
            color: white;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            min-height: 100vh;
            padding: 20px;
            padding-bottom: 80px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        
        .header h1 {
            font-size: 24px;
            color: #ffffff;
            margin-bottom: 5px;
        }
        
        .header .subtitle {
            color: #8b8b8b;
            font-size: 14px;
        }
        
        .tabs {
            display: flex;
            margin-bottom: 20px;
            background: #2a2a3e;
            border-radius: 10px;
            padding: 4px;
        }
        
        .tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .tab.active {
            background: #3d5afe;
            color: white;
        }
        
        .tab:not(.active) {
            color: #8b8b8b;
        }
        
        .gifts-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .gift-card {
            background: #2a2a3e;
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            transition: transform 0.3s ease;
            min-height: 180px;
        }
        
        .gift-card:hover {
            transform: translateY(-2px);
        }
        
        .gift-image-placeholder {
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            margin: 0 auto 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            color: white;
            font-weight: 600;
        }
        
        .gift-title {
            color: white;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
            text-transform: uppercase;
        }
        
        .gift-subtitle {
            color: #8b8b8b;
            font-size: 12px;
            margin-bottom: 15px;
        }
        
        .price-btn {
            background: #2196F3;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            width: 100%;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
        }
        
        .price-btn:hover {
            background: #1976D2;
            transform: translateY(-1px);
        }
        
        .triangle-icon {
            color: #64B5F6;
            font-size: 16px;
        }
        
        .cancel-btn {
            background: #f44336;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 12px;
            margin-top: 8px;
            cursor: pointer;
        }
        
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #1a1a2e;
            border-top: 1px solid #2a2a3e;
            display: flex;
            padding: 15px;
        }
        
        .nav-item {
            flex: 1;
            text-align: center;
            padding: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .nav-item.active {
            color: #3d5afe;
        }
        
        .nav-item:not(.active) {
            color: #8b8b8b;
        }
        
        .nav-text {
            font-size: 12px;
            font-weight: 500;
        }
        
        .new-badge {
            background: #4CAF50;
            color: white;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 10px;
            font-weight: 600;
            margin-left: 5px;
        }
        
        .search-box {
            background: #2a2a3e;
            border: none;
            padding: 12px 15px;
            border-radius: 10px;
            color: white;
            width: 100%;
            margin-bottom: 20px;
            font-size: 14px;
        }
        
        .search-box::placeholder {
            color: #8b8b8b;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .gift-card {
            animation: fadeIn 0.6s ease-out;
        }
        
        .empty-state {
            grid-column: 1/-1;
            text-align: center;
            padding: 40px;
            color: #8b8b8b;
        }
        
        .empty-icon {
            width: 80px;
            height: 80px;
            background: #2a2a3e;
            border-radius: 50%;
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>GiftRoom Market</h1>
        <div class="subtitle">Магазин подарков в Telegram</div>
    </div>
    
    <input type="text" class="search-box" placeholder="Поиск подарков...">
    
    <div class="tabs">
        <div class="tab active" onclick="switchTab('listed')">Listed Gifts</div>
        <div class="tab" onclick="switchTab('unlisted')">Unlisted Gifts</div>
    </div>
    
    <div class="gifts-grid" id="giftsGrid">
        <div class="gift-card">
            <div class="gift-image-placeholder">ОРЕЛ</div>
            <div class="gift-title">ОРЕЛ <span class="new-badge">NEW!</span></div>
            <div class="gift-subtitle">Символ свободы</div>
            <button class="price-btn">
                <span>2.12</span>
                <span class="triangle-icon">▼</span>
                <span>(1244 подарков)</span>
            </button>
        </div>
        
        <div class="gift-card">
            <div class="gift-image-placeholder">СТАТУЯ</div>
            <div class="gift-title">СТАТУЯ <span class="new-badge">NEW!</span></div>
            <div class="gift-subtitle">Статуя Свободы</div>
            <button class="price-btn">
                <span>5.3</span>
                <span class="triangle-icon">▼</span>
                <span>(508 подарков)</span>
            </button>
        </div>
        
        <div class="gift-card">
            <div class="gift-image-placeholder">ФАКЕЛ</div>
            <div class="gift-title">ФАКЕЛ <span class="new-badge">NEW!</span></div>
            <div class="gift-subtitle">Огонь свободы</div>
            <button class="price-btn">
                <span>4.759</span>
                <span class="triangle-icon">▼</span>
                <span>(215 подарков)</span>
            </button>
        </div>
        
        <div class="gift-card">
            <div class="gift-image-placeholder">СОСКА</div>
            <div class="gift-title">СОСКА <span class="new-badge">NEW!</span></div>
            <div class="gift-subtitle">Золотая соска</div>
            <button class="price-btn">
                <span>12.614</span>
                <span class="triangle-icon">▼</span>
                <span>(611 подарков)</span>
            </button>
        </div>
        
        <div class="gift-card">
            <div class="gift-image-placeholder">МОРОЖЕНОЕ</div>
            <div class="gift-title">МОРОЖЕНОЕ</div>
            <div class="gift-subtitle">Холодное удовольствие</div>
            <button class="price-btn">
                <span>95.4</span>
                <span class="triangle-icon">▼</span>
                <span>(231 подарок)</span>
            </button>
        </div>
        
        <div class="gift-card">
            <div class="gift-image-placeholder">КУЛИЧ</div>
            <div class="gift-title">КУЛИЧ</div>
            <div class="gift-subtitle">Праздничный десерт</div>
            <button class="price-btn">
                <span>2.12</span>
                <span class="triangle-icon">▼</span>
                <span>(11500 подарков)</span>
            </button>
        </div>
    </div>
    
    <div class="bottom-nav">
        <div class="nav-item active">
            <div class="nav-text">Market</div>
        </div>
        <div class="nav-item" onclick="showMyGifts()">
            <div class="nav-text">My Gifts</div>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        function switchTab(tab) {
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
            
            if (tab === 'unlisted') {
                showMyGifts();
            } else {
                showListedGifts();
            }
        }
        
        function showMyGifts() {
            const grid = document.getElementById('giftsGrid');
            grid.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">?</div>
                    <div style="font-size: 16px; margin-bottom: 8px;">У вас пока нет подарков</div>
                    <div style="font-size: 14px;">Купите подарки в Market чтобы увидеть их здесь</div>
                </div>
            `;
            
            // Обновляем навигацию
            const navItems = document.querySelectorAll('.nav-item');
            navItems.forEach(item => item.classList.remove('active'));
            navItems[1].classList.add('active');
        }
        
        function showListedGifts() {
            location.reload(); // Простое обновление страницы
        }
        
        // Главная кнопка Telegram
        tg.MainButton.text = "Готово";
        tg.MainButton.show();
        tg.MainButton.onClick(() => { 
            tg.showAlert('GiftRoom Market работает!');
        });
        
        // Адаптация к теме
        if (tg.colorScheme === 'dark') {
            document.body.style.background = '#0f0f1a';
        }
        
        // Анимация при загрузке
        document.addEventListener('DOMContentLoaded', () => {
            const cards = document.querySelectorAll('.gift-card');
            cards.forEach((card, index) => {
                card.style.animationDelay = `${index * 0.1}s`;
            });
        });
    </script>
</body>
</html>
    """

# Telegram бот
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="Открыть GiftRoom Market",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]]
    )
    
    await message.answer(
        f"Привет {message.from_user.first_name}!\n\n"
        f"Добро пожаловать в GiftRoom Market!\n"
        f"Магазин уникальных подарков в Telegram.\n\n"
        f"Нажми кнопку чтобы открыть каталог:",
        reply_markup=keyboard
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "Доступные команды:\n\n"
        "/start - Открыть GiftRoom Market\n"
        "/help - Показать эту помощь\n"
        "/catalog - Посмотреть каталог\n"
        "/support - Поддержка"
    )

async def run_bot():
    await dp.start_polling(bot)

def start_bot():
    asyncio.run(run_bot())

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("GiftRoom Market запущен!")
    print(f"URL: {WEBAPP_URL}")
    print("Магазин подарков готов!")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
