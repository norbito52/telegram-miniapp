 # main.py - FastAPI приложение для ChannelGift Market - торговля Telegram каналами с подарками
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
    <title>ChannelGift Market</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        /* Loading Screen Styles */
        .loading-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            animation: fadeIn 0.5s ease-out;
        }
        
        .loading-screen.hidden {
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.8s ease-out;
        }
        
        /* Logo Animation */
        .loading-logo {
            width: 140px;
            height: 140px;
            background: linear-gradient(135deg, #4285f4 0%, #34a853 25%, #fbbc05 50%, #ea4335 75%);
            border-radius: 35px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 56px;
            margin-bottom: 35px;
            animation: pulse 2s ease-in-out infinite;
            box-shadow: 0 25px 50px rgba(66, 133, 244, 0.4);
            position: relative;
        }
        
        .loading-logo::before {
            content: '';
            position: absolute;
            width: 160px;
            height: 160px;
            border: 3px solid rgba(255, 255, 255, 0.1);
            border-radius: 40px;
            animation: rotate 3s linear infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        /* Title Animation */
        .loading-title {
            font-size: 36px;
            font-weight: 800;
            background: linear-gradient(135deg, #4285f4, #34a853, #fbbc05);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 12px;
            animation: slideUp 1s ease-out 0.3s both;
            text-align: center;
        }
        
        .loading-subtitle {
            font-size: 18px;
            color: #8b8b8b;
            margin-bottom: 45px;
            animation: slideUp 1s ease-out 0.5s both;
            text-align: center;
            font-weight: 500;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Channel Loading Animation */
        .channel-loader {
            display: flex;
            gap: 20px;
            margin-bottom: 35px;
            animation: slideUp 1s ease-out 0.7s both;
        }
        
        .channel-box {
            width: 50px;
            height: 50px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 12px;
            animation: bounce 1.8s ease-in-out infinite;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .channel-box:nth-child(1) { 
            animation-delay: 0s; 
            background: linear-gradient(45deg, #4285f4, #1976d2);
        }
        .channel-box:nth-child(2) { 
            animation-delay: 0.3s; 
            background: linear-gradient(45deg, #34a853, #2e7d32);
        }
        .channel-box:nth-child(3) { 
            animation-delay: 0.6s; 
            background: linear-gradient(45deg, #fbbc05, #f57c00);
        }
        
        .channel-box::before {
            content: '📺';
            font-size: 24px;
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-20px);
            }
            60% {
                transform: translateY(-10px);
            }
        }
        
        /* Progress Bar */
        .progress-container {
            width: 250px;
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            overflow: hidden;
            margin-bottom: 25px;
            animation: slideUp 1s ease-out 0.9s both;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #4285f4, #34a853, #fbbc05);
            border-radius: 3px;
            animation: loadProgress 3.5s ease-out;
        }
        
        @keyframes loadProgress {
            from { width: 0%; }
            to { width: 100%; }
        }
        
        /* Loading Text */
        .loading-text {
            color: #8b8b8b;
            font-size: 16px;
            font-weight: 500;
            animation: slideUp 1s ease-out 1.1s both;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* Main App Container */
        .main-app {
            opacity: 0;
            transition: opacity 0.8s ease-in;
        }
        
        .main-app.visible {
            opacity: 1;
        }
        
        .new-badge {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            font-size: 10px;
            padding: 3px 8px;
            border-radius: 10px;
            font-weight: 700;
            margin-left: 6px;
            box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
        }
        
        .hot-badge {
            background: linear-gradient(135deg, #ff4757, #ff3742);
            color: white;
            font-size: 10px;
            padding: 3px 8px;
            border-radius: 10px;
            font-weight: 700;
            margin-left: 6px;
            box-shadow: 0 2px 8px rgba(255, 71, 87, 0.3);
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
        }
        
        .header {
            text-align: center;
            margin-bottom: 25px;
        }
        
        .header h1 {
            font-size: 28px;
            background: linear-gradient(135deg, #4285f4, #34a853, #fbbc05);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
            font-weight: 800;
        }
        
        .header .subtitle {
            color: #8b8b8b;
            font-size: 16px;
            margin-bottom: 20px;
            font-weight: 500;
        }
        
        .wallet-section {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, #2a2a3e 0%, #2d2d42 100%);
            border-radius: 16px;
            padding: 15px 18px;
            margin-bottom: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .wallet-connect-btn {
            background: linear-gradient(135deg, #4285f4, #1976d2);
            color: white;
            border: none;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: 12px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);
        }
        
        .wallet-connect-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(66, 133, 244, 0.4);
        }
        
        .balance-section {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .balance-btn {
            background: linear-gradient(135deg, #4285f4, #1976d2);
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
            box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);
        }
        
        .balance-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(66, 133, 244, 0.4);
        }
        
        .balance-btn.minus {
            background: linear-gradient(135deg, #ff4757, #ff3742);
            box-shadow: 0 4px 15px rgba(255, 71, 87, 0.3);
        }
        
        .balance-btn.minus:hover {
            box-shadow: 0 6px 20px rgba(255, 71, 87, 0.4);
        }
        
        .balance-display {
            color: white;
            font-size: 15px;
            font-weight: 700;
            min-width: 80px;
            text-align: center;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .ton-icon {
            width: 20px;
            height: 20px;
            background-image: url('https://i.postimg.cc/kX2nWB4M/121-20250711185549.png');
            background-size: cover;
            background-position: center;
            border-radius: 50%;
            flex-shrink: 0;
        }
        
        .tabs {
            display: flex;
            margin-bottom: 25px;
            background: linear-gradient(135deg, #2a2a3e 0%, #2d2d42 100%);
            border-radius: 14px;
            padding: 6px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .tab {
            flex: 1;
            padding: 14px;
            text-align: center;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            font-size: 15px;
            position: relative;
        }
        
        .tab.active {
            background: linear-gradient(135deg, #4285f4, #1976d2);
            color: white;
            box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);
        }
        
        .tab:not(.active) {
            color: #8b8b8b;
        }
        
        .tab:not(.active):hover {
            color: #ffffff;
            background: rgba(255, 255, 255, 0.05);
        }
        
        /* Фильтры */
        .filters-section {
            margin-bottom: 25px;
        }
        
        .filter-row {
            display: flex;
            gap: 10px;
            margin-bottom: 18px;
            align-items: center;
        }
        
        .filter-select {
            background: linear-gradient(135deg, #2a2a3e 0%, #2d2d42 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 12px 15px;
            border-radius: 12px;
            color: white;
            font-size: 14px;
            flex: 1;
            transition: all 0.3s ease;
        }
        
        .filter-select:focus {
            outline: none;
            border-color: #4285f4;
            box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1);
        }
        
        .filter-select option {
            background: #2a2a3e;
            color: white;
        }
        
        .clear-filters-btn {
            background: linear-gradient(135deg, #ff4757, #ff3742);
            color: white;
            border: none;
            padding: 10px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 16px;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            flex-shrink: 0;
            margin-left: 10px;
            box-shadow: 0 4px 15px rgba(255, 71, 87, 0.3);
        }
        
        .clear-filters-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(255, 71, 87, 0.4);
        }
        
        .channels-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 18px;
            margin-bottom: 25px;
        }
        
        .channel-group-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #2d2d42 100%);
            border-radius: 18px;
            padding: 18px;
            text-align: center;
            transition: all 0.3s ease;
            min-height: 220px;
            position: relative;
            cursor: pointer;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .channel-group-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
            border-color: rgba(66, 133, 244, 0.3);
        }
        
        .channel-group-images {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 18px;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .channel-group-images.single {
            justify-content: center;
        }
        
        .channel-group-images.double {
            justify-content: space-around;
        }
        
        .channel-group-images.triple {
            justify-content: space-between;
        }
        
        .channel-group-image {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            background-size: cover;
            background-position: center;
            border: 2px solid rgba(255, 255, 255, 0.1);
            flex-shrink: 0;
            position: relative;
        }
        
        .channel-group-image::before {
            display: none;
        }
        
        .channel-group-image.single {
            width: 85px;
            height: 85px;
        }
        
        .channel-group-image.single::before {
            font-size: 30px;
        }
        
        .channel-group-image.double {
            width: 65px;
            height: 65px;
        }
        
        .channel-group-image.double::before {
            font-size: 22px;
        }
        
        .channel-group-image.triple {
            width: 50px;
            height: 50px;
        }
        
        .channel-group-image.triple::before {
            font-size: 18px;
        }
        
        .channel-group-count {
            position: absolute;
            top: 15px;
            right: 15px;
            background: linear-gradient(135deg, #4285f4, #1976d2);
            color: white;
            font-size: 12px;
            padding: 6px 10px;
            border-radius: 12px;
            font-weight: 700;
            box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);
        }
        
        .channel-group-title {
            color: white;
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 18px;
            text-transform: uppercase;
        }
        
        .channel-card-catalog {
            background: linear-gradient(135deg, #2a2a3e 0%, #2d2d42 100%);
            border-radius: 18px;
            padding: 18px;
            text-align: center;
            transition: all 0.3s ease;
            min-height: 160px;
            position: relative;
            cursor: pointer;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .channel-card-catalog:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
        }
        
        .channel-image-catalog {
            width: 85px;
            height: 85px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            margin: 12px auto 18px;
            background-size: cover;
            background-position: center;
            border: 2px solid rgba(255, 255, 255, 0.1);
            position: relative;
        }
        
        .channel-image-catalog::before {
            display: none;
        }
        
        .channel-name-catalog {
            color: white;
            font-size: 15px;
            font-weight: 700;
            text-transform: uppercase;
            line-height: 1.2;
        }
        
        .price-btn {
            background: linear-gradient(135deg, #4285f4, #1976d2);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 12px;
            width: 100%;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            font-size: 13px;
            box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);
        }
        
        .price-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(66, 133, 244, 0.4);
        }
        
        .triangle-icon {
            color: #64B5F6;
            font-size: 14px;
        }
        
        /* My Channel Styles */
        .channel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 35px;
        }
        
        .channel-title-header {
            color: white;
            font-size: 22px;
            font-weight: 700;
        }
        
        .add-ad-btn {
            background: linear-gradient(135deg, #4285f4, #1976d2);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 20px;
            width: 45px;
            height: 45px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);
        }
        
        .add-ad-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(66, 133, 244, 0.4);
        }
        
        .empty-channel {
            text-align: center;
            padding: 50px;
            color: #8b8b8b;
        }
        
        .empty-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        
        .empty-title {
            font-size: 18px;
            color: #ffffff;
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        .empty-subtitle {
            font-size: 15px;
            color: #8b8b8b;
            margin-bottom: 30px;
            line-height: 1.4;
        }
        
        .create-ad-btn {
            background: linear-gradient(135deg, #4285f4, #1976d2);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 15px;
            font-weight: 700;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);
        }
        
        .create-ad-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(66, 133, 244, 0.4);
        }
        
        .empty-state {
            grid-column: 1/-1;
            text-align: center;
            padding: 50px;
            color: #8b8b8b;
        }
        
        .loading {
            grid-column: 1/-1;
            text-align: center;
            padding: 50px;
            color: #8b8b8b;
            font-size: 16px;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .channel-card {
            animation: fadeIn 0.6s ease-out;
        }
        
        .filters-hidden {
            display: none;
        }
        
        /* Modal overlay for channel filter */
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
            padding: 25px;
            border-bottom: 1px solid #2a2a3e;
            position: sticky;
            top: 0;
            background: #1a1a2e;
            z-index: 10;
        }
        
        .modal-title {
            color: white;
            font-size: 20px;
            font-weight: 700;
        }
        
        .modal-close {
            background: none;
            border: none;
            color: #8b8b8b;
            font-size: 28px;
            cursor: pointer;
            padding: 0;
            width: 35px;
            height: 35px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        .modal-close:hover {
            color: white;
            transform: scale(1.1);
        }
        
        .modal-search {
            background: linear-gradient(135deg, #2a2a3e 0%, #2d2d42 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 14px 45px 14px 18px;
            border-radius: 12px;
            color: white;
            width: calc(100% - 40px);
            margin: 0 20px 25px 20px;
            font-size: 16px;
            position: relative;
        }
        
        .modal-search:focus {
            outline: none;
            border-color: #4285f4;
            box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1);
        }
        
        .modal-search::placeholder {
            color: #8b8b8b;
        }
        
        .channel-options-list {
            padding: 0 20px 120px 20px;
        }
        
        .channel-option {
            display: flex;
            align-items: center;
            padding: 18px 0;
            cursor: pointer;
            border-bottom: 1px solid #2a2a3e;
            transition: all 0.3s ease;
        }
        
        .channel-option:last-child {
            border-bottom: none;
        }
        
        .channel-option:hover {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            margin: 0 -15px;
            padding: 18px 15px;
        }
        
        .channel-option-radio {
            width: 22px;
            height: 22px;
            border: 2px solid #4a4a5e;
            border-radius: 50%;
            margin-right: 18px;
            position: relative;
            flex-shrink: 0;
            transition: all 0.3s ease;
        }
        
        .channel-option.selected .channel-option-radio {
            border-color: #4285f4;
            background: rgba(66, 133, 244, 0.1);
        }
        
        .channel-option.selected .channel-option-radio::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 10px;
            height: 10px;
            background: #4285f4;
            border-radius: 50%;
        }
        
        .channel-option-image {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            margin-right: 18px;
            background-size: cover;
            background-position: center;
            border: 2px solid rgba(255, 255, 255, 0.1);
            flex-shrink: 0;
            position: relative;
        }
        
        .channel-option-image::before {
            display: none;
        }
        
        .channel-option-name {
            color: white;
            font-size: 17px;
            font-weight: 600;
        }
        
        .modal-buttons {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #1a1a2e;
            padding: 25px;
            display: flex;
            gap: 18px;
            border-top: 1px solid #2a2a3e;
        }
        
        .modal-btn {
            flex: 1;
            padding: 18px;
            border: none;
            border-radius: 15px;
            font-size: 17px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .modal-btn.cancel {
            background: #4a4a5e;
            color: white;
        }
        
        .modal-btn.cancel:hover {
            background: #5a5a6e;
            transform: translateY(-2px);
        }
        
        .modal-btn.select {
            background: linear-gradient(135deg, #4285f4, #1976d2);
            color: white;
            box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);
        }
        
        .modal-btn.select:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(66, 133, 244, 0.4);
        }
        
        /* Channel Detail Modal */
        .channel-detail-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.85);
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
        }
        
        .channel-detail-modal.show {
            display: flex;
        }
        
        .channel-detail-content {
            background: linear-gradient(135deg, #2a2a3e 0%, #2d2d42 100%);
            border-radius: 25px;
            padding: 35px;
            max-width: 350px;
            width: 100%;
            text-align: center;
            position: relative;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }
        
        .channel-detail-close {
            position: absolute;
            top: 18px;
            right: 18px;
            background: #4a4a5e;
            border: none;
            color: white;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        .channel-detail-close:hover {
            background: #5a5a6e;
            transform: scale(1.1);
        }
        
        .channel-detail-image {
            width: 130px;
            height: 130px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 25px;
            margin: 0 auto 25px;
            background-size: cover;
            background-position: center;
            border: 3px solid rgba(255, 255, 255, 0.1);
            position: relative;
        }
        
        .channel-detail-image::before {
            display: none;
        }
        
        .channel-detail-title {
            color: white;
            font-size: 22px;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        
        .channel-detail-id {
            color: #8b8b8b;
            font-size: 15px;
            margin-bottom: 18px;
        }
        
        .channel-detail-description {
            color: #8b8b8b;
            font-size: 15px;
            line-height: 1.5;
            margin-bottom: 30px;
            min-height: 45px;
        }
        
        .channel-detail-price {
            background: linear-gradient(135deg, #4285f4, #1976d2);
            color: white;
            border: none;
            padding: 18px;
            border-radius: 15px;
            width: 100%;
            font-weight: 700;
            cursor: pointer;
            font-size: 17px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);
        }
        
        .channel-detail-price:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(66, 133, 244, 0.4);
        }
    </style>
</head>
<body>
    <!-- Loading Screen -->
    <div class="loading-screen" id="loadingScreen">
        <div class="loading-logo">🚀</div>
        <div class="loading-title">GiftRoom</div>
        <div class="loading-subtitle">Магазин подарунків в Telegram</div>
        
        <div class="channel-loader">
            <div class="channel-box"></div>
            <div class="channel-box"></div>
            <div class="channel-box"></div>
        </div>
        
        <div class="progress-container">
            <div class="progress-bar"></div>
        </div>
        
        <div class="loading-text">Загрузка подарков...</div>
    </div>

    <!-- Main App -->
    <div class="main-app" id="mainApp">
        <div style="padding: 20px;">
            <div class="header">
                <h1>GiftRoom Market</h1>
                <div class="subtitle">Магазин подарунків в Telegram</div>
                
                <div class="wallet-section">
                    <button class="wallet-connect-btn" onclick="connectWallet()">TON гаманець</button>
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
                <div class="tab" onclick="openChannelModal()">Collections</div>
                <div class="tab" onclick="switchTab('my-channel')">My Channel</div>
            </div>
            
            <!-- Фильтры (показываются только в Маркете) -->
            <div class="filters-section" id="filtersSection">
                <div class="filter-row">
                    <select class="filter-select" id="channelTypeFilter" onchange="applyFilters()">
                        <option value="">Все каналы</option>
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
                        <option value="recent">Новые</option>
                        <option value="price_asc">Цена: мин → макс</option>
                        <option value="price_desc">Цена: макс → мин</option>
                        <option value="rarity">По редкости</option>
                        <option value="popular">Популярные</option>
                    </select>
                    
                    <button class="clear-filters-btn" onclick="clearFilters()" title="Очистить фильтры">✕</button>
                </div>
            </div>
            
            <div class="channels-grid" id="channelsGrid">
                <div class="loading">Загрузка подарков...</div>
            </div>
        </div>
    </div>
    
    <!-- Modal для выбора каналов -->
    <div class="modal-overlay" id="channelModal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">Выберите тип канала</div>
                <button class="modal-close" onclick="closeChannelModal()">✕</button>
            </div>
            
            <input type="text" class="modal-search" placeholder="Поиск каналов..." id="modalSearchBox" onkeyup="filterModalChannels()">
            
            <div class="channel-options-list" id="channelOptionsList">
                <!-- Список каналов будет сгенерирован здесь -->
            </div>
            
            <div class="modal-buttons">
                <button class="modal-btn cancel" onclick="closeChannelModal()">Отмена</button>
                <button class="modal-btn select" onclick="selectModalChannel()">Выбрать</button>
            </div>
        </div>
    </div>
    
    <!-- Modal для деталей канала -->
    <div class="channel-detail-modal" id="channelDetailModal">
        <div class="channel-detail-content">
            <button class="channel-detail-close" onclick="closeChannelDetail()">✕</button>
            <div class="channel-detail-image" id="channelDetailImage"></div>
            <div class="channel-detail-title" id="channelDetailTitle"></div>
            <div class="channel-detail-id" id="channelDetailId"></div>
            <div class="channel-detail-description" id="channelDetailDescription">
                Канал с уникальными подарками в Telegram. Получите доступ к эксклюзивным коллекциям!
            </div>
            <button class="channel-detail-price" id="channelDetailPrice" onclick="buyChannelFromDetail()">
                <span id="channelDetailPriceText"></span>
                <span class="triangle-icon">▼</span>
                <span id="channelDetailSubscribers"></span>
            </button>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        // Loading Screen Logic
        function hideLoadingScreen() {
            const loadingScreen = document.getElementById('loadingScreen');
            const mainApp = document.getElementById('mainApp');
            
            setTimeout(() => {
                loadingScreen.classList.add('hidden');
                mainApp.classList.add('visible');
            }, 3800);
        }
        
        // Initialize app
        function initializeApp() {
            console.log('ChannelGift Market инициализирован');
            
            setTimeout(() => {
                loadInitialChannels();
            }, 1200);
        }
        
        function loadInitialChannels() {
            showMarket();
        }
        
        // Start loading process when DOM is ready
        document.addEventListener('DOMContentLoaded', () => {
            initializeApp();
            hideLoadingScreen();
        });
        
        // База данных всех подарков с вариациями для тестирования групп
        const allChannels = [
            {id: 1, name: "МОДНЫЕ ПОДАРКИ", desc: "Стильные подарки", price: "2.12", subscribers: "11.5K", new: false, listed: true, category: "fashion", rarity: 1, popular: true, image: "https://i.postimg.cc/jdsL20Gt/Gifts-Gifts-Gifts-Ag-ADBmg-AAnz-Oe-Ek.png"},
            {id: 2, name: "ВИНТАЖ КОЛЛЕКЦИЯ", desc: "Винтажные вещи", price: "2.90", subscribers: "3.1K", new: false, listed: true, category: "objects", rarity: 1, popular: false, image: "https://i.postimg.cc/XqDSnCRZ/Gifts-Gifts-Gifts-Ag-ADWWg-AAhwgi-Uk.png"},
            {id: 3, name: "МИЛЫЕ ПИТОМЦЫ", desc: "Подарки с животными", price: "3.23", subscribers: "2.9K", new: false, listed: true, category: "animals", rarity: 1, popular: true, image: "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"},
            {id: 4, name: "УЮТНЫЙ ДОМ", desc: "Домашние подарки", price: "3.56", subscribers: "2.8K", new: false, listed: false, category: "objects", rarity: 1, popular: false, image: "https://i.postimg.cc/bwxCTnmQ/Gifts-Gifts-Gifts-Ag-ADKmk-AAt0-L2-Ek.png"},
            {id: 5, name: "ФИТНЕС ЗОНА", desc: "Спортивные подарки", price: "3.89", subscribers: "2.7K", new: false, listed: true, category: "sports", rarity: 1, popular: true, image: "https://i.postimg.cc/K4Xf7cLq/Gifts-Gifts-Gifts-Ag-ADB3-UAAp5-V0-Uk.png"},
            {id: 6, name: "ТЕХ ГАДЖЕТЫ", desc: "Технические новинки", price: "4.12", subscribers: "2.6K", new: false, listed: true, category: "objects", rarity: 1, popular: false, image: "https://i.postimg.cc/hjfNpjzc/Gifts-Gifts-Gifts-Ag-ADj-Gw-AAkl0c-Eo.png"},
            {id: 7, name: "ПРАЗДНИЧНАЯ МАГИЯ", desc: "Подарки для праздников", price: "4.45", subscribers: "2.5K", new: false, listed: false, category: "holidays", rarity: 1, popular: true, image: "https://i.postimg.cc/TY8BJTRv/Gifts-Gifts-Gifts-Ag-ADk3-AAAiy-WGEs.png"},
            {id: 8, name: "СЛАДКИЕ РАДОСТИ", desc: "Сладкие подарки", price: "4.78", subscribers: "2.4K", new: false, listed: true, category: "food", rarity: 1, popular: false, image: "https://i.postimg.cc/gkqtyRS3/Gifts-Gifts-Gifts-Ag-ADB3-AAAr-Pqc-Eo.png"},
            {id: 9, name: "ЖЕНСКИЙ ДЕНЬ", desc: "8 марта подарки", price: "5.12", subscribers: "2.3K", new: false, listed: false, category: "holidays", rarity: 1, popular: false, image: "https://i.postimg.cc/d1y4hTZk/Gifts-Gifts-Gifts-Ag-ADh2o-AAoa-Dc-Eo.png"},
            {id: 10, name: "ПРЕМИУМ ТЕХ", desc: "Дорогая техника", price: "5.45", subscribers: "2.2K", new: false, listed: true, category: "objects", rarity: 2, popular: true, image: "https://i.postimg.cc/3NZjGj8R/Gifts-Gifts-Gifts-Ag-ADhmw-AAl1-Zc-Uo.png"},
            {id: 11, name: "КУХНЯ ПРО", desc: "Кухонная техника", price: "5.89", subscribers: "2.1K", new: false, listed: false, category: "objects", rarity: 2, popular: false, image: "https://i.postimg.cc/Dfc1Bghf/Gifts-Gifts-Gifts-Ag-ADe-WMAAp-Rw-IUs.png"},
            {id: 12, name: "ТАЛИСМАНЫ УДАЧИ", desc: "Подарки на удачу", price: "6.34", subscribers: "2.0K", new: false, listed: true, category: "symbols", rarity: 2, popular: true, image: "https://i.postimg.cc/NfJmwjLW/Gifts-Gifts-Gifts-Ag-ADf-GYAAjfaw-Uo.png"},
            {id: 13, name: "МИСТИЧЕСКАЯ СИЛА", desc: "Загадочные подарки", price: "6.78", subscribers: "1.8K", new: false, listed: false, category: "symbols", rarity: 2, popular: false, image: "https://i.postimg.cc/hGFJSzn3/Gifts-Gifts-Gifts-Ag-AD-HEAAq-9c-Us.png"},
            {id: 14, name: "СВЯЩЕННЫЕ МЕСТА", desc: "Религиозные подарки", price: "7.23", subscribers: "1.7K", new: false, listed: true, category: "symbols", rarity: 2, popular: false, image: "https://i.postimg.cc/pr1T3ykC/Gifts-Gifts-Gifts-Ag-ADV3-MAAnv-We-Us.png"},
            {id: 15, name: "УЛИЧНАЯ ЕДА", desc: "Вкусные подарки", price: "7.89", subscribers: "1.6K", new: false, listed: true, category: "food", rarity: 2, popular: true, image: "https://i.postimg.cc/k5F5qTfB/Gifts-Gifts-Gifts-Ag-AD4-GQAAq8-Xg-Us.png"},
            {id: 16, name: "ЗАБАВНЫЕ ШТУЧКИ", desc: "Прикольные подарки", price: "8.67", subscribers: "1.5K", new: false, listed: false, category: "misc", rarity: 2, popular: false, image: "https://i.postimg.cc/05HykMdd/Gifts-Gifts-Gifts-Ag-AD82w-AAk-FZg-Es.png"},
            {id: 17, name: "ЦАРСТВО ЖИВОТНЫХ", desc: "Подарки с животными", price: "9.45", subscribers: "1.4K", new: false, listed: true, category: "animals", rarity: 2, popular: true, image: "https://i.postimg.cc/bN7Yn75Z/Gifts-Gifts-Gifts-Ag-AEZAACV66-BSw.png"},
            {id: 18, name: "СТРОИТЕЛЬСТВО", desc: "Строительные подарки", price: "10.78", subscribers: "1.3K", new: false, listed: false, category: "objects", rarity: 2, popular: false, image: "https://i.postimg.cc/c1jdyq0F/Gifts-Gifts-Gifts-Ag-ADg2o-AAg-R5g-Us.png"},
            {id: 19, name: "КОСМИЧЕСКИЕ ПУТЕШЕСТВИЯ", desc: "Космические подарки", price: "12.34", subscribers: "1.2K", new: false, listed: true, category: "objects", rarity: 3, popular: true, image: "https://i.postimg.cc/nhfZrvs7/Gifts-Gifts-Gifts-Ag-ADIo-UAAk3-J2-Es.png"},
            {id: 20, name: "ПАСХАЛЬНАЯ РАДОСТЬ", desc: "Пасхальные подарки", price: "13.67", subscribers: "1.1K", new: false, listed: true, category: "holidays", rarity: 3, popular: false, image: "https://i.postimg.cc/tTJGwkf0/Gifts-Gifts-Gifts-Ag-ADBa-UAAk8-WKEg.png"},
            {id: 21, name: "ПУШИСТЫЕ ДРУЗЬЯ", desc: "Мягкие игрушки", price: "15.43", subscribers: "967", new: false, listed: false, category: "animals", rarity: 3, popular: true, image: "https://i.postimg.cc/WtLRDv4j/Gifts-Gifts-Gifts-Ag-ADh-HUAAg-O6-IUg.png"},
            {id: 22, name: "ДЕНЬ ТРУДА", desc: "1 мая подарки", price: "17.89", subscribers: "856", new: false, listed: true, category: "holidays", rarity: 3, popular: false, image: "https://i.postimg.cc/gJxk8GG6/Gifts-Gifts-Gifts-Ag-ADMm4-AAj-Ll6-Ug.png"},
            {id: 23, name: "ЧЕМПИОНЫ", desc: "Спортивные награды", price: "19.56", subscribers: "745", new: false, listed: true, category: "sports", rarity: 3, popular: true, image: "https://i.postimg.cc/N0zQgZRG/Gifts-Gifts-Gifts-Ag-ADO3c-AAqb-DEEk.png"},
            {id: 24, name: "ГОРОДСКИЕ ПТИЦЫ", desc: "Подарки с птицами", price: "22.78", subscribers: "634", new: false, listed: false, category: "animals", rarity: 3, popular: false, image: "https://i.postimg.cc/QxJsBFcy/Gifts-Gifts-Gifts-Ag-ADa3-QAAtw-JEEk.png"},
            {id: 25, name: "ЗВЕЗДНЫЙ", desc: "Звездные подарки", price: "25.34", subscribers: "512", new: false, listed: true, category: "symbols", rarity: 3, popular: true, image: "https://i.postimg.cc/3Nr1nfbp/Gifts-Gifts-Gifts-Ag-ADbn-UAAl-XNEUk.png"},
            {id: 26, name: "РАЙ МОРОЖЕНОГО", desc: "Мороженое подарки", price: "28.67", subscribers: "423", new: false, listed: true, category: "food", rarity: 4, popular: false, image: "https://i.postimg.cc/ydjXgXYN/Gifts-Gifts-Gifts-Ag-AD0-Ww-AAs4-T4-Ek.png"},
            {id: 27, name: "ЗАМОРОЖЕННЫЕ ЛАКОМСТВА", desc: "Ледяные подарки", price: "32.45", subscribers: "345", new: false, listed: false, category: "food", rarity: 4, popular: true, image: "https://i.postimg.cc/L4y3mTbC/Gifts-Gifts-Gifts-Ag-ADy-XEAAky04-Ek.png"},
            {id: 28, name: "МАСТЕР РЕМЕСЛА", desc: "Ремесленные подарки", price: "38.90", subscribers: "267", new: true, listed: true, category: "misc", rarity: 4, popular: false, image: "https://i.postimg.cc/85pLSJBg/Gifts-Gifts-Gifts-Ag-ADKX4-AAuw-O2-Ek.png"},
            {id: 29, name: "ЗОЛОТАЯ РОСКОШЬ", desc: "Дорогие подарки", price: "45.78", subscribers: "203", new: true, listed: true, category: "misc", rarity: 4, popular: true, image: "https://i.postimg.cc/BQrDvwcg/Gifts-Gifts-Gifts-Ag-ADD3-IAAm-RNKUo.png"},
            {id: 30, name: "СИМВОЛ СВОБОДЫ", desc: "Патриотические подарки", price: "54.67", subscribers: "156", new: true, listed: true, category: "symbols", rarity: 5, popular: true, image: "https://i.postimg.cc/0QXK1ty7/Gifts-Gifts-Gifts-Ag-ADzn-IAAl-Gn-QEs.png"},
            {id: 31, name: "СТАТУЯ СВОБОДЫ", desc: "Американские подарки", price: "65.43", subscribers: "112", new: true, listed: true, category: "symbols", rarity: 5, popular: false, image: "https://i.postimg.cc/V6hvVdKR/Gifts-Gifts-Gifts-Ag-ADi-IYAAqf-LQEs.png"},
            {id: 32, name: "ФАКЕЛ НАДЕЖДЫ", desc: "Вдохновляющие подарки", price: "76.89", subscribers: "89", new: true, listed: true, category: "symbols", rarity: 5, popular: true, image: "https://i.postimg.cc/wv1LMKPw/Gifts-Gifts-Gifts-Ag-AD2-XQAAk-VPSEs.png"},
            {id: 33, name: "ЗАПАДНОЕ ПОБЕРЕЖЬЕ", desc: "Калифорнийские подарки", price: "87.32", subscribers: "67", new: true, listed: true, category: "symbols", rarity: 5, popular: false, image: "https://i.postimg.cc/GtkBTbjx/Gifts-Gifts-Gifts-Ag-ADV4-QAAiibe-Us.png"},
            {id: 34, name: "КУЛЬТУРА ЛОУРАЙДЕРОВ", desc: "Автомобильные подарки", price: "98.45", subscribers: "23", new: true, listed: true, category: "entertainment", rarity: 5, popular: true, image: "https://i.postimg.cc/7Y96Fsth/Gifts-Gifts-Gifts-Ag-ADNWw-AAg5ze-Es.png"},
            {id: 35, name: "ПРЕМИУМ ДЫМ", desc: "Элитные курительные", price: "134.56", subscribers: "45", new: true, listed: true, category: "entertainment", rarity: 5, popular: false, image: "https://i.postimg.cc/FKMsy2zW/Gifts-Gifts-Gifts-Ag-ADi38-AAg-7c-Es.png"},
            {id: 36, name: "КОЛЛЕКЦИЯ СВЭГА", desc: "Стильные аксессуары", price: "156.78", subscribers: "34", new: true, listed: true, category: "fashion", rarity: 5, popular: true, image: "https://i.postimg.cc/d1cwkrNg/Gifts-Gifts-Gifts-Ag-AD5-XMAAmjze-Us.png"},
            {id: 37, name: "ЛЕГЕНДАРНЫЙ КАНАЛ", desc: "Эксклюзивная коллекция", price: "208.354", subscribers: "15", new: true, listed: true, category: "entertainment", rarity: 5, popular: true, image: "https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"},
            
            // Дополнительные варианты для тестирования групп
            {id: 38, name: "ЛЕГЕНДАРНЫЙ КАНАЛ", desc: "Эксклюзивная коллекция - вариант 2", price: "180.25", subscribers: "8", new: true, listed: true, category: "entertainment", rarity: 5, popular: true, image: "https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"},
            {id: 39, name: "ЛЕГЕНДАРНЫЙ КАНАЛ", desc: "Эксклюзивная коллекция - вариант 3", price: "220.15", subscribers: "5", new: true, listed: true, category: "entertainment", rarity: 5, popular: true, image: "https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"},
            
            {id: 40, name: "ПРЕМИУМ ДЫМ", desc: "Элитные курительные - вариант 2", price: "145.20", subscribers: "25", new: true, listed: true, category: "entertainment", rarity: 5, popular: false, image: "https://i.postimg.cc/FKMsy2zW/Gifts-Gifts-Gifts-Ag-ADi38-AAg-7c-Es.png"},
            
            {id: 41, name: "МИЛЫЕ ПИТОМЦЫ", desc: "Подарки с животными - вариант 2", price: "3.45", subscribers: "2.5K", new: false, listed: true, category: "animals", rarity: 1, popular: true, image: "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"},
            {id: 42, name: "МИЛЫЕ ПИТОМЦЫ", desc: "Подарки с животными - вариант 3", price: "3.67", subscribers: "2.2K", new: false, listed: true, category: "animals", rarity: 1, popular: true, image: "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"}
        ];
        
        let currentView = 'market';
        let selectedFilter = null;
        let tempSelectedChannel = null;
        let currentFilters = {
            channelType: '',
            sort: 'recent'
        };
        
        // Применение фильтров
        function applyFilters() {
            if (currentView === 'market') {
                applyMarketFilters();
            }
        }
        
        // Применение фильтров в Маркете
        function applyMarketFilters() {
            if (selectedFilter) {
                applyChannelNameFilter();
                return;
            }
            
            const channelTypeFilter = document.getElementById('channelTypeFilter').value;
            const sortFilter = document.getElementById('sortFilter').value;
            
            currentFilters.channelType = channelTypeFilter;
            currentFilters.sort = sortFilter;
            
            let filteredChannels = allChannels.filter(channel => channel.listed);
            
            // Фильтр по типу канала
            if (channelTypeFilter) {
                filteredChannels = filteredChannels.filter(channel => channel.category === channelTypeFilter);
            }
            
            // Сортировка
            switch (sortFilter) {
                case 'recent':
                    filteredChannels.sort((a, b) => b.new - a.new || b.id - a.id);
                    break;
                case 'price_asc':
                    filteredChannels.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
                    break;
                case 'price_desc':
                    filteredChannels.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
                    break;
                case 'rarity':
                    filteredChannels.sort((a, b) => b.rarity - a.rarity);
                    break;
                case 'popular':
                    filteredChannels.sort((a, b) => b.popular - a.popular);
                    break;
            }
            
            renderGroupedChannels(filteredChannels);
        }
        
        // Очистка фильтров
        function clearFilters() {
            document.getElementById('channelTypeFilter').value = '';
            document.getElementById('sortFilter').value = 'recent';
            selectedFilter = null;
            currentFilters = {
                channelType: '',
                sort: 'recent'
            };
            
            if (currentView === 'market') {
                applyMarketFilters();
            } else if (currentView === 'catalog') {
                showCatalog();
            }
        }
        
        // Показать только listed каналы в Маркете
        function showMarket() {
            document.getElementById('filtersSection').classList.remove('filters-hidden');
            applyMarketFilters();
        }
        
        // Показать Мои каналы
        function showMyChannel() {
            document.getElementById('filtersSection').classList.add('filters-hidden');
            const grid = document.getElementById('channelsGrid');
            grid.innerHTML = `
                <div class="channel-header">
                    <div class="channel-title-header">Мои каналы</div>
                    <button class="add-ad-btn" onclick="createAd()" title="Добавить канал">+</button>
                </div>
                <div class="empty-channel">
                    <div class="empty-icon">📺</div>
                    <div class="empty-title">Нет каналов</div>
                    <div class="empty-subtitle">Создайте ваше первое объявление о продаже канала</div>
                    <button class="create-ad-btn" onclick="createAd()">Добавить канал</button>
                </div>
            `;
        }
        
        function openChannelModal() {
            const modal = document.getElementById('channelModal');
            const optionsList = document.getElementById('channelOptionsList');
            
            // Создаем список всех уникальных каналов
            const channelGroups = {};
            allChannels.forEach(channel => {
                if (!channelGroups[channel.name]) {
                    channelGroups[channel.name] = {
                        name: channel.name,
                        image: channel.image,
                        new: channel.new
                    };
                }
            });
            
            const uniqueChannels = Object.values(channelGroups);
            
            // Добавляем опцию "Все каналы"
            const allChannelsOption = {
                name: 'Все каналы',
                image: '',
                new: false,
                isAll: true
            };
            
            const options = [allChannelsOption, ...uniqueChannels];
            
            optionsList.innerHTML = options.map(channel => `
                <div class="channel-option ${(!selectedFilter && channel.isAll) || selectedFilter === channel.name ? 'selected' : ''}" 
                     onclick="selectModalOption('${channel.isAll ? '' : channel.name}', this)">
                    <div class="channel-option-radio"></div>
                    ${channel.isAll ? '' : `<div class="channel-option-image" style="background-image: url('${channel.image}')"></div>`}
                    <div class="channel-option-name">${channel.name}</div>
                </div>
            `).join('');
            
            // Устанавливаем текущий выбор
            tempSelectedChannel = selectedFilter;
            
            modal.classList.add('show');
        }
        
        function closeChannelModal() {
            const modal = document.getElementById('channelModal');
            modal.classList.remove('show');
            tempSelectedChannel = null;
        }
        
        function selectModalOption(channelName, element) {
            // Убираем выделение с предыдущего элемента
            document.querySelectorAll('.channel-option').forEach(opt => opt.classList.remove('selected'));
            
            // Выделяем текущий элемент
            element.classList.add('selected');
            
            // Сохраняем временный выбор
            tempSelectedChannel = channelName === '' ? null : channelName;
        }
        
        function selectModalChannel() {
            // Применяем выбор
            selectedFilter = tempSelectedChannel;
            
            // Закрываем модальное окно
            closeChannelModal();
            
            // Переключаемся на Каталог и применяем фильтр
            currentView = 'catalog';
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab')[1].classList.add('active');
            
            showCatalog();
        }
        
        function filterModalChannels() {
            const query = document.getElementById('modalSearchBox').value.toLowerCase();
            const options = document.querySelectorAll('.channel-option');
            
            options.forEach(option => {
                const name = option.querySelector('.channel-option-name').textContent.toLowerCase();
                if (name.includes(query)) {
                    option.style.display = 'flex';
                } else {
                    option.style.display = 'none';
                }
            });
        }
        
        // Применение фильтра по названию канала
        function applyChannelNameFilter() {
            if (!selectedFilter) {
                applyFilters();
                return;
            }
            
            let filteredChannels = allChannels.filter(channel => channel.listed && channel.name === selectedFilter);
            
            // Применяем сортировку
            switch (currentFilters.sort) {
                case 'recent':
                    filteredChannels.sort((a, b) => b.new - a.new || b.id - a.id);
                    break;
                case 'price_asc':
                    filteredChannels.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
                    break;
                case 'price_desc':
                    filteredChannels.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
                    break;
                case 'rarity':
                    filteredChannels.sort((a, b) => b.rarity - a.rarity);
                    break;
                case 'popular':
                    filteredChannels.sort((a, b) => b.popular - a.popular);
                    break;
            }
            
            renderChannels(filteredChannels);
        }
        
        // Показать каталог - с выборочным показом каналов
        function showCatalog() {
            document.getElementById('filtersSection').classList.add('filters-hidden');
            
            if (selectedFilter) {
                // Показываем только выбранный тип канала
                const filteredChannels = allChannels.filter(channel => channel.name === selectedFilter);
                const sortedChannels = filteredChannels.sort((a, b) => b.id - a.id);
                renderCatalogChannels(sortedChannels);
            } else {
                // Показываем все каналы
                const sortedChannels = [...allChannels].sort((a, b) => b.id - a.id);
                renderCatalogChannels(sortedChannels);
            }
        }
        
        // Рендер каналов в Каталоге
        function renderCatalogChannels(channels) {
            const grid = document.getElementById('channelsGrid');
            
            if (channels.length === 0) {
                grid.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 16px; margin-bottom: 8px;">Каналы не найдены</div>
                        <div style="font-size: 14px;">Попробуйте изменить фильтры</div>
                    </div>
                `;
                return;
            }
            
            grid.innerHTML = channels.map(channel => `
                <div class="channel-card-catalog" onclick="selectChannel(${channel.id})">
                    ${channel.new ? '<span class="new-badge">NEW</span>' : ''}
                    ${channel.popular ? '<span class="hot-badge">HOT</span>' : ''}
                    <div class="channel-image-catalog" style="background-image: url('${channel.image}')"></div>
                    <div class="channel-name-catalog">${channel.name}</div>
                </div>
            `).join('');
        }
        
        // Выбор канала в каталоге
        function selectChannel(id) {
            const channel = allChannels.find(c => c.id === id);
            openChannelDetail(id);
        }
        
        // Группируем каналы по названию
        function groupChannelsByName(channels) {
            const groups = {};
            channels.forEach(channel => {
                if (!groups[channel.name]) {
                    groups[channel.name] = [];
                }
                groups[channel.name].push(channel);
            });
            return Object.values(groups);
        }
        
        // Рендер сгруппированных каналов
        function renderGroupedChannels(channels) {
            const grid = document.getElementById('channelsGrid');
            
            if (channels.length === 0) {
                grid.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 16px; margin-bottom: 8px;">Каналы не найдены</div>
                        <div style="font-size: 14px;">Попробуйте изменить фильтры</div>
                    </div>
                `;
                return;
            }
            
            const groupedChannels = groupChannelsByName(channels);
            
            grid.innerHTML = groupedChannels.map(group => {
                const count = group.length;
                const firstChannel = group[0];
                
                let imageClass = 'single';
                let containerClass = 'single';
                if (count === 2) {
                    imageClass = 'double';
                    containerClass = 'double';
                } else if (count >= 3) {
                    imageClass = 'triple';
                    containerClass = 'triple';
                }
                
                const imagesToShow = group.slice(0, 3); // Показываем максимум 3 изображения
                
                return `
                    <div class="channel-group-card" onclick="openChannelGroupDetail('${firstChannel.name}')">
                        <div class="channel-group-count">${count}</div>
                        <div class="channel-group-images ${containerClass}">
                            ${imagesToShow.map(channel => `
                                <div class="channel-group-image ${imageClass}" style="background-image: url('${channel.image}')"></div>
                            `).join('')}
                        </div>
                        <div class="channel-group-title">${firstChannel.name}</div>
                        <button class="price-btn" onclick="event.stopPropagation(); showChannelGroupPrices('${firstChannel.name}')">
                            Цена в TON
                        </button>
                    </div>
                `;
            }).join('');
        }
        
        // Рендер обычных каналов (без группировки)
        function renderChannels(channels) {
            const grid = document.getElementById('channelsGrid');
            
            if (channels.length === 0) {
                grid.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 16px; margin-bottom: 8px;">Каналы не найдены</div>
                        <div style="font-size: 14px;">Попробуйте изменить фильтры</div>
                    </div>
                `;
                return;
            }
            
            grid.innerHTML = channels.map(channel => `
                <div class="channel-card-catalog" onclick="openChannelDetail(${channel.id})">
                    ${channel.new ? '<span class="new-badge">NEW</span>' : ''}
                    ${channel.popular ? '<span class="hot-badge">HOT</span>' : ''}
                    <div class="channel-image-catalog" style="background-image: url('${channel.image}')"></div>
                    <div class="channel-name-catalog">${channel.name}</div>
                    <div class="price-btn" style="margin-top: 10px; font-size: 12px;">
                        ${channel.price} ▼ (${channel.subscribers})
                    </div>
                </div>
            `).join('');
        }
        
        // Переключение вкладок
        function switchTab(tab) {
            currentView = tab;
            
            // Обновляем активную вкладку
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
        
        // Открыть детали группы каналов
        function openChannelGroupDetail(channelName) {
            const channelsInGroup = allChannels.filter(channel => channel.name === channelName);
            if (channelsInGroup.length === 1) {
                // Если один канал, открываем обычное модальное окно
                openChannelDetail(channelsInGroup[0].id);
            } else {
                // Если несколько, показываем список (пока просто alert)
                tg.showAlert(`Группа ${channelName}: ${channelsInGroup.length} каналов`);
            }
        }
        
        // Показать цены группы каналов
        function showChannelGroupPrices(channelName) {
            const channelsInGroup = allChannels.filter(channel => channel.name === channelName && channel.listed);
            const prices = channelsInGroup.map(channel => `${channel.price} ▼ (${channel.subscribers})`).join(', ');
            tg.showAlert(`Цены ${channelName}: ${prices}`);
        }
        
        // Создаем переменную для текущего канала
        let currentChannelDetail = null;
        function openChannelDetail(channelId) {
            const channel = allChannels.find(c => c.id === channelId);
            if (!channel) return;
            
            currentChannelDetail = channel;
            
            document.getElementById('channelDetailImage').style.backgroundImage = `url('${channel.image}')`;
            document.getElementById('channelDetailTitle').textContent = channel.name;
            document.getElementById('channelDetailId').textContent = `#${channel.id}`;
            document.getElementById('channelDetailPriceText').textContent = channel.price;
            document.getElementById('channelDetailSubscribers').textContent = `(${channel.subscribers})`;
            
            document.getElementById('channelDetailModal').classList.add('show');
        }
        
        // Закрыть детали канала
        function closeChannelDetail() {
            document.getElementById('channelDetailModal').classList.remove('show');
            currentChannelDetail = null;
        }
        
        // Купить канал из детального просмотра
        function buyChannelFromDetail() {
            if (currentChannelDetail) {
                buyChannel(currentChannelDetail.id);
                closeChannelDetail();
            }
        }
        
        // Покупка канала
        function buyChannel(id) {
            const channel = allChannels.find(c => c.id === id);
            tg.showAlert(`Покупаем канал #${id}: ${channel.name} за ${channel.price} ▼`);
        }
        
        // Функция для создания объявления
        function createAd() {
            tg.showAlert('Создание объявления о продаже канала - функция в разработке');
        }
        
        // Функции кошелька
        function connectWallet() {
            tg.showAlert('Подключение TON кошелька');
        }
        
        function withdrawBalance() {
            tg.showAlert('Вывод средств');
        }
        
        function addBalance() {
            tg.showAlert('Пополнение баланса');
        }
        
        // Убираем главную кнопку Telegram
        tg.MainButton.hide();
        
        // Адаптация к теме
        if (tg.colorScheme === 'dark') {
            document.body.style.background = '#0f0f1a';
        }
        
        // Telegram WebApp готов
        tg.ready();
    </script>
</body>
</html>
    """

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="🚀 Открыть GiftRoom Market",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]]
    )
    
    await message.answer(
        f"Привет {message.from_user.first_name}! 👋\n\n"
        f"Добро пожаловать в GiftRoom Market! 🎁\n\n"
        f"🔥 45 уникальных подарков\n"
        f"💎 Редкие и эксклюзивные коллекции\n"
        f"⚡ Мгновенные транзакции в TON\n"
        f"🎯 Фильтры по категориям и ценам\n"
        f"📈 Популярные и новые подарки\n\n"
        f"Нажми кнопку чтобы открыть магазин подарков:",
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
    
    print("🎁 GiftRoom Market запущен!")
    print(f"🌐 URL: {WEBAPP_URL}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
