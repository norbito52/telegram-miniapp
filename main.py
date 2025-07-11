# main.py - FastAPI приложение для GiftRoom Market с My Channel
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
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #2a2a3e;
            border-radius: 12px;
            padding: 12px 15px;
            margin-bottom: 20px;
        }
        
        .wallet-connect-btn {
            background: transparent;
            color: #0088ff;
            border: none;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .wallet-connect-btn:hover {
            color: #006dd9;
        }
        
        .balance-section {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .balance-btn {
            background: #2196F3;
            color: white;
            border: none;
            padding: 6px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 14px;
            width: 28px;
            height: 28px;
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
            font-size: 14px;
            font-weight: 600;
            min-width: 70px;
            text-align: center;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .ton-icon {
            width: 18px;
            height: 18px;
            background-image: url('https://i.postimg.cc/kX2nWB4M/121-20250711185549.png');
            background-size: cover;
            background-position: center;
            border-radius: 50%;
            flex-shrink: 0;
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
        
        .gift-group-card {
            background: #2a2a3e;
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            transition: transform 0.3s ease;
            min-height: 200px;
            position: relative;
            cursor: pointer;
        }
        
        .gift-group-card:hover {
            transform: translateY(-2px);
        }
        
        .gift-group-images {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 15px;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .gift-group-images.single {
            justify-content: center;
        }
        
        .gift-group-images.double {
            justify-content: space-around;
        }
        
        .gift-group-images.triple {
            justify-content: space-between;
        }
        
        .gift-group-image {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            background-size: cover;
            background-position: center;
            border: 2px solid #3a3a5c;
            flex-shrink: 0;
        }
        
        .gift-group-image.single {
            width: 80px;
            height: 80px;
        }
        
        .gift-group-image.double {
            width: 60px;
            height: 60px;
        }
        
        .gift-group-image.triple {
            width: 45px;
            height: 45px;
        }
        
        .gift-group-count {
            position: absolute;
            top: 12px;
            right: 12px;
            background: rgba(0,0,0,0.7);
            color: white;
            font-size: 14px;
            padding: 4px 8px;
            border-radius: 8px;
            font-weight: 600;
        }
        
        .gift-group-title {
            color: white;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 15px;
        }
        
        .gift-id {
            display: none;
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
        
        /* My Channel Styles - в стиле старого интерфейса */
        .channel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }
        
        .channel-title {
            color: white;
            font-size: 20px;
            font-weight: 500;
        }
        
        .add-ad-btn {
            background: #3d5afe;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 18px;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        .add-ad-btn:hover {
            background: #2c47e8;
            transform: scale(1.05);
        }
        
        .empty-channel {
            text-align: center;
            padding: 40px;
            color: #8b8b8b;
        }
        
        .empty-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }
        
        .empty-title {
            font-size: 16px;
            color: #ffffff;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        .empty-subtitle {
            font-size: 14px;
            color: #8b8b8b;
            margin-bottom: 25px;
            line-height: 1.3;
        }
        
        .create-ad-btn {
            background: #3d5afe;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .create-ad-btn:hover {
            background: #2c47e8;
            transform: translateY(-1px);
        }
        
        .bottom-nav {
            display: none;
        }
        
        .nav-item {
            flex: 1;
            text-align: center;
            padding: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            border-radius: 12px;
            font-weight: 600;
        }
        
        .nav-item.active {
            background: #3d5afe;
            color: white;
        }
        
        .nav-item:not(.active) {
            background: #2a2a3e;
            color: #8b8b8b;
        }
        
        .nav-text {
            font-size: 16px;
            font-weight: 600;
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
        
        /* Modal overlay for gift filter */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            z-index: 1000;
            display: none;
        }
        
        .modal-overlay.show {
            display: block;
        }
        
        .modal-content {
            background: #1a1a2e;
            margin: 0;
            height: 100vh;
            overflow-y: auto;
            position: relative;
        }
        
        .modal-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px;
            border-bottom: 1px solid #2a2a3e;
            position: sticky;
            top: 0;
            background: #1a1a2e;
            z-index: 10;
        }
        
        .modal-title {
            color: white;
            font-size: 18px;
            font-weight: 600;
        }
        
        .modal-close {
            background: none;
            border: none;
            color: #8b8b8b;
            font-size: 24px;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .modal-search {
            background: #2a2a3e;
            border: none;
            padding: 12px 40px 12px 15px;
            border-radius: 10px;
            color: white;
            width: 100%;
            margin: 0 20px 20px 20px;
            font-size: 16px;
            position: relative;
        }
        
        .modal-search::placeholder {
            color: #8b8b8b;
        }
        
        .gift-options-list {
            padding: 0 20px 100px 20px;
        }
        
        .gift-option {
            display: flex;
            align-items: center;
            padding: 15px 0;
            cursor: pointer;
            border-bottom: 1px solid #2a2a3e;
        }
        
        .gift-option:last-child {
            border-bottom: none;
        }
        
        .gift-option-radio {
            width: 20px;
            height: 20px;
            border: 2px solid #4a4a5e;
            border-radius: 50%;
            margin-right: 15px;
            position: relative;
            flex-shrink: 0;
        }
        
        .gift-option.selected .gift-option-radio {
            border-color: #3d5afe;
        }
        
        .gift-option.selected .gift-option-radio::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 10px;
            height: 10px;
            background: #3d5afe;
            border-radius: 50%;
        }
        
        .gift-option-image {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            margin-right: 15px;
            background-size: cover;
            background-position: center;
            border: 2px solid #3a3a5c;
            flex-shrink: 0;
        }
        
        .gift-option-name {
            color: white;
            font-size: 16px;
            font-weight: 500;
        }
        
        .modal-buttons {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #1a1a2e;
            padding: 20px;
            display: flex;
            gap: 15px;
            border-top: 1px solid #2a2a3e;
        }
        
        .modal-btn {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .modal-btn.cancel {
            background: #4a4a5e;
            color: white;
        }
        
        .modal-btn.cancel:hover {
            background: #5a5a6e;
        }
        
        .modal-btn.select {
            background: #3d5afe;
            color: white;
        }
        
        .modal-btn.select:hover {
            background: #2c47e8;
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
        
        /* Gift Detail Modal */
        .gift-detail-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
        }
        
        .gift-detail-modal.show {
            display: flex;
        }
        
        .gift-detail-content {
            background: #2a2a3e;
            border-radius: 20px;
            padding: 30px;
            max-width: 320px;
            width: 100%;
            text-align: center;
            position: relative;
        }
        
        .gift-detail-close {
            position: absolute;
            top: 15px;
            right: 15px;
            background: #4a4a5e;
            border: none;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .gift-detail-image {
            width: 120px;
            height: 120px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            margin: 0 auto 20px;
            background-size: cover;
            background-position: center;
            border: 3px solid #3a3a5c;
        }
        
        .gift-detail-title {
            color: white;
            font-size: 20px;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        
        .gift-detail-id {
            color: #8b8b8b;
            font-size: 14px;
            margin-bottom: 15px;
        }
        
        .gift-detail-description {
            color: #8b8b8b;
            font-size: 14px;
            line-height: 1.4;
            margin-bottom: 25px;
            min-height: 40px;
        }
        
        .gift-detail-price {
            background: #2196F3;
            color: white;
            border: none;
            padding: 15px;
            border-radius: 12px;
            width: 100%;
            font-weight: 600;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>GiftRoom Market</h1>
        <div class="subtitle">Магазин подарков в Telegram</div>
        
        <div class="wallet-section">
            <button class="wallet-connect-btn" onclick="connectWallet()">TON кошелек</button>
            <div class="balance-section">
                <button class="balance-btn minus" onclick="withdrawBalance()">−</button>
                <div class="balance-display">
                    <div class="ton-icon"></div>
                    <span>0.00 TON</span>
                </div>
                <button class="balance-btn" onclick="addBalance()">+</button>
            </div>
        </div>
    </div>
    
    <div class="tabs">
        <div class="tab active" onclick="switchTab('market')">Market</div>
        <div class="tab" onclick="openGiftModal()">Collections</div>
        <div class="tab" onclick="switchTab('my-channel')">My Channel</div>
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
    
    <div class="bottom-nav" style="display: none;">
        <div class="nav-item active" onclick="switchTab('market')">
            <div class="nav-text">Market</div>
        </div>
        <div class="nav-item" onclick="switchTab('my-channel')">
            <div class="nav-text">My Channel</div>
        </div>
    </div>
    
    <!-- Modal для выбора подарков -->
    <div class="modal-overlay" id="giftModal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">Выберите вид подарка</div>
                <button class="modal-close" onclick="closeGiftModal()">✕</button>
            </div>
            
            <input type="text" class="modal-search" placeholder="Поиск" id="modalSearchBox" onkeyup="filterModalGifts()">
            
            <div class="gift-options-list" id="giftOptionsList">
                <!-- Список подарков будет сгенерирован здесь -->
            </div>
            
            <div class="modal-buttons">
                <button class="modal-btn cancel" onclick="closeGiftModal()">Отмена</button>
                <button class="modal-btn select" onclick="selectModalGift()">Выбрать</button>
            </div>
        </div>
    </div>
    
    <!-- Modal для деталей подарка -->
    <div class="gift-detail-modal" id="giftDetailModal">
        <div class="gift-detail-content">
            <button class="gift-detail-close" onclick="closeGiftDetail()">✕</button>
            <div class="gift-detail-image" id="giftDetailImage"></div>
            <div class="gift-detail-title" id="giftDetailTitle"></div>
            <div class="gift-detail-id" id="giftDetailId"></div>
            <div class="gift-detail-description" id="giftDetailDescription">
                <!-- Описание будет добавлено позже -->
            </div>
            <button class="gift-detail-price" id="giftDetailPrice" onclick="buyGiftFromDetail()">
                <span id="giftDetailPriceText"></span>
                <span class="triangle-icon">▼</span>
                <span id="giftDetailCount"></span>
            </button>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        // База данных всех подарков
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
        let selectedFilter = null;
        let tempSelectedGift = null;
        let currentFilters = {
            giftType: '',
            sort: 'recent'
        };
        
        // Зберігаємо групи глобально для доступу
        let currentMixedGroups = [];
        
        // Створюємо мікс-групи різних подарків для тестування  
        function createMixedGroups(gifts) {
            const mixedGroups = [];
            
            // Група 1: 3 різних подарка - SNOOP DOGG + EAGLE + LOW RIDER
            const group1 = [
                gifts.find(g => g.name === "SNOOP DOGG" && g.id === 37),
                gifts.find(g => g.name === "EAGLE" && g.id === 30),
                gifts.find(g => g.name === "LOW RIDER" && g.id === 34)
            ].filter(Boolean);
            if (group1.length > 0) mixedGroups.push(group1);
            
            // Група 2: 2 різних подарка - CATS + HEELS  
            const group2 = [
                gifts.find(g => g.name === "CATS" && g.id === 3),
                gifts.find(g => g.name === "HEELS" && g.id === 1)
            ].filter(Boolean);
            if (group2.length > 0) mixedGroups.push(group2);
            
            // Група 3: 3 різних подарка - SWAG BAG + TORCH + WESTSIDE SIGN
            const group3 = [
                gifts.find(g => g.name === "SWAG BAG" && g.id === 36),
                gifts.find(g => g.name === "TORCH" && g.id === 32),
                gifts.find(g => g.name === "WESTSIDE SIGN" && g.id === 33)
            ].filter(Boolean);
            if (group3.length > 0) mixedGroups.push(group3);
            
            // Решта подарків поодинці
            const usedIds = new Set();
            mixedGroups.forEach(group => {
                group.forEach(gift => usedIds.add(gift.id));
            });
            
            const singleGifts = gifts.filter(gift => !usedIds.has(gift.id));
            singleGifts.forEach(gift => {
                mixedGroups.push([gift]);
            });
            
            return mixedGroups;
        }
        
        // Визначаємо основну назву групи (від підарка якого найбільше)
        function getGroupMainName(group) {
            const nameCounts = {};
            group.forEach(gift => {
                nameCounts[gift.name] = (nameCounts[gift.name] || 0) + parseInt(gift.count);
            });
            
            let maxCount = 0;
            let mainName = group[0].name;
            
            Object.entries(nameCounts).forEach(([name, count]) => {
                if (count > maxCount) {
                    maxCount = count;
                    mainName = name;
                }
            });
            
            return mainName;
        }
        
        // Рендер мікс-груп подарків
        function renderMixedGifts(gifts) {
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
            
            currentMixedGroups = createMixedGroups(gifts);
            
            grid.innerHTML = currentMixedGroups.map((group, index) => {
                const count = group.length;
                const mainName = getGroupMainName(group);
                
                let imageClass = 'single';
                let containerClass = 'single';
                if (count === 2) {
                    imageClass = 'double';
                    containerClass = 'double';
                } else if (count >= 3) {
                    imageClass = 'triple';
                    containerClass = 'triple';
                }
                
                const imagesToShow = group.slice(0, 3);
                
                return `
                    <div class="gift-group-card" onclick="openMixedGroupDetail(${index})">
                        <div class="gift-group-count">${count}</div>
                        <div class="gift-group-images ${containerClass}">
                            ${imagesToShow.map(gift => `
                                <div class="gift-group-image ${imageClass}" style="background-image: url('${gift.image}')"></div>
                            `).join('')}
                        </div>
                        <div class="gift-group-title">${mainName}</div>
                        <button class="price-btn" onclick="event.stopPropagation(); showMixedGroupPrices(${index})">
                            Ціна в TON
                        </button>
                    </div>
                `;
            }).join('');
        }
        
        // Открыть детали смешанной группы подарков
        function openMixedGroupDetail(groupIndex) {
            const group = currentMixedGroups[groupIndex];
            if (!group) return;
            
            if (group.length === 1) {
                // Если один подарок, открываем обычное модальное окно
                openGiftDetail(group[0].id);
            } else {
                // Если несколько, показываем информацию о группе
                const mainName = getGroupMainName(group);
                const giftNames = [...new Set(group.map(g => g.name))];
                const info = `Группа "${mainName}"\n\nВ группе: ${giftNames.join(', ')}\nВсего подарков: ${group.length}`;
                tg.showAlert(info);
            }
        }
        
        // Показать цены смешанной группы подарков
        function showMixedGroupPrices(groupIndex) {
            const group = currentMixedGroups[groupIndex];
            if (!group) return;
            
            const pricesInfo = group.map(gift => 
                `${gift.name}: ${gift.price} ▼ (${gift.count})`
            ).join('\n');
            tg.showAlert(`Цены в группе:\n\n${pricesInfo}`);
        }
        
        // Применение фильтров
        function applyFilters() {
            if (currentView === 'market') {
                applyMarketFilters();
            }
        }
        
        // Применение фильтров в Market
        function applyMarketFilters() {
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
            
            renderMixedGifts(filteredGifts);
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
            
            if (currentView === 'market') {
                applyMarketFilters();
            } else if (currentView === 'catalog') {
                showCatalog();
            }
        }
        
        // Показать только listed подарки в Market
        function showMarket() {
            document.getElementById('filtersSection').classList.remove('filters-hidden');
            applyMarketFilters();
        }
        
        // Показать My Channel в стиле старого интерфейса
        function showMyChannel() {
            document.getElementById('filtersSection').classList.add('filters-hidden');
            const grid = document.getElementById('giftsGrid');
            grid.innerHTML = `
                <div class="channel-header">
                    <div class="channel-title">Мои объявления</div>
                    <button class="add-ad-btn" onclick="createAd()" title="Добавить объявление">+</button>
                </div>
                <div class="empty-channel">
                    <div class="empty-icon">📦</div>
                    <div class="empty-title">Нет объявлений</div>
                    <div class="empty-subtitle">Создайте ваше первое объявление</div>
                    <button class="create-ad-btn" onclick="createAd()">Добавить объявление</button>
                </div>
            `;
        }
        
        function openGiftModal() {
            const modal = document.getElementById('giftModal');
            const optionsList = document.getElementById('giftOptionsList');
            
            // Создаем список всех уникальных подарков
            const giftGroups = {};
            allGifts.forEach(gift => {
                if (!giftGroups[gift.name]) {
                    giftGroups[gift.name] = {
                        name: gift.name,
                        image: gift.image,
                        new: gift.new
                    };
                }
            });
            
            const uniqueGifts = Object.values(giftGroups);
            
            // Добавляем опцию "Все подарки"
            const allGiftsOption = {
                name: 'Все подарки',
                image: '',
                new: false,
                isAll: true
            };
            
            const options = [allGiftsOption, ...uniqueGifts];
            
            optionsList.innerHTML = options.map(gift => `
                <div class="gift-option ${(!selectedFilter && gift.isAll) || selectedFilter === gift.name ? 'selected' : ''}" 
                     onclick="selectModalOption('${gift.isAll ? '' : gift.name}', this)">
                    <div class="gift-option-radio"></div>
                    ${gift.isAll ? '' : `<div class="gift-option-image" style="background-image: url('${gift.image}')"></div>`}
                    <div class="gift-option-name">${gift.name}</div>
                </div>
            `).join('');
            
            // Устанавливаем текущий выбор
            tempSelectedGift = selectedFilter;
            
            modal.classList.add('show');
        }
        
        function closeGiftModal() {
            const modal = document.getElementById('giftModal');
            modal.classList.remove('show');
            tempSelectedGift = null;
        }
        
        function selectModalOption(giftName, element) {
            // Убираем выделение с предыдущего элемента
            document.querySelectorAll('.gift-option').forEach(opt => opt.classList.remove('selected'));
            
            // Выделяем текущий элемент
            element.classList.add('selected');
            
            // Сохраняем временный выбор
            tempSelectedGift = giftName === '' ? null : giftName;
        }
        
        function selectModalGift() {
            // Применяем выбор
            selectedFilter = tempSelectedGift;
            
            // Закрываем модальное окно
            closeGiftModal();
            
            // Переключаемся на Collections и применяем фильтр
            currentView = 'catalog';
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab')[1].classList.add('active');
            
            showCatalog();
        }
        
        function filterModalGifts() {
            const query = document.getElementById('modalSearchBox').value.toLowerCase();
            const options = document.querySelectorAll('.gift-option');
            
            options.forEach(option => {
                const name = option.querySelector('.gift-option-name').textContent.toLowerCase();
                if (name.includes(query)) {
                    option.style.display = 'flex';
                } else {
                    option.style.display = 'none';
                }
            });
        }
        
        // Показать каталог - с выборочным показом подарков
        function showCatalog() {
            document.getElementById('filtersSection').classList.add('filters-hidden');
            
            if (selectedFilter) {
                // Показываем только выбранный тип подарка
                const filteredGifts = allGifts.filter(gift => gift.name === selectedFilter);
                const sortedGifts = filteredGifts.sort((a, b) => b.id - a.id);
                renderCatalogGifts(sortedGifts);
            } else {
                // Показываем все подарки
                const sortedGifts = [...allGifts].sort((a, b) => b.id - a.id);
                renderCatalogGifts(sortedGifts);
            }
        }
        
        // Рендер подарков в Collections
        function renderCatalogGifts(gifts) {
            const grid = document.getElementById('giftsGrid');
            
            if (gifts.length === 0) {
                grid.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 16px; margin-bottom: 8px;">Подарки не найдены</div>
                        <div style="font-size: 14px;">Попробуйте изменить фильтры</div>
                    </div>
                `;
                return;
            }
            
            grid.innerHTML = gifts.map(gift => `
                <div class="gift-card-catalog" onclick="selectGift(${gift.id})">
                    <div class="gift-id">#${gift.id}</div>
                    <div class="gift-image-catalog" style="background-image: url('${gift.image}')"></div>
                    <div class="gift-name-catalog">${gift.name}</div>
                </div>
            `).join('');
        }
        
        // Выбор подарка в каталоге
        function selectGift(id) {
            const gift = allGifts.find(g => g.id === id);
            tg.showAlert(`Выбран подарок #${id}: ${gift.name}`);
        }
        
        // Переключение вкладок
        function switchTab(tab) {
            currentView = tab;
            
            // Обновляем активную вкладку в верхних табах
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            
            if (tab === 'market') {
                document.querySelectorAll('.tab')[0].classList.add('active');
                showMarket();
            } else if (tab === 'catalog') {
                document.querySelectorAll('.tab')[1].classList.add('active');
                showCatalog();
            } else if (tab === 'my-channel') {
                document.querySelectorAll('.tab')[2].classList.add('active');
                showMyChannel();
            }
        }
        
        // Створюємо змінну для поточного подарка
        let currentGiftDetail = null;
        
        function openGiftDetail(giftId) {
            const gift = allGifts.find(g => g.id === giftId);
            if (!gift) return;
            
            currentGiftDetail = gift;
            
            document.getElementById('giftDetailImage').style.backgroundImage = `url('${gift.image}')`;
            document.getElementById('giftDetailTitle').textContent = gift.name;
            document.getElementById('giftDetailId').textContent = `#${gift.id}`;
            document.getElementById('giftDetailPriceText').textContent = gift.price;
            document.getElementById('giftDetailCount').textContent = `(${gift.count})`;
            
            document.getElementById('giftDetailModal').classList.add('show');
        }
        
        // Закрыть детали подарка
        function closeGiftDetail() {
            document.getElementById('giftDetailModal').classList.remove('show');
            currentGiftDetail = null;
        }
        
        // Купить подарок из детального просмотра
        function buyGiftFromDetail() {
            if (currentGiftDetail) {
                buyGift(currentGiftDetail.id);
                closeGiftDetail();
            }
        }
        
        // Создание объявления
        function createAd() {
            tg.showAlert("Функция создания объявления будет добавлена в следующем обновлении!");
        }
        
        // Закрытие модальных окон при клике на фон
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('gift-detail-modal')) {
                closeGiftDetail();
            }
        });
        
        // Покупка подарка
        function buyGift(id) {
            const gift = allGifts.find(g => g.id === id);
            tg.showAlert(`Покупаем подарок #${id}: ${gift.name} за ${gift.price} ▼`);
        }
        
        // Инициализация
        document.addEventListener('DOMContentLoaded', () => {
            showMarket();
        });
        
        // Убираем главную кнопку Telegram
        tg.MainButton.hide();
        
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
    
    print("🎁 GiftRoom Market з My Channel запущен!")
    print(f"🌐 URL: {WEBAPP_URL}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
