# main.py - FastAPI приложение для GiftRoom Market с фильтрами
import asyncio
import threading
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import uvicorn

# Конфигурация
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
        .new-badge {
            background: #4CAF50;
            color: white;
            font-size: 9px;
            padding: 2px 5px;
            border-radius: 8px;
            font-weight: 600;
            margin-left: 4px;
        }
        
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
            margin-bottom: 15px;
        }
        
        .wallet-section {
            background: #2a2a3e;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .wallet-connect-btn {
            background: #0088ff;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            width: 100%;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        
        .wallet-connect-btn:hover {
            background: #006dd9;
        }
        
        .balance-section {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }
        
        .balance-btn {
            background: #2196F3;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        .balance-btn:hover {
            background: #1976D2;
            transform: scale(1.1);
        }
        
        .balance-btn.minus {
            background: #ff4757;
        }
        
        .balance-btn.minus:hover {
            background: #ff3742;
        }
        
        .balance-display {
            color: white;
            font-size: 16px;
            font-weight: 600;
            min-width: 100px;
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
            font-size: 14px;
        }
        
        .tab.active {
            background: #3d5afe;
            color: white;
        }
        
        .tab:not(.active) {
            color: #8b8b8b;
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
        
        /* Фильтры */
        .filters-section {
            margin-bottom: 20px;
        }
        
        .filter-row {
            display: flex;
            gap: 8px;
            margin-bottom: 15px;
            align-items: center;
        }
        
        .filter-select {
            background: #2a2a3e;
            border: none;
            padding: 10px 12px;
            border-radius: 8px;
            color: white;
            font-size: 13px;
            flex: 1;
        }
        
        .filter-select option {
            background: #2a2a3e;
            color: white;
        }
        
        .clear-filters-btn {
            background: #ff4757;
            color: white;
            border: none;
            padding: 8px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 16px;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            flex-shrink: 0;
            margin-left: 8px;
        }
        
        .clear-filters-btn:hover {
            background: #ff3742;
            transform: scale(1.1);
        }
        
        .filter-label {
            color: #8b8b8b;
            font-size: 12px;
            font-weight: 500;
            min-width: 35px;
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
            min-height: 200px;
            position: relative;
        }
        
        .gift-card:hover {
            transform: translateY(-2px);
        }
        
        .gift-id {
            position: absolute;
            top: 8px;
            left: 8px;
            background: rgba(0,0,0,0.6);
            color: #8b8b8b;
            font-size: 10px;
            padding: 4px 6px;
            border-radius: 4px;
            font-weight: 500;
        }
        
        .gift-image {
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            margin: 15px auto 10px;
            background-size: cover;
            background-position: center;
            border: 2px solid #3a3a5c;
        }
        
        .gift-title {
            color: white;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 8px;
            text-transform: uppercase;
            line-height: 1.2;
        }
        
        .gift-subtitle {
            color: #8b8b8b;
            font-size: 11px;
            margin-bottom: 15px;
            line-height: 1.3;
        }
        
        .price-btn {
            background: #2196F3;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 8px;
            width: 100%;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            font-size: 12px;
        }
        
        .price-btn:hover {
            background: #1976D2;
            transform: translateY(-1px);
        }
        
        .triangle-icon {
            color: #64B5F6;
            font-size: 14px;
        }
        
        .gift-card-catalog {
            background: #2a2a3e;
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            transition: transform 0.3s ease;
            min-height: 140px;
            position: relative;
            cursor: pointer;
        }
        
        .gift-card-catalog:hover {
            transform: translateY(-2px);
        }
        
        .gift-image-catalog {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            margin: 10px auto 15px;
            background-size: cover;
            background-position: center;
            border: 2px solid #3a3a5c;
        }
        
        .gift-name-catalog {
            color: white;
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            line-height: 1.2;
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
        
        .empty-state {
            grid-column: 1/-1;
            text-align: center;
            padding: 40px;
            color: #8b8b8b;
        }
        
        .loading {
            grid-column: 1/-1;
            text-align: center;
            padding: 40px;
            color: #8b8b8b;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .gift-card {
            animation: fadeIn 0.6s ease-out;
        }
        
        .active-filter {
            background: #3d5afe !important;
        }
        
        .filters-hidden {
            display: none;
        }
        
        /* Filter page styles */
        .filter-list {
            margin-top: 20px;
        }
        
        .filter-item {
            display: flex;
            align-items: center;
            background: #2a2a3e;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .filter-item:hover {
            background: #323251;
        }
        
        .filter-item.selected {
            border-color: #3d5afe;
            background: #2a2a5e;
        }
        
        .filter-item-image {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            margin-right: 15px;
            background-size: cover;
            background-position: center;
            border: 2px solid #3a3a5c;
            flex-shrink: 0;
        }
        
        .filter-item-content {
            flex: 1;
        }
        
        .filter-item-name {
            color: white;
            font-size: 16px;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        
        .filter-item-price {
            color: #64B5F6;
            font-size: 14px;
            font-weight: 500;
        }
        
        .filter-item-badge {
            background: #4CAF50;
            color: white;
            font-size: 10px;
            padding: 4px 8px;
            border-radius: 12px;
            font-weight: 600;
            margin-left: 10px;
        }
        
        .filter-clear-btn {
            background: #ff4757;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            width: 100%;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        
        .filter-clear-btn:hover {
            background: #ff3742;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>GiftRoom Market</h1>
        <div class="subtitle">Магазин подарков в Telegram</div>
        
        <div class="wallet-section">
            <button class="wallet-connect-btn" onclick="connectWallet()">Привязать TON кошелек</button>
            <div class="balance-section">
                <button class="balance-btn minus" onclick="withdrawBalance()">−</button>
                <div class="balance-display">0.00 TON</div>
                <button class="balance-btn" onclick="addBalance()">+</button>
            </div>
        </div>
    </div>
    
    <input type="text" class="search-box" placeholder="Поиск подарков..." id="searchBox" onkeyup="searchGifts()">
    
    <div class="tabs">
        <div class="tab active" onclick="switchTab('market')">Market</div>
        <div class="tab" onclick="showFilter()">Все подарки</div>
        <div class="tab" onclick="switchTab('my-gifts')">My Gifts</div>
    </div>
    
    <!-- Фильтры (показываются только в Market) -->
    <div class="filters-section" id="filtersSection">
        <div class="filter-row">
            <select class="filter-select" id="giftTypeFilter" onchange="applyFilters()">
                <option value="">Все подарки</option>
                <option value="fashion">Мода</option>
                <option value="food">Еда</option>
                <option value="animals">Животные</option>
                <option value="objects">Предметы</option>
                <option value="holidays">Праздники</option>
                <option value="sports">Спорт</option>
                <option value="symbols">Символы</option>
                <option value="entertainment">Развлечения</option>
                <option value="misc">Разное</option>
            </select>
            
            <select class="filter-select" id="sortFilter" onchange="applyFilters()">
                <option value="recent">Недавние</option>
                <option value="price_asc">Цена: мин → макс</option>
                <option value="price_desc">Цена: макс → мин</option>
                <option value="rarity">По редкости</option>
            </select>
            
            <button class="clear-filters-btn" onclick="clearFilters()" title="Очистить фильтры">✕</button>
        </div>
    </div>
    
    <div class="gifts-grid" id="giftsGrid">
        <div class="loading">Загрузка подарков...</div>
    </div>
    
    <div class="bottom-nav">
        <div class="nav-item active">
            <div class="nav-text">Market</div>
        </div>
        <div class="nav-item" onclick="switchTab('my-gifts')">
            <div class="nav-text">My Gifts</div>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        // База данных всех 37 подарков с категориями
        const allGifts = [
            {id: 1, name: "HEELS", desc: "High heels", price: "2.12", count: "11500", new: false, listed: true, category: "fashion", rarity: 1, image: "https://i.postimg.cc/jdsL20Gt/Gifts-Gifts-Gifts-Ag-ADBmg-AAnz-Oe-Ek.png"},
            {id: 2, name: "BUTTON", desc: "Simple button", price: "2.90", count: "3056", new: false, listed: true, category: "objects", rarity: 1, image: "https://i.postimg.cc/XqDSnCRZ/Gifts-Gifts-Gifts-Ag-ADWWg-AAhwgi-Uk.png"},
            {id: 3, name: "CATS", desc: "Cute cats", price: "3.23", count: "2945", new: false, listed: true, category: "animals", rarity: 1, image: "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"},
            {id: 4, name: "SOCKS", desc: "Warm socks", price: "3.56", count: "2834", new: false, listed: false, category: "fashion", rarity: 1, image: "https://i.postimg.cc/bwxCTnmQ/Gifts-Gifts-Gifts-Ag-ADKmk-AAt0-L2-Ek.png"},
            {id: 5, name: "BICEPS", desc: "Strong muscles", price: "3.89", count: "2723", new: false, listed: true, category: "sports", rarity: 1, image: "https://i.postimg.cc/K4Xf7cLq/Gifts-Gifts-Gifts-Ag-ADB3-UAAp5-V0-Uk.png"},
            {id: 6, name: "LAMP", desc: "Table lamp", price: "4.12", count: "2612", new: false, listed: true, category: "objects", rarity: 1, image: "https://i.postimg.cc/hjfNpjzc/Gifts-Gifts-Gifts-Ag-ADj-Gw-AAkl0c-Eo.png"},
            {id: 7, name: "BOUQUET", desc: "Flower bouquet", price: "4.45", count: "2501", new: false, listed: false, category: "holidays", rarity: 1, image: "https://i.postimg.cc/TY8BJTRv/Gifts-Gifts-Gifts-Ag-ADk3-AAAiy-WGEs.png"},
            {id: 8, name: "CUPCAKE", desc: "Sweet cupcake", price: "4.78", count: "2390", new: false, listed: true, category: "food", rarity: 1, image: "https://i.postimg.cc/gkqtyRS3/Gifts-Gifts-Gifts-Ag-ADB3-AAAr-Pqc-Eo.png"},
            {id: 9, name: "MARCH 8", desc: "Women's day", price: "5.12", count: "2289", new: false, listed: false, category: "holidays", rarity: 1, image: "https://i.postimg.cc/d1y4hTZk/Gifts-Gifts-Gifts-Ag-ADh2o-AAoa-Dc-Eo.png"},
            {id: 10, name: "DYSON", desc: "Powerful vacuum", price: "5.45", count: "2178", new: false, listed: true, category: "objects", rarity: 2, image: "https://i.postimg.cc/3NZjGj8R/Gifts-Gifts-Gifts-Ag-ADhmw-AAl1-Zc-Uo.png"},
            {id: 11, name: "BOILER", desc: "Steam boiler", price: "5.89", count: "2067", new: false, listed: false, category: "objects", rarity: 2, image: "https://i.postimg.cc/Dfc1Bghf/Gifts-Gifts-Gifts-Ag-ADe-WMAAp-Rw-IUs.png"},
            {id: 12, name: "CLOVER", desc: "Lucky clover", price: "6.34", count: "1956", new: false, listed: true, category: "symbols", rarity: 2, image: "https://i.postimg.cc/NfJmwjLW/Gifts-Gifts-Gifts-Ag-ADf-GYAAjfaw-Uo.png"},
            {id: 13, name: "AMULET", desc: "Protective amulet", price: "6.78", count: "1845", new: false, listed: false, category: "symbols", rarity: 2, image: "https://i.postimg.cc/hGFJSzn3/Gifts-Gifts-Gifts-Ag-AD-HEAAq-9c-Us.png"},
            {id: 14, name: "MOSQUE", desc: "Beautiful mosque", price: "7.23", count: "1734", new: false, listed: true, category: "symbols", rarity: 2, image: "https://i.postimg.cc/pr1T3ykC/Gifts-Gifts-Gifts-Ag-ADV3-MAAnv-We-Us.png"},
            {id: 15, name: "DOSHIK", desc: "Instant noodles", price: "7.89", count: "1623", new: false, listed: true, category: "food", rarity: 2, image: "https://i.postimg.cc/k5F5qTfB/Gifts-Gifts-Gifts-Ag-AD4-GQAAq8-Xg-Us.png"},
            {id: 16, name: "POOP", desc: "Funny poop", price: "8.67", count: "1512", new: false, listed: false, category: "misc", rarity: 2, image: "https://i.postimg.cc/05HykMdd/Gifts-Gifts-Gifts-Ag-AD82w-AAk-FZg-Es.png"},
            {id: 17, name: "MONKEY", desc: "Playful monkey", price: "9.45", count: "1401", new: false, listed: true, category: "animals", rarity: 2, image: "https://i.postimg.cc/bN7Yn75Z/Gifts-Gifts-Gifts-Ag-AEZAACV66-BSw.png"},
            {id: 18, name: "BRICK", desc: "Building brick", price: "10.78", count: "1290", new: false, listed: false, category: "objects", rarity: 2, image: "https://i.postimg.cc/c1jdyq0F/Gifts-Gifts-Gifts-Ag-ADg2o-AAg-R5g-Us.png"},
            {id: 19, name: "ROCKET", desc: "Space rocket", price: "12.34", count: "1189", new: false, listed: true, category: "objects", rarity: 3, image: "https://i.postimg.cc/nhfZrvs7/Gifts-Gifts-Gifts-Ag-ADIo-UAAk3-J2-Es.png"},
            {id: 20, name: "EASTER", desc: "Easter holiday", price: "13.67", count: "1078", new: false, listed: true, category: "holidays", rarity: 3, image: "https://i.postimg.cc/tTJGwkf0/Gifts-Gifts-Gifts-Ag-ADBa-UAAk8-WKEg.png"},
            {id: 21, name: "RABBIT", desc: "Fluffy rabbit", price: "15.43", count: "967", new: false, listed: false, category: "animals", rarity: 3, image: "https://i.postimg.cc/WtLRDv4j/Gifts-Gifts-Gifts-Ag-ADh-HUAAg-O6-IUg.png"},
            {id: 22, name: "1 MAY", desc: "Labor day", price: "17.89", count: "856", new: false, listed: true, category: "holidays", rarity: 3, image: "https://i.postimg.cc/gJxk8GG6/Gifts-Gifts-Gifts-Ag-ADMm4-AAj-Ll6-Ug.png"},
            {id: 23, name: "MEDAL", desc: "Gold medal", price: "19.56", count: "745", new: false, listed: true, category: "sports", rarity: 3, image: "https://i.postimg.cc/N0zQgZRG/Gifts-Gifts-Gifts-Ag-ADO3c-AAqb-DEEk.png"},
            {id: 24, name: "PIGEON", desc: "City pigeon", price: "22.78", count: "634", new: false, listed: false, category: "animals", rarity: 3, image: "https://i.postimg.cc/QxJsBFcy/Gifts-Gifts-Gifts-Ag-ADa3-QAAtw-JEEk.png"},
            {id: 25, name: "STAR", desc: "Bright star", price: "25.34", count: "512", new: false, listed: true, category: "symbols", rarity: 3, image: "https://i.postimg.cc/3Nr1nfbp/Gifts-Gifts-Gifts-Ag-ADbn-UAAl-XNEUk.png"},
            {id: 26, name: "CREAMY ICE CREAM", desc: "Creamy ice cream", price: "28.67", count: "423", new: false, listed: true, category: "food", rarity: 4, image: "https://i.postimg.cc/ydjXgXYN/Gifts-Gifts-Gifts-Ag-AD0-Ww-AAs4-T4-Ek.png"},
            {id: 27, name: "ESKIMO", desc: "Eskimo ice cream", price: "32.45", count: "345", new: false, listed: false, category: "food", rarity: 4, image: "https://i.postimg.cc/L4y3mTbC/Gifts-Gifts-Gifts-Ag-ADy-XEAAky04-Ek.png"},
            {id: 28, name: "PLUMBER", desc: "Plumber", price: "38.90", count: "267", new: true, listed: true, category: "misc", rarity: 4, image: "https://i.postimg.cc/85pLSJBg/Gifts-Gifts-Gifts-Ag-ADKX4-AAuw-O2-Ek.png"},
            {id: 29, name: "NIPPLE", desc: "Golden nipple", price: "45.78", count: "203", new: true, listed: true, category: "misc", rarity: 4, image: "https://i.postimg.cc/BQrDvwcg/Gifts-Gifts-Gifts-Ag-ADD3-IAAm-RNKUo.png"},
            {id: 30, name: "EAGLE", desc: "Symbol of freedom", price: "54.67", count: "156", new: true, listed: true, category: "symbols", rarity: 5, image: "https://i.postimg.cc/0QXK1ty7/Gifts-Gifts-Gifts-Ag-ADzn-IAAl-Gn-QEs.png"},
            {id: 31, name: "STATUE", desc: "Statue of Liberty", price: "65.43", count: "112", new: true, listed: true, category: "symbols", rarity: 5, image: "https://i.postimg.cc/V6hvVdKR/Gifts-Gifts-Gifts-Ag-ADi-IYAAqf-LQEs.png"},
            {id: 32, name: "TORCH", desc: "Torch of freedom", price: "76.89", count: "89", new: true, listed: true, category: "symbols", rarity: 5, image: "https://i.postimg.cc/wv1LMKPw/Gifts-Gifts-Gifts-Ag-AD2-XQAAk-VPSEs.png"},
            {id: 33, name: "WESTSIDE SIGN", desc: "West coast sign", price: "87.32", count: "67", new: true, listed: true, category: "symbols", rarity: 5, image: "https://i.postimg.cc/GtkBTbjx/Gifts-Gifts-Gifts-Ag-ADV4-QAAiibe-Us.png"},
            {id: 34, name: "LOW RIDER", desc: "Cool car", price: "98.45", count: "23", new: true, listed: true, category: "entertainment", rarity: 5, image: "https://i.postimg.cc/7Y96Fsth/Gifts-Gifts-Gifts-Ag-ADNWw-AAg5ze-Es.png"},
            {id: 35, name: "SNOOP CIGAR", desc: "Elite cigar", price: "134.56", count: "45", new: true, listed: true, category: "entertainment", rarity: 5, image: "https://i.postimg.cc/FKMsy2zW/Gifts-Gifts-Gifts-Ag-ADi38-AAg-7c-Es.png"},
            {id: 36, name: "SWAG BAG", desc: "Stylish bag", price: "156.78", count: "34", new: true, listed: true, category: "fashion", rarity: 5, image: "https://i.postimg.cc/d1cwkrNg/Gifts-Gifts-Gifts-Ag-AD5-XMAAmjze-Us.png"},
            {id: 37, name: "SNOOP DOGG", desc: "Legendary rapper", price: "208.354", count: "15", new: true, listed: true, category: "entertainment", rarity: 5, image: "https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"}
        ];
        
        let currentView = 'market';
        let selectedFilter = null; // Выбранный подарок для фильтрации
        let currentFilters = {
            giftType: '',
            sort: 'recent'
        };
        
        // Применение фильтров
        function applyFilters() {
            if (currentView !== 'market') return;
            
            if (selectedFilter) {
                applyGiftNameFilter();
                return;
            }
            
            const giftTypeFilter = document.getElementById('giftTypeFilter').value;
            const sortFilter = document.getElementById('sortFilter').value;
            
            currentFilters.giftType = giftTypeFilter;
            currentFilters.sort = sortFilter;
            
            let filteredGifts = allGifts.filter(gift => gift.listed);
            
            // Фильтр по типу подарка
            if (giftTypeFilter) {
                filteredGifts = filteredGifts.filter(gift => gift.category === giftTypeFilter);
            }
            
            // Сортировка
            switch (sortFilter) {
                case 'recent':
                    // По умолчанию (новые сначала, потом по ID)
                    filteredGifts.sort((a, b) => b.new - a.new || b.id - a.id);
                    break;
                case 'price_asc':
                    filteredGifts.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
                    break;
                case 'price_desc':
                    filteredGifts.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
                    break;
                case 'rarity':
                    filteredGifts.sort((a, b) => b.rarity - a.rarity);
                    break;
            }
            
            renderGifts(filteredGifts);
        }
        
        // Очистка фильтров
        function clearFilters() {
            document.getElementById('giftTypeFilter').value = '';
            document.getElementById('sortFilter').value = 'recent';
            selectedFilter = null;
            currentFilters = {
                giftType: '',
                sort: 'recent'
            };
            applyFilters();
        }
        
        // Показать только listed подарки в Market
        function showMarket() {
            document.getElementById('filtersSection').classList.remove('filters-hidden');
            applyFilters();
        }
        
        // Показать страницу фильтра - ВСЕ подарки как на фото
        function showFilter() {
            currentView = 'filter';
            document.getElementById('filtersSection').classList.add('filters-hidden');
            
            // Обновляем активную вкладку
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab')[1].classList.add('active'); // "Все подарки" активная
            
            const grid = document.getElementById('giftsGrid');
            
            // Показываем ВСЕ подарки как отдельные элементы (как на фото)
            const allListedGifts = allGifts.filter(gift => gift.listed);
            
            grid.innerHTML = `
                <div style="grid-column: 1/-1;">
                    <div class="filter-list">
                        ${allListedGifts.map(gift => `
                            <div class="filter-item ${selectedFilter === gift.name ? 'selected' : ''}" onclick="selectGiftFilter('${gift.name}')">
                                <div class="filter-item-image" style="background-image: url('${gift.image}')"></div>
                                <div class="filter-item-content">
                                    <div class="filter-item-name">${gift.name}</div>
                                    <div class="filter-item-price">${gift.price} ▼ (${gift.count} 🎁)</div>
                                </div>
                                ${gift.new ? '<div class="filter-item-badge">NEW!</div>' : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
        
        // Выбор подарка для фильтрации
        function selectGiftFilter(giftName) {
            selectedFilter = giftName;
            // Переключаемся на Market и показываем только выбранный тип подарка
            currentView = 'market';
            
            // Обновляем активную вкладку на Market
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab')[0].classList.add('active'); // Market активный
            document.querySelectorAll('.nav-item')[0].classList.add('active');
            
            // Показываем фильтры и применяем выбранный подарок
            document.getElementById('filtersSection').classList.remove('filters-hidden');
            applyGiftNameFilter();
        }
        
        // Очистка фильтра подарков
        function clearGiftFilter() {
            selectedFilter = null;
            // Остаемся в Market но показываем все подарки
            currentView = 'market';
            
            // Обновляем активную вкладку
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab')[0].classList.add('active'); // Market активный
            
            showMarket();
        }
        
        // Применение фильтра по названию подарка
        function applyGiftNameFilter() {
            if (!selectedFilter) {
                applyFilters();
                return;
            }
            
            let filteredGifts = allGifts.filter(gift => gift.listed && gift.name === selectedFilter);
            
            // Применяем сортировку
            switch (currentFilters.sort) {
                case 'recent':
                    filteredGifts.sort((a, b) => b.new - a.new || b.id - a.id);
                    break;
                case 'price_asc':
                    filteredGifts.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
                    break;
                case 'price_desc':
                    filteredGifts.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
                    break;
                case 'rarity':
                    filteredGifts.sort((a, b) => b.rarity - a.rarity);
                    break;
            }
            
            renderGifts(filteredGifts);
        }
        
        // Показать каталог - только фото и названия
        function showCatalog() {
            document.getElementById('filtersSection').classList.add('filters-hidden');
            const grid = document.getElementById('giftsGrid');
            grid.innerHTML = allGifts.map(gift => `
                <div class="gift-card-catalog" onclick="selectGift(${gift.id})">
                    <div class="gift-id">#${gift.id}</div>
                    <div class="gift-image-catalog" style="background-image: url('${gift.image}')"></div>
                    <div class="gift-name-catalog">${gift.name}</div>
                </div>
            `).join('');
        }
        
        // Показать My Gifts - простая пустая страница
        function showMyGifts() {
            document.getElementById('filtersSection').classList.add('filters-hidden');
            const grid = document.getElementById('giftsGrid');
            grid.innerHTML = `
                <div class="empty-state">
                    <div style="font-size: 48px; margin-bottom: 15px;">📦</div>
                    <div style="font-size: 16px; margin-bottom: 8px;">У вас пока нет подарков</div>
                    <div style="font-size: 14px;">Купите подарки в Market чтобы увидеть их здесь</div>
                </div>
            `;
        }
        
        // Выбор подарка в каталоге
        function selectGift(id) {
            const gift = allGifts.find(g => g.id === id);
            tg.showAlert(`Выбран подарок #${id}: ${gift.name}`);
        }
        
        // Рендер подарков (только для Market)
        function renderGifts(gifts) {
            const grid = document.getElementById('giftsGrid');
            
            if (gifts.length === 0) {
                grid.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 16px; margin-bottom: 8px;">Подарки не найдены</div>
                        <div style="font-size: 14px;">Попробуйте изменить фильтры или поисковый запрос</div>
                    </div>
                `;
                return;
            }
            
            grid.innerHTML = gifts.map(gift => `
                <div class="gift-card">
                    <div class="gift-id">#${gift.id}</div>
                    <div class="gift-image" style="background-image: url('${gift.image}')"></div>
                    <div class="gift-title">
                        ${gift.name}
                        ${gift.new ? '<span class="new-badge">NEW!</span>' : ''}
                    </div>
                    <button class="price-btn" onclick="buyGift(${gift.id})">
                        <span>${gift.price}</span>
                        <span class="triangle-icon">▼</span>
                        <span>(${gift.count})</span>
                    </button>
                </div>
            `).join('');
        }
        
        // Переключение вкладок
        function switchTab(tab) {
            currentView = tab;
            
            // Обновляем активную вкладку
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            
            if (tab === 'market') {
                document.querySelectorAll('.tab')[0].classList.add('active');
                document.querySelectorAll('.nav-item')[0].classList.add('active');
                showMarket();
            } else if (tab === 'catalog') {
                document.querySelectorAll('.tab')[2].classList.add('active');
                showCatalog();
            } else if (tab === 'my-gifts') {
                document.querySelectorAll('.tab')[3].classList.add('active');
                document.querySelectorAll('.nav-item')[1].classList.add('active');
                showMyGifts();
            }
        }
        
        // Поиск подарков
        function searchGifts() {
            const query = document.getElementById('searchBox').value.toLowerCase();
            
            if (currentView === 'my-gifts') return;
            
            if (query === '') {
                if (currentView === 'market') {
                    applyFilters();
                } else if (currentView === 'catalog') {
                    showCatalog();
                }
                return;
            }
            
            if (currentView === 'market') {
                let baseGifts = allGifts.filter(gift => gift.listed);
                
                // Если выбран конкретный подарок
                if (selectedFilter) {
                    baseGifts = baseGifts.filter(gift => gift.name === selectedFilter);
                } else {
                    // Применяем фильтры категорий
                    if (currentFilters.giftType) {
                        baseGifts = baseGifts.filter(gift => gift.category === currentFilters.giftType);
                    }
                }
                
                const filtered = baseGifts.filter(gift => 
                    gift.name.toLowerCase().includes(query) || 
                    gift.id.toString().includes(query)
                );
                
                // Применяем сортировку
                switch (currentFilters.sort) {
                    case 'recent':
                        filtered.sort((a, b) => b.new - a.new || b.id - a.id);
                        break;
                    case 'price_asc':
                        filtered.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
                        break;
                    case 'price_desc':
                        filtered.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
                        break;
                    case 'rarity':
                        filtered.sort((a, b) => b.rarity - a.rarity);
                        break;
                }
                
                renderGifts(filtered);
            }
        }
        
        // Покупка подарка
        function buyGift(id) {
            const gift = allGifts.find(g => g.id === id);
            tg.showAlert(`Покупаем подарок #${id}: ${gift.name} за ${gift.price} ▼`);
        }
        
        // Инициализация
        document.addEventListener('DOMContentLoaded', () => {
            showMarket();
        });
        
        // Главная кнопка Telegram
        tg.MainButton.text = "Готово";
        tg.MainButton.show();
        tg.MainButton.onClick(() => { 
            tg.close();
        });
        
        // Адаптация к теме
        if (tg.colorScheme === 'dark') {
            document.body.style.background = '#0f0f1a';
        }
    </script>
</body>
</html>
    """

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
        f"🎁 37 уникальных подарков\n"
        f"🔍 Поиск по ID и названию\n"
        f"💎 Редкие и обычные подарки\n"
        f"🔧 Фильтры по типу и цене\n\n"
        f"Нажми кнопку чтобы открыть каталог:",
        reply_markup=keyboard
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
    
    print("🎁 GiftRoom Market с фильтрами запущен!")
    print(f"🌐 URL: {WEBAPP_URL}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
