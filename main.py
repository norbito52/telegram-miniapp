# main.py - FastAPI приложение для GiftRoom Market - Маркетплейс каналов с подарками
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
            overflow-x: hidden;
        }
        
        /* Loading Screen Styles */
        .loading-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            animation: gradientShift 6s ease-in-out infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%); }
            33% { background: linear-gradient(135deg, #2a5298 0%, #3d5afe 50%, #2a5298 100%); }
            66% { background: linear-gradient(135deg, #3d5afe 0%, #667eea 50%, #3d5afe 100%); }
        }
        
        .logo-container {
            position: relative;
            margin-bottom: 50px;
            animation: logoFloat 3s ease-in-out infinite;
        }
        
        @keyframes logoFloat {
            0%, 100% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-10px) scale(1.05); }
        }
        
        .logo-bg {
            width: 130px;
            height: 130px;
            background: linear-gradient(45deg, #ff6b6b, #ffa500, #4ecdc4, #45b7d1);
            background-size: 400% 400%;
            border-radius: 30px;
            position: relative;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            animation: gradientRotate 3s ease-in-out infinite;
        }
        
        @keyframes gradientRotate {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .logo-bg::before {
            content: '';
            position: absolute;
            top: -3px;
            left: -3px;
            right: -3px;
            bottom: -3px;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.2), transparent);
            border-radius: 33px;
            animation: shimmer 2s linear infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(200%) rotate(45deg); }
        }
        
        .rocket {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 40px;
            animation: rocketBounce 1.5s ease-in-out infinite;
        }
        
        @keyframes rocketBounce {
            0%, 100% { transform: translate(-50%, -50%) rotate(-5deg); }
            50% { transform: translate(-50%, -55%) rotate(5deg); }
        }
        
        .app-name {
            font-size: 42px;
            font-weight: 700;
            background: linear-gradient(45deg, #4ecdc4, #45b7d1, #96c93d, #ffa500);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 12px;
            animation: textGradient 3s ease-in-out infinite;
            text-align: center;
        }
        
        @keyframes textGradient {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .app-subtitle {
            font-size: 16px;
            color: rgba(255,255,255,0.8);
            margin-bottom: 60px;
            text-align: center;
            animation: fadeInOut 2s ease-in-out infinite;
        }
        
        @keyframes fadeInOut {
            0%, 100% { opacity: 0.8; }
            50% { opacity: 1; }
        }
        
        .gift-icons {
            display: flex;
            gap: 25px;
            margin-bottom: 45px;
            animation: iconsFloat 4s ease-in-out infinite;
        }
        
        @keyframes iconsFloat {
            0%, 100% { transform: translateY(0px); }
            33% { transform: translateY(-6px); }
            66% { transform: translateY(3px); }
        }
        
        .gift-icon {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            animation: iconBounce 2s ease-in-out infinite;
        }
        
        .gift-icon:nth-child(1) {
            background: linear-gradient(45deg, #3498db, #2980b9);
            animation-delay: 0s;
        }
        
        .gift-icon:nth-child(2) {
            background: linear-gradient(45deg, #2ecc71, #27ae60);
            animation-delay: 0.3s;
        }
        
        .gift-icon:nth-child(3) {
            background: linear-gradient(45deg, #f39c12, #e67e22);
            animation-delay: 0.6s;
        }
        
        @keyframes iconBounce {
            0%, 100% { transform: scale(1) rotateY(0deg); }
            50% { transform: scale(1.1) rotateY(180deg); }
        }
        
        .progress-container {
            width: 260px;
            height: 5px;
            background: rgba(255,255,255,0.2);
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 20px;
            position: relative;
        }
        
        .progress-bar {
            width: 0%;
            height: 100%;
            background: linear-gradient(90deg, #4ecdc4, #45b7d1, #96c93d, #ffa500);
            background-size: 400% 100%;
            border-radius: 8px;
            animation: progressGradient 2s linear infinite, progressFill 4s ease-in-out forwards;
            position: relative;
        }
        
        .progress-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: -40px;
            width: 40px;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
            animation: progressShine 2s linear infinite;
        }
        
        @keyframes progressGradient {
            0% { background-position: 0% 50%; }
            100% { background-position: 400% 50%; }
        }
        
        @keyframes progressFill {
            0% { width: 0%; }
            25% { width: 30%; }
            50% { width: 60%; }
            75% { width: 85%; }
            100% { width: 100%; }
        }
        
        @keyframes progressShine {
            0% { left: -40px; }
            100% { left: 100%; }
        }
        
        .loading-text {
            font-size: 15px;
            color: rgba(255,255,255,0.9);
            text-align: center;
            animation: textPulse 1.5s ease-in-out infinite;
        }
        
        @keyframes textPulse {
            0%, 100% { opacity: 0.7; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.02); }
        }
        
        .loading-dots::after {
            content: '';
            animation: dots 1.5s steps(4, end) infinite;
        }
        
        @keyframes dots {
            0%, 20% { content: ''; }
            40% { content: '.'; }
            60% { content: '..'; }
            80%, 100% { content: '...'; }
        }
        
        .particle {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            pointer-events: none;
            animation: float 6s linear infinite;
        }
        
        @keyframes float {
            0% {
                transform: translateY(100vh) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) rotate(360deg);
                opacity: 0;
            }
        }
        
        /* Main App Styles */
        .main-app {
            display: none;
            padding: 20px;
        }
        
        .new-badge {
            background: #4CAF50;
            color: white;
            font-size: 9px;
            padding: 2px 5px;
            border-radius: 8px;
            font-weight: 600;
            margin-left: 4px;
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
        
        /* Category Tabs Styles */
        .category-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .category-tabs.hidden {
            display: none;
        }
        
        .category-tab {
            background: #2a2a3e;
            color: #8b8b8b;
            border: none;
            padding: 8px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            white-space: nowrap;
            flex-shrink: 0;
        }
        
        .category-tab.active {
            background: #3d5afe;
            color: white;
            border-color: #3d5afe;
        }
        
        .category-tab:hover:not(.active) {
            background: #3a3a5c;
            color: white;
        }
        
        .clear-selection-btn {
            background: #ff4757;
            color: white;
            border: none;
            padding: 8px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            margin-left: 10px;
        }
        
        .clear-selection-btn:hover {
            background: #ff3742;
            transform: scale(1.1);
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
        
        /* Фільтри видалені - стилі не потрібні */
        
        .gifts-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        
        /* Gifts Filter List Styles */
        .gifts-filter-grid {
            display: block;
            margin-bottom: 20px;
        }
        
        .gift-filter-item {
            display: flex;
            align-items: center;
            background: #2a2a3e;
            border-radius: 12px;
            padding: 12px 15px;
            margin-bottom: 8px;
            transition: all 0.3s ease;
            cursor: pointer;
            border: 2px solid transparent;
        }
        
        .gift-filter-item:hover {
            background: #3a3a5c;
            border-color: #3d5afe;
        }
        
        .gift-filter-checkbox {
            width: 20px;
            height: 20px;
            background: transparent;
            border: 2px solid #4a4a6a;
            border-radius: 4px;
            margin-right: 20px;
            position: relative;
            flex-shrink: 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .gift-filter-checkbox.checked {
            background: #3d5afe;
            border-color: #3d5afe;
        }
        
        .gift-filter-checkbox.checked::after {
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 12px;
            font-weight: bold;
        }
        
        .gift-filter-image {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            margin-right: 15px;
            background-size: cover;
            background-position: center;
            flex-shrink: 0;
        }
        
        .gift-filter-info {
            flex: 1;
            min-width: 0;
        }
        
        .gift-filter-name {
            color: white;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 4px;
            text-transform: uppercase;
        }
        
        .gift-filter-stats {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .gift-filter-price {
            color: #64B5F6;
            font-size: 14px;
            font-weight: 600;
        }
        
        .gift-filter-count {
            color: rgba(255,255,255,0.7);
            font-size: 14px;
        }
        
        .gift-filter-badge {
            background: #4CAF50;
            color: white;
            font-size: 10px;
            padding: 4px 8px;
            border-radius: 12px;
            font-weight: 600;
            margin-left: 10px;
        }
        
        .gifts-grid.my-channel-grid {
            display: block;
            margin: -20px -20px 0 -20px;
            padding: 0;
        }
        
        /* Gift card main styles for Market */
        .gift-card-main {
            background: #2a2a3e;
            border-radius: 15px;
            padding: 12px;
            text-align: center;
            transition: all 0.3s ease;
            min-height: 160px;
            position: relative;
            cursor: pointer;
            border: 2px solid transparent;
        }
        
        .gift-card-main:hover {
            transform: translateY(-3px);
            border-color: #3d5afe;
            box-shadow: 0 8px 25px rgba(61, 90, 254, 0.3);
        }
        
        .gift-image-main {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            margin: 5px auto 10px;
            background-size: cover;
            background-position: center;
            border: 2px solid rgba(255,255,255,0.2);
            position: relative;
        }
        
        .gift-name-main {
            color: white;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            line-height: 1.1;
            margin-bottom: 4px;
        }
        
        .gift-channel-name {
            color: rgba(255,255,255,0.7);
            font-size: 10px;
            margin-bottom: 6px;
            font-weight: 500;
        }
        
        .gift-price-main {
            background: rgba(0,0,0,0.3);
            color: white;
            padding: 5px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 3px;
            margin-bottom: 6px;
        }
        
        .gift-price-main .ton-icon {
            width: 12px;
            height: 12px;
        }
        
        .gift-count-main {
            color: rgba(255,255,255,0.7);
            font-size: 10px;
        }
        
        /* My Channel WOW Styles */
        .my-channel-container {
            background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
            border-radius: 0;
            padding: 20px 20px 20px 20px;
            margin: 0;
            position: relative;
            overflow: hidden;
            min-height: calc(100vh - 140px);
            width: 100%;
            box-sizing: border-box;
        }
        
        .my-channel-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="%23ffffff" fill-opacity="0.02"><circle cx="30" cy="30" r="4"/></g></svg>') repeat;
            opacity: 0.5;
        }
        
        .channel-header-new {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            position: relative;
            z-index: 2;
            padding-top: 20px;
        }
        
        .channel-title-new {
            color: white;
            font-size: 20px;
            font-weight: 600;
            text-shadow: 0 1px 3px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .channel-icon {
            font-size: 28px;
            animation: channelPulse 2s ease-in-out infinite;
        }
        
        @keyframes channelPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .add-channel-btn {
            background: linear-gradient(45deg, #4299e1, #3182ce);
            color: white;
            border: none;
            padding: 10px 12px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(66,153,225,0.3);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .add-channel-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(66,153,225,0.4);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 25px;
            position: relative;
            z-index: 2;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            background: rgba(255,255,255,0.12);
        }
        
        .stat-number {
            font-size: 20px;
            font-weight: 700;
            color: white;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 11px;
            color: rgba(255,255,255,0.8);
            text-transform: uppercase;
            font-weight: 600;
        }
        
        .empty-state-new {
            text-align: center;
            padding: 40px 20px;
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            flex: 1;
        }
        
        .empty-icon-new {
            font-size: 80px;
            margin-bottom: 25px;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .empty-title-new {
            font-size: 22px;
            color: white;
            margin-bottom: 12px;
            font-weight: 600;
            text-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
        
        .empty-subtitle-new {
            font-size: 15px;
            color: rgba(255,255,255,0.7);
            margin-bottom: 30px;
            line-height: 1.4;
            max-width: 280px;
        }
        
        .create-channel-btn {
            background: linear-gradient(45deg, #4299e1, #3182ce);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(66,153,225,0.3);
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .create-channel-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(66,153,225,0.4);
        }
        
        .floating-add-btn {
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
            border: none;
            border-radius: 50%;
            color: white;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 8px 25px rgba(255,107,107,0.4);
            z-index: 1000;
            transition: all 0.3s ease;
            animation: floatingPulse 3s ease-in-out infinite;
        }
        
        @keyframes floatingPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .floating-add-btn:hover {
            transform: scale(1.15);
            box-shadow: 0 12px 30px rgba(255,107,107,0.6);
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
        
        .channel-listing-card {
            animation: fadeIn 0.6s ease-out;
        }
        
        .filters-hidden {
            display: none;
        }
        
        /* Gifts Modal */
        .gifts-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            z-index: 1000;
            display: none;
        }
        
        .gifts-modal.show {
            display: block;
        }
        
        .gifts-modal-content {
            background: #1a1a2e;
            margin: 0;
            height: 100vh;
            overflow-y: auto;
            position: relative;
        }
        
        .gifts-modal-header {
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
        
        .gifts-modal-title {
            color: white;
            font-size: 18px;
            font-weight: 600;
        }
        
        .gifts-modal-close {
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
        
        .gifts-modal-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            padding: 20px;
        }
        
        .gift-card {
            background: #2a2a3e;
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            transition: transform 0.3s ease;
            min-height: 180px;
            position: relative;
            cursor: pointer;
            border: 2px solid transparent;
        }
        
        .gift-card:hover {
            transform: translateY(-2px);
            border-color: #3d5afe;
        }
        
        .gift-image {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            margin: 0 auto 10px;
            background-size: cover;
            background-position: center;
            border: 2px solid #3a3a5c;
        }
        
        .gift-title {
            color: white;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 6px;
            text-transform: uppercase;
            line-height: 1.2;
        }
        
        .gift-description {
            color: #8b8b8b;
            font-size: 10px;
            margin-bottom: 10px;
            line-height: 1.3;
        }
        
        .gift-count {
            color: rgba(255,255,255,0.7);
            font-size: 10px;
            margin-bottom: 10px;
        }
        
        .buy-channel-btn {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            width: calc(100% - 40px);
            margin: 15px 20px 20px 20px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        
        .buy-channel-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
        }
    </style>
</head>
<body>
    <!-- Loading Screen -->
    <div class="loading-screen" id="loadingScreen">
        <div class="logo-container">
            <div class="logo-bg">
                <div class="rocket">🚀</div>
            </div>
        </div>
        
        <div class="app-name">GiftRoom</div>
        <div class="app-subtitle">Маркетплейс Telegram каналов с подарками</div>
        
        <div class="gift-icons">
            <div class="gift-icon">🎁</div>
            <div class="gift-icon">💎</div>
            <div class="gift-icon">🏆</div>
        </div>
        
        <div class="progress-container">
            <div class="progress-bar"></div>
        </div>
        
        <div class="loading-text">
            <span class="loading-dots">Загрузка подарков</span>
        </div>
    </div>

    <!-- Main App -->
    <div class="main-app" id="mainApp">
        <div class="header">
            <h1>GiftRoom Market</h1>
            <div class="subtitle">Маркетплейс Telegram каналов с подарками</div>
            
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
            <div class="tab active" onclick="switchTab('market')">Маркет</div>
            <div class="tab" onclick="switchTab('my-channels')">Мої канали</div>
        </div>
        
        <!-- Нижні кнопки категорій -->
        <div class="category-tabs">
            <div class="category-tab active" onclick="switchCategory('all')">Всі категорії</div>
            <div class="category-tab" onclick="switchCategory('new')">Нові</div>
            <div class="category-tab" onclick="switchCategory('sorting')">Сортування</div>
            <div class="clear-selection-btn" onclick="clearAllSelections()" style="display: none;">✕</div>
        </div>
        
        <!-- Фільтри видалені -->
        
        <div class="gifts-grid" id="giftsGrid">
            <div class="loading">Загрузка каналов...</div>
        </div>
        
        <!-- Gifts Modal -->
        <div class="gifts-modal" id="giftsModal">
            <div class="gifts-modal-content">
                <div class="gifts-modal-header">
                    <div class="gifts-modal-title" id="modalChannelName">Подарки канала</div>
                    <button class="gifts-modal-close" onclick="closeGiftsModal()">✕</button>
                </div>
                
                <div class="gifts-modal-grid" id="giftsModalGrid">
                    <!-- Подарки будут загружены здесь -->
                </div>
                
                <button class="buy-channel-btn" id="buyChannelBtn" onclick="buyChannelFromModal()">
                    <div class="ton-icon"></div>
                    <span>Купить канал за 0.00 TON</span>
                </button>
            </div>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        // База данных каналов с подарками - всі 37 подарунків з правильними назвами
        const channelListings = [
            {
                id: 1,
                name: "Fashion Style 👠",
                description: "Эксклюзивные подарки модной тематики - обувь, аксессуары и стильные предметы",
                subscribers: 1250,
                posts: 45,
                category: "fashion", 
                price: 25.50,
                owner: "Maria Fashion",
                avatar: "👗",
                dateAdded: new Date('2024-01-15'),
                gifts: [
                    {id: 37, name: "HEELS", desc: "High heels", count: "11500", image: "https://i.postimg.cc/jdsL20Gt/Gifts-Gifts-Gifts-Ag-ADBmg-AAnz-Oe-Ek.png"},
                    {id: 34, name: "SOCKS", desc: "Warm socks", count: "2834", image: "https://i.postimg.cc/bwxCTnmQ/Gifts-Gifts-Gifts-Ag-ADKmk-AAt0-L2-Ek.png"},
                    {id: 2, name: "SWAG BAG", desc: "Stylish bag", count: "34", image: "https://i.postimg.cc/d1cwkrNg/Gifts-Gifts-Gifts-Ag-AD5-XMAAmjze-Us.png"},
                    {id: 36, name: "BUTTON", desc: "Simple button", count: "356", image: "https://i.postimg.cc/XqDSnCRZ/Gifts-Gifts-Gifts-Ag-ADWWg-AAhwgi-Uk.png"},
                    {id: 27, name: "STAR", desc: "Shining star", count: "1240", image: "https://i.postimg.cc/L4y3mTbC/Gifts-Gifts-Gifts-Ag-ADy-XEAAky04-Ek.png"},
                    {id: 31, name: "BOUQUET", desc: "Beautiful bouquet", count: "890", image: "https://i.postimg.cc/V6hvVdKR/Gifts-Gifts-Gifts-Ag-ADi-IYAAqf-LQEs.png"}
                ]
            },
            {
                id: 2,
                name: "Cat Lovers 🐱",
                description: "Милые подарки для любителей котиков и других животных",
                subscribers: 890,
                posts: 32,
                category: "animals",
                price: 15.25,
                owner: "CatMom",
                avatar: "🐱",
                dateAdded: new Date('2024-01-20'),
                gifts: [
                    {id: 35, name: "CATS", desc: "Cute cats", count: "2945", image: "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"},
                    {id: 21, name: "MONKEY", desc: "Playful monkey", count: "1401", image: "https://i.postimg.cc/bN7Yn75Z/Gifts-Gifts-Gifts-Ag-AEZAACV66-BSw.png"},
                    {id: 17, name: "RABBIT", desc: "Fluffy rabbit", count: "967", image: "https://i.postimg.cc/WtLRDv4j/Gifts-Gifts-Gifts-Ag-ADh-HUAAg-O6-IUg.png"},
                    {id: 37, name: "HEELS", desc: "High heels", count: "250", image: "https://i.postimg.cc/jdsL20Gt/Gifts-Gifts-Gifts-Ag-ADBmg-AAnz-Oe-Ek.png"},
                    {id: 14, name: "PIGEON", desc: "City pigeon", count: "723", image: "https://i.postimg.cc/pr1T3ykC/Gifts-Gifts-Gifts-Ag-ADV3-MAAnv-We-Us.png"},
                    {id: 8, name: "EAGLE", desc: "Majestic eagle", count: "567", image: "https://i.postimg.cc/NfJmwjLW/Gifts-Gifts-Gifts-Ag-ADf-GYAAjfaw-Uo.png"}
                ]
            },
            {
                id: 3,
                name: "Tech Store 🔌",
                description: "Технические подарки и современные гаджеты",
                subscribers: 2100,
                posts: 67,
                category: "tech",
                price: 45.00,
                owner: "TechGuru",
                avatar: "⚡",
                dateAdded: new Date('2024-01-10'),
                gifts: [
                    {id: 32, name: "LAMP", desc: "Table lamp", count: "2612", image: "https://i.postimg.cc/hjfNpjzc/Gifts-Gifts-Gifts-Ag-ADj-Gw-AAkl0c-Eo.png"},
                    {id: 28, name: "DYSON", desc: "Powerful vacuum", count: "2178", image: "https://i.postimg.cc/3NZjGj8R/Gifts-Gifts-Gifts-Ag-ADhmw-AAl1-Zc-Uo.png"},
                    {id: 19, name: "ROCKET", desc: "Space rocket", count: "1189", image: "https://i.postimg.cc/nhfZrvs7/Gifts-Gifts-Gifts-Ag-ADIo-UAAk3-J2-Es.png"},
                    {id: 36, name: "BUTTON", desc: "Simple button", count: "890", image: "https://i.postimg.cc/XqDSnCRZ/Gifts-Gifts-Gifts-Ag-ADWWg-AAhwgi-Uk.png"},
                    {id: 11, name: "ESKIMO", desc: "Cold eskimo", count: "456", image: "https://i.postimg.cc/Dfc1Bghf/Gifts-Gifts-Gifts-Ag-ADe-WMAAp-Rw-IUs.png"},
                    {id: 20, name: "BRICK", desc: "Building brick", count: "334", image: "https://i.postimg.cc/tTJGwkf0/Gifts-Gifts-Gifts-Ag-ADBa-UAAk8-WKEg.png"}
                ]
            },
            {
                id: 4,
                name: "Sweet Treats 🧁",
                description: "Сладкие подарки и десерты для сладкоежек",
                subscribers: 756,
                posts: 28,
                category: "food",
                price: 18.75,
                owner: "SweetChef", 
                avatar: "🍰",
                dateAdded: new Date('2024-01-25'),
                gifts: [
                    {id: 30, name: "CUPCAKE", desc: "Sweet cupcake", count: "2390", image: "https://i.postimg.cc/gkqtyRS3/Gifts-Gifts-Gifts-Ag-ADB3-AAAr-Pqc-Eo.png"},
                    {id: 23, name: "DOSHIK", desc: "Instant noodles", count: "1623", image: "https://i.postimg.cc/k5F5qTfB/Gifts-Gifts-Gifts-Ag-AD4-GQAAq8-Xg-Us.png"},
                    {id: 12, name: "CREAMY ICE CREAM", desc: "Creamy ice cream", count: "423", image: "https://i.postimg.cc/ydjXgXYN/Gifts-Gifts-Gifts-Ag-AD0-Ww-AAs4-T4-Ek.png"},
                    {id: 35, name: "CATS", desc: "Cute cats", count: "150", image: "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"},
                    {id: 18, name: "KULICH", desc: "Easter cake", count: "789", image: "https://i.postimg.cc/c1jdyq0F/Gifts-Gifts-Gifts-Ag-ADg2o-AAg-R5g-Us.png"},
                    {id: 22, name: "POOP", desc: "Funny poop", count: "1234", image: "https://i.postimg.cc/gJxk8GG6/Gifts-Gifts-Gifts-Ag-ADMm4-AAj-Ll6-Ug.png"}
                ]
            },
            {
                id: 5,
                name: "Hip Hop Central 🎤",
                description: "Эксклюзивные подарки в стиле хип-хоп культуры",
                subscribers: 1890,
                posts: 54,
                category: "entertainment",
                price: 67.30,
                owner: "SpaceMan",
                avatar: "🌌",
                dateAdded: new Date('2024-01-12'),
                gifts: [
                    {id: 5, name: "WESTSIDE SIGN", desc: "West coast sign", count: "67", image: "https://i.postimg.cc/GtkBTbjx/Gifts-Gifts-Gifts-Ag-ADV4-QAAiibe-Us.png"},
                    {id: 4, name: "LOW RIDER", desc: "Cool car", count: "23", image: "https://i.postimg.cc/7Y96Fsth/Gifts-Gifts-Gifts-Ag-ADNWw-AAg5ze-Es.png"},
                    {id: 1, name: "SNOOP DOGG", desc: "Legendary rapper", count: "15", image: "https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"},
                    {id: 2, name: "SWAG BAG", desc: "Stylish bag", count: "89", image: "https://i.postimg.cc/d1cwkrNg/Gifts-Gifts-Gifts-Ag-AD5-XMAAmjze-Us.png"},
                    {id: 3, name: "SNOOP CIGAR", desc: "Smoking cigar", count: "345", image: "https://i.postimg.cc/FKMsy2zW/Gifts-Gifts-Gifts-Ag-ADi38-AAg-7c-Es.png"},
                    {id: 6, name: "TORCH", desc: "Olympic torch", count: "178", image: "https://i.postimg.cc/wv1LMKPw/Gifts-Gifts-Gifts-Ag-AD2-XQAAk-VPSEs.png"}
                ]
            },
            {
                id: 6,
                name: "Button Collectors 🔘",
                description: "Редкие и уникальные кнопки для коллекционеров",
                subscribers: 456,
                posts: 23,
                category: "misc",
                price: 12.50,
                owner: "ButtonMaster",
                avatar: "🔘",
                dateAdded: new Date('2024-01-28'),
                gifts: [
                    {id: 36, name: "BUTTON", desc: "Simple button", count: "5600", image: "https://i.postimg.cc/XqDSnCRZ/Gifts-Gifts-Gifts-Ag-ADWWg-AAhwgi-Uk.png"},
                    {id: 32, name: "LAMP", desc: "Table lamp", count: "234", image: "https://i.postimg.cc/hjfNpjzc/Gifts-Gifts-Gifts-Ag-ADj-Gw-AAkl0c-Eo.png"},
                    {id: 33, name: "BICEPS", desc: "Strong muscles", count: "567", image: "https://i.postimg.cc/K4Xf7cLq/Gifts-Gifts-Gifts-Ag-ADB3-UAAp5-V0-Uk.png"},
                    {id: 15, name: "MEDAL", desc: "Gold medal", count: "89", image: "https://i.postimg.cc/k5F5qTfB/Gifts-Gifts-Gifts-Ag-AD4-GQAAq8-Xg-Us.png"},
                    {id: 26, name: "CLOVER", desc: "Lucky clover", count: "234", image: "https://i.postimg.cc/85pLSJBg/Gifts-Gifts-Gifts-Ag-ADKX4-AAuw-O2-Ek.png"},
                    {id: 9, name: "NIPPLE", desc: "Baby nipple", count: "567", image: "https://i.postimg.cc/d1y4hTZk/Gifts-Gifts-Gifts-Ag-ADh2o-AAoa-Dc-Eo.png"}
                ]
            },
            {
                id: 7,
                name: "Sports Arena 🏆",
                description: "Спортивные подарки для активных людей",
                subscribers: 1567,
                posts: 41,
                category: "sports",
                price: 33.75,
                owner: "SportsFan",
                avatar: "⚽",
                dateAdded: new Date('2024-01-18'),
                gifts: [
                    {id: 15, name: "MEDAL", desc: "Gold medal", count: "1234", image: "https://i.postimg.cc/k5F5qTfB/Gifts-Gifts-Gifts-Ag-AD4-GQAAq8-Xg-Us.png"},
                    {id: 16, name: "1 MAY", desc: "Labor day", count: "456", image: "https://i.postimg.cc/05HykMdd/Gifts-Gifts-Gifts-Ag-AD82w-AAk-FZg-Es.png"},
                    {id: 29, name: "MARCH 8", desc: "Women's day", count: "789", image: "https://i.postimg.cc/BQrDvwcg/Gifts-Gifts-Gifts-Ag-ADD3-IAAm-RNKUo.png"},
                    {id: 33, name: "BICEPS", desc: "Strong muscles", count: "123", image: "https://i.postimg.cc/K4Xf7cLq/Gifts-Gifts-Gifts-Ag-ADB3-UAAp5-V0-Uk.png"},
                    {id: 10, name: "PLUMBER", desc: "Mario plumber", count: "345", image: "https://i.postimg.cc/TY8BJTRv/Gifts-Gifts-Gifts-Ag-ADk3-AAAiy-WGEs.png"},
                    {id: 7, name: "STATUE", desc: "Ancient statue", count: "678", image: "https://i.postimg.cc/hGFJSzn3/Gifts-Gifts-Gifts-Ag-AD-HEAAq-9c-Us.png"}
                ]
            },
            {
                id: 8,
                name: "Cultural Collection 🏛️",
                description: "Культурные и религиозные подарки",
                subscribers: 892,
                posts: 36,
                category: "misc",
                price: 41.25,
                owner: "CultureKeeper",
                avatar: "🕌",
                dateAdded: new Date('2024-01-22'),
                gifts: [
                    {id: 24, name: "MOSQUE", desc: "Beautiful mosque", count: "234", image: "https://i.postimg.cc/QxJsBFcy/Gifts-Gifts-Gifts-Ag-ADa3-QAAtw-JEEk.png"},
                    {id: 25, name: "AMULET", desc: "Protection amulet", count: "156", image: "https://i.postimg.cc/3Nr1nfbp/Gifts-Gifts-Gifts-Ag-ADbn-UAAl-XNEUk.png"},
                    {id: 27, name: "BOILER", desc: "Hot boiler", count: "789", image: "https://i.postimg.cc/0QXK1ty7/Gifts-Gifts-Gifts-Ag-ADzn-IAAl-Gn-QEs.png"},
                    {id: 7, name: "STATUE", desc: "Ancient statue", count: "345", image: "https://i.postimg.cc/hGFJSzn3/Gifts-Gifts-Gifts-Ag-AD-HEAAq-9c-Us.png"},
                    {id: 13, name: "STAR", desc: "Shining star", count: "567", image: "https://i.postimg.cc/N0zQgZRG/Gifts-Gifts-Gifts-Ag-ADO3c-AAqb-DEEk.png"}
                ]
            }
        ];
        
        let currentView = 'market';
        let currentCategory = 'all';
        let currentChannelModal = null;
        let selectedGiftFilter = null;
        let selectedGifts = new Set(); // Набір вибраних підарунків
        let currentSorting = 'all'; // 'all', 'expensive' або 'cheap'
        let currentFilters = {
            search: '',
            category: '',
            sort: 'recent'
        };
        
        // Loading Screen Logic
        function createParticle() {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.width = particle.style.height = Math.random() * 4 + 2 + 'px';
            particle.style.animationDuration = (Math.random() * 3 + 4) + 's';
            document.querySelector('.loading-screen').appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, 6000);
        }
        
        function startParticles() {
            const particleInterval = setInterval(() => {
                if (document.getElementById('loadingScreen').style.display !== 'none') {
                    createParticle();
                } else {
                    clearInterval(particleInterval);
                }
            }, 300);
        }
        
        function startLoading() {
            startParticles();
            
            const loadingTexts = [
                'Загрузка подарков',
                'Подключение к TON',
                'Синхронизация данных',
                'Подготовка интерфейса',
                'Почти готово'
            ];
            
            let textIndex = 0;
            const textInterval = setInterval(() => {
                if (textIndex < loadingTexts.length) {
                    document.querySelector('.loading-dots').textContent = loadingTexts[textIndex];
                    textIndex++;
                } else {
                    clearInterval(textInterval);
                }
            }, 800);
            
            setTimeout(() => {
                document.getElementById('loadingScreen').style.opacity = '0';
                document.getElementById('loadingScreen').style.transform = 'scale(0.95)';
                document.getElementById('loadingScreen').style.transition = 'all 0.5s ease-in-out';
                
                setTimeout(() => {
                    document.getElementById('loadingScreen').style.display = 'none';
                    document.getElementById('mainApp').style.display = 'block';
                    document.getElementById('mainApp').style.opacity = '0';
                    document.getElementById('mainApp').style.transform = 'translateY(20px)';
                    
                    setTimeout(() => {
                        document.getElementById('mainApp').style.transition = 'all 0.5s ease-out';
                        document.getElementById('mainApp').style.opacity = '1';
                        document.getElementById('mainApp').style.transform = 'translateY(0)';
                        
                        initializeApp();
                    }, 50);
                }, 500);
            }, 4000);
        }
        
        function initializeApp() {
            showMarket();
        }
        
        function applyFilters() {
            const categoryFilter = document.getElementById('categoryFilter').value;
            const sortFilter = document.getElementById('sortFilter').value;
            
            currentFilters.search = '';
            currentFilters.category = categoryFilter;
            currentFilters.sort = sortFilter;
            
            // Если выбран конкретный подарок - показываем каналы с этим подарком
            if (selectedGiftFilter) {
                showChannelsWithGift(selectedGiftFilter);
                return;
            }
            
            let filteredChannels = [...channelListings];
            
            // Фильтр по категории
            if (categoryFilter) {
                filteredChannels = filteredChannels.filter(channel => channel.category === categoryFilter);
            }
            
            // Сортировка
            switch (sortFilter) {
                case 'recent':
                    filteredChannels.sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded));
                    break;
                case 'price_asc':
                    filteredChannels.sort((a, b) => a.price - b.price);
                    break;
                case 'price_desc':
                    filteredChannels.sort((a, b) => b.price - a.price);
                    break;
                case 'subscribers':
                    filteredChannels.sort((a, b) => b.subscribers - a.subscribers);
                    break;
            }
            
            renderChannelListings(filteredChannels);
        }
        
        function showGiftsFilter() {
            // Собираем все уникальные подарки из всех каналов
            const allGifts = new Map();
            
            channelListings.forEach(channel => {
                channel.gifts.forEach(gift => {
                    if (!allGifts.has(gift.id)) {
                        allGifts.set(gift.id, {
                            ...gift,
                            totalCount: parseInt(gift.count),
                            channels: [channel.id]
                        });
                    } else {
                        const existing = allGifts.get(gift.id);
                        existing.totalCount += parseInt(gift.count);
                        if (!existing.channels.includes(channel.id)) {
                            existing.channels.push(channel.id);
                        }
                    }
                });
            });
            
            const giftsArray = Array.from(allGifts.values());
            renderGiftsFilterList(giftsArray);
        }
        
        function renderGiftsFilterList(gifts) {
            const grid = document.getElementById('giftsGrid');
            
            // ID підарунків які є "новими"
            const newGiftIds = [1, 2, 3, 4, 5]; // Snoop Dogg, Swag Bag, Snoop Cigar, Low Rider, Westside Sign
            
            grid.innerHTML = gifts.map(gift => `
                <div class="gift-filter-item" onclick="selectGiftForFilter(${gift.id})">
                    <div class="gift-filter-checkbox ${selectedGifts.has(gift.id) ? 'checked' : ''}" onclick="event.stopPropagation(); toggleGiftSelection(${gift.id})"></div>
                    <div class="gift-filter-image" style="background-image: url('${gift.image}')"></div>
                    <div class="gift-filter-info">
                        <div class="gift-filter-name">${gift.name}</div>
                        <div class="gift-filter-stats">
                            <span class="gift-filter-price">${gift.totalCount} ▽</span>
                            <span class="gift-filter-count">(${gift.channels.length} 🎁)</span>
                        </div>
                    </div>
                    ${newGiftIds.includes(gift.id) ? '<div class="gift-filter-badge">NEW!</div>' : ''}
                </div>
            `).join('');
        }
        
        function toggleGiftSelection(giftId) {
            if (selectedGifts.has(giftId)) {
                selectedGifts.delete(giftId);
            } else {
                selectedGifts.add(giftId);
            }
            
            updateClearButton();
            
            // Оновлюємо відображення
            if (currentCategory === 'new') {
                showAllGiftsFilter();
            } else if (currentCategory === 'all') {
                applyGiftFilter();
            }
        }
        
        function showSortingOptions() {
            document.getElementById('giftsGrid').className = 'gifts-filter-grid';
            
            const grid = document.getElementById('giftsGrid');
            grid.innerHTML = `
                <div class="gift-filter-item" onclick="applySorting('all')">
                    <div class="gift-filter-checkbox ${currentSorting === 'all' ? 'checked' : ''}"></div>
                    <div class="gift-filter-image" style="background: linear-gradient(45deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; font-size: 20px;">📋</div>
                    <div class="gift-filter-info">
                        <div class="gift-filter-name">Всі</div>
                        <div class="gift-filter-stats">
                            <span class="gift-filter-count">Показати всі канали</span>
                        </div>
                    </div>
                </div>
                
                <div class="gift-filter-item" onclick="applySorting('expensive')">
                    <div class="gift-filter-checkbox ${currentSorting === 'expensive' ? 'checked' : ''}"></div>
                    <div class="gift-filter-image" style="background: linear-gradient(45deg, #ffd700, #ffed4e); display: flex; align-items: center; justify-content: center; font-size: 20px;">💰</div>
                    <div class="gift-filter-info">
                        <div class="gift-filter-name">Дорогі → Дешеві</div>
                        <div class="gift-filter-stats">
                            <span class="gift-filter-count">Спочатку дорожчі</span>
                        </div>
                    </div>
                </div>
                
                <div class="gift-filter-item" onclick="applySorting('cheap')">
                    <div class="gift-filter-checkbox ${currentSorting === 'cheap' ? 'checked' : ''}"></div>
                    <div class="gift-filter-image" style="background: linear-gradient(45deg, #4ecdc4, #44a08d); display: flex; align-items: center; justify-content: center; font-size: 20px;">💸</div>
                    <div class="gift-filter-info">
                        <div class="gift-filter-name">Дешеві → Дорогі</div>
                        <div class="gift-filter-stats">
                            <span class="gift-filter-count">Спочатку дешевші</span>
                        </div>
                    </div>
                </div>
            `;
        }
        
        function applySorting(sortType) {
            currentSorting = sortType;
            updateClearButton();
            
            // Оновлюємо відображення опцій сортування
            showSortingOptions();
        }
        
        function updateClearButton() {
            const clearBtn = document.querySelector('.clear-selection-btn');
            const hasSelections = selectedGifts.size > 0 || currentSorting !== 'all';
            
            if (hasSelections) {
                clearBtn.style.display = 'flex';
            } else {
                clearBtn.style.display = 'none';
            }
        }
        
        function clearAllSelections() {
            selectedGifts.clear();
            currentSorting = 'all';
            
            updateClearButton();
            
            // Оновлюємо відображення
            if (currentCategory === 'new') {
                showAllGiftsFilter();
            } else if (currentCategory === 'all') {
                applyGiftFilter();
            } else if (currentCategory === 'sorting') {
                showSortingOptions();
            }
        }
        
        function selectGiftForFilter(giftId) {
            // Ця функція замінює стару selectGiftFilter
            selectedGiftFilter = giftId;
            showChannelsWithGift(giftId);
        }
        
        function applyGiftFilter() {
            let channelsToShow = channelListings;
            
            // Фільтруємо за вибраними підарунками
            if (selectedGifts.size > 0) {
                channelsToShow = channelListings.filter(channel => {
                    return channel.gifts.some(gift => selectedGifts.has(gift.id));
                });
            }
            
            // Сортуємо за ціною
            if (currentSorting === 'expensive') {
                channelsToShow.sort((a, b) => b.price - a.price); // дорогі → дешеві
            } else if (currentSorting === 'cheap') {
                channelsToShow.sort((a, b) => a.price - b.price); // дешеві → дорогі
            }
            // Якщо currentSorting === 'all', залишаємо оригінальний порядок
            
            renderChannelListings(channelsToShow);
        }
        
        function selectGiftFilter(giftId) {
            selectedGiftFilter = giftId;
            showChannelsWithGift(giftId);
        }
        
        function showChannelsWithGift(giftId) {
            // Находим все каналы где этот подарок является ПЕРВЫМ (главным)
            const channelsWithGift = channelListings.filter(channel => 
                channel.gifts.length > 0 && channel.gifts[0].id === giftId
            );
            
            // Сортируем по количеству этого подарка (у кого больше)
            channelsWithGift.sort((a, b) => {
                const aGift = a.gifts.find(gift => gift.id === giftId);
                const bGift = b.gifts.find(gift => gift.id === giftId);
                return parseInt(bGift.count) - parseInt(aGift.count);
            });
            
            renderChannelListings(channelsWithGift);
        }
        
        function clearFilters() {
            selectedGiftFilter = null;
            currentFilters = { search: '', category: '', sort: 'recent' };
            renderChannelListings(channelListings);
        }
        
        function renderChannelListings(channelsToRender) {
            const grid = document.getElementById('giftsGrid');
            
            if (channelsToRender.length === 0) {
                grid.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 18px; margin-bottom: 10px;">Каналы не найдены</div>
                        <div style="font-size: 14px;">Этот подарок не является главным ни в одном канале</div>
                    </div>
                `;
                return;
            }
            
            grid.innerHTML = channelsToRender.map(channel => {
                // Берем ПЕРВЫЙ подарок как главный
                const mainGift = channel.gifts[0];
                
                return `
                    <div class="gift-card-main" onclick="openGiftsModal(${channel.id})">
                        <div class="gift-image-main" style="background-image: url('${mainGift.image}')"></div>
                        <div class="gift-name-main">${mainGift.name}</div>
                        <div class="gift-channel-name">${channel.name}</div>
                        <div class="gift-price-main">
                            <div class="ton-icon"></div>
                            <span>${channel.price} TON</span>
                        </div>
                        <div class="gift-count-main">${mainGift.count} шт</div>
                    </div>
                `;
            }).join('');
        }
        
        function showMarket() {
            document.querySelector('.category-tabs').classList.remove('hidden');
            document.getElementById('giftsGrid').className = 'gifts-grid';
            selectedGiftFilter = null;
            
            if (currentCategory === 'all') {
                applyGiftFilter();
            } else if (currentCategory === 'new') {
                showAllGiftsFilter();
            }
        }
        
        function showMyChannels() {
            document.querySelector('.category-tabs').classList.add('hidden');
            const grid = document.getElementById('giftsGrid');
            grid.className = 'gifts-grid my-channel-grid';
            grid.innerHTML = `
                <div class="my-channel-container">
                    <div class="channel-header-new">
                        <div class="channel-title-new">
                            <span class="channel-icon">📺</span>
                            Мои каналы
                        </div>
                        <button class="add-channel-btn" onclick="createChannel()">
                            <span>+</span>
                            Добавить
                        </button>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">0</div>
                            <div class="stat-label">Каналов</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">0</div>
                            <div class="stat-label">Подписчиков</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">0</div>
                            <div class="stat-label">Доход TON</div>
                        </div>
                    </div>
                    
                    <div class="empty-state-new">
                        <div class="empty-icon-new">🚀</div>
                        <div class="empty-title-new">Создайте свой первый канал!</div>
                        <div class="empty-subtitle-new">
                            Начните продавать подарки через Telegram канал
                            и зарабатывайте TON каждый день
                        </div>
                        <button class="create-channel-btn" onclick="createChannel()">
                            <span>📺</span>
                            Создать канал
                        </button>
                    </div>
                </div>
            `;
        }
        
        function showAllGiftsFilter() {
            document.getElementById('giftsGrid').className = 'gifts-filter-grid';
            
            // Собираем все уникальные подарки из всех каналов
            const allGifts = new Map();
            
            channelListings.forEach(channel => {
                channel.gifts.forEach(gift => {
                    if (!allGifts.has(gift.id)) {
                        allGifts.set(gift.id, {
                            ...gift,
                            totalCount: parseInt(gift.count),
                            channels: [channel.id]
                        });
                    } else {
                        const existing = allGifts.get(gift.id);
                        existing.totalCount += parseInt(gift.count);
                        if (!existing.channels.includes(channel.id)) {
                            existing.channels.push(channel.id);
                        }
                    }
                });
            });
            
            const giftsArray = Array.from(allGifts.values());
            
            // Сортируем в прямому порядку по ID (від 1 до 37)
            giftsArray.sort((a, b) => a.id - b.id);
            
            renderGiftsFilterList(giftsArray);
        }
        
        function switchCategory(category) {
            currentCategory = category;
            
            document.querySelectorAll('.category-tab').forEach(t => t.classList.remove('active'));
            
            if (category === 'all') {
                document.querySelectorAll('.category-tab')[0].classList.add('active');
                if (currentView === 'market') {
                    document.getElementById('giftsGrid').className = 'gifts-grid';
                    applyGiftFilter();
                }
            } else if (category === 'new') {
                document.querySelectorAll('.category-tab')[1].classList.add('active');
                if (currentView === 'market') {
                    document.getElementById('giftsGrid').className = 'gifts-filter-grid';
                    showAllGiftsFilter();
                }
            } else if (category === 'sorting') {
                document.querySelectorAll('.category-tab')[2].classList.add('active');
                if (currentView === 'market') {
                    showSortingOptions();
                }
            }
            
            updateClearButton();
        }
        
        function openGiftsModal(channelId) {
            const channel = channelListings.find(c => c.id === channelId);
            if (!channel) return;
            
            currentChannelModal = channel;
            
            document.getElementById('modalChannelName').textContent = `Подарки канала ${channel.name}`;
            document.getElementById('buyChannelBtn').innerHTML = `
                <div class="ton-icon"></div>
                <span>Купить канал за ${channel.price} TON</span>
            `;
            
            const giftsGrid = document.getElementById('giftsModalGrid');
            
            giftsGrid.innerHTML = channel.gifts.map(gift => `
                <div class="gift-card">
                    <div class="gift-image" style="background-image: url('${gift.image}')"></div>
                    <div class="gift-title">${gift.name}</div>
                    <div class="gift-description">${gift.desc}</div>
                    <div class="gift-count">${gift.count} шт</div>
                </div>
            `).join('');
            
            document.getElementById('giftsModal').classList.add('show');
        }
        
        function closeGiftsModal() {
            document.getElementById('giftsModal').classList.remove('show');
            currentChannelModal = null;
        }
        
        function buyChannelFromModal() {
            if (currentChannelModal) {
                tg.showAlert(`Покупка канала: ${currentChannelModal.name}\\nЦена: ${currentChannelModal.price} TON\\n\\nДля завершения покупки подключите TON кошелек`);
                closeGiftsModal();
            }
        }
        
        function switchTab(tab) {
            currentView = tab;
            
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            
            if (tab === 'market') {
                document.querySelectorAll('.tab')[0].classList.add('active');
                showMarket();
            } else if (tab === 'my-channels') {
                document.querySelectorAll('.tab')[1].classList.add('active');
                showMyChannels();
            }
        }
        
        function createChannel() {
            tg.showAlert('Создание Telegram канала для продажи подарков');
        }
        
        function connectWallet() {
            tg.showAlert('Подключение к TON кошельку...');
        }
        
        function addBalance() {
            tg.showAlert('Пополнение баланса');
        }
        
        function withdrawBalance() {
            tg.showAlert('Вывод средств');
        }
        
        // Start loading when page loads
        window.addEventListener('load', startLoading);
        
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
        f"📺 Маркетплейс Telegram каналов с подарками\n"
        f"🎁 37 уникальных подарков\n"
        f"💎 Создавай каналы и продавай подарки\n"
        f"💰 Зарабатывай TON с каждой продажи\n\n"
        f"Нажми кнопку чтобы открыть магазин:",
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
    
    print("🎁 GiftRoom Market без системы рідкісності запущен!")
    print(f"🌐 URL: {WEBAPP_URL}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
