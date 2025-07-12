# main.py - FastAPI приложение для GiftRoom Market - Маркетплейс каналов
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
        
        /* Фільтри */
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
        
        .channels-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        /* Channel Card Styles */
        .channel-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #363654 100%);
            border-radius: 18px;
            padding: 20px;
            border: 2px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .channel-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            transition: left 0.5s ease;
        }
        
        .channel-card:hover::before {
            left: 100%;
        }
        
        .channel-card:hover {
            transform: translateY(-5px);
            border-color: #3d5afe;
            box-shadow: 0 10px 30px rgba(61, 90, 254, 0.3);
        }
        
        .channel-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .channel-avatar {
            width: 50px;
            height: 50px;
            background: linear-gradient(45deg, #ff9a9e, #fecfef, #ffecd2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        .channel-info h3 {
            color: white;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 5px;
            line-height: 1.2;
        }
        
        .channel-info p {
            color: rgba(255,255,255,0.7);
            font-size: 13px;
            margin: 0;
        }
        
        .channel-stats {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .stat-item {
            display: flex;
            align-items: center;
            gap: 5px;
            color: rgba(255,255,255,0.8);
            font-size: 12px;
        }
        
        .stat-icon {
            font-size: 14px;
        }
        
        .channel-tags {
            display: flex;
            gap: 6px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        
        .tag {
            background: rgba(61, 90, 254, 0.2);
            color: #64B5F6;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }
        
        .channel-price {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 15px;
        }
        
        .price-display {
            display: flex;
            align-items: center;
            gap: 6px;
            color: white;
            font-size: 16px;
            font-weight: 600;
        }
        
        .buy-btn {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .buy-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
        }
        
        /* My Channel Styles */
        .my-channel-container {
            background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
            border-radius: 0;
            padding: 20px;
            margin: -20px -20px 0 -20px;
            position: relative;
            overflow: hidden;
            min-height: calc(100vh - 140px);
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
            padding: 10px 15px;
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
            margin-left: auto;
            margin-right: auto;
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
        
        /* Add Channel Form */
        .add-channel-form {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 18px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.2);
            position: relative;
            z-index: 2;
            margin-bottom: 20px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-label {
            color: white;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
            display: block;
        }
        
        .form-input {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            padding: 12px 15px;
            color: white;
            width: 100%;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        
        .form-input:focus {
            outline: none;
            border-color: #3d5afe;
            background: rgba(255,255,255,0.15);
        }
        
        .form-input::placeholder {
            color: rgba(255,255,255,0.5);
        }
        
        .form-textarea {
            min-height: 80px;
            resize: vertical;
        }
        
        .form-select {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            padding: 12px 15px;
            color: white;
            width: 100%;
            font-size: 14px;
        }
        
        .form-select option {
            background: #2a2a3e;
            color: white;
        }
        
        .form-buttons {
            display: flex;
            gap: 12px;
            margin-top: 25px;
        }
        
        .btn-cancel {
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            flex: 1;
            transition: all 0.3s ease;
        }
        
        .btn-cancel:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .btn-submit {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            flex: 2;
            transition: all 0.3s ease;
        }
        
        .btn-submit:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
        }
        
        .floating-add-btn {
            position: fixed;
            bottom: 30px;
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
        
        .channel-card {
            animation: fadeIn 0.6s ease-out;
        }
        
        .filters-hidden {
            display: none;
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
            <div class="gift-icon">📺</div>
            <div class="gift-icon">💎</div>
            <div class="gift-icon">💰</div>
        </div>
        
        <div class="progress-container">
            <div class="progress-bar"></div>
        </div>
        
        <div class="loading-text">
            <span class="loading-dots">Загрузка каналов</span>
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
            <div class="tab" onclick="switchTab('my-channel')">Мої канали</div>
        </div>
        
        <!-- Фільтри (показываются только в Market) -->
        <div class="filters-section" id="filtersSection">
            <input type="text" class="search-box" placeholder="Поиск каналов..." id="searchBox" onkeyup="applyFilters()">
            <div class="filter-row">
                <select class="filter-select" id="categoryFilter" onchange="applyFilters()">
                    <option value="">Все категории</option>
                    <option value="fashion">Мода</option>
                    <option value="food">Еда</option>
                    <option value="animals">Животные</option>
                    <option value="tech">Технологии</option>
                    <option value="entertainment">Развлечения</option>
                    <option value="sports">Спорт</option>
                    <option value="misc">Разное</option>
                </select>
                
                <select class="filter-select" id="sortFilter" onchange="applyFilters()">
                    <option value="recent">Новые</option>
                    <option value="price_asc">Цена: мин → макс</option>
                    <option value="price_desc">Цена: макс → мин</option>
                    <option value="subscribers">По подписчикам</option>
                </select>
                
                <button class="clear-filters-btn" onclick="clearFilters()" title="Очистить фильтры">✕</button>
            </div>
        </div>
        
        <div class="channels-grid" id="channelsGrid">
            <div class="loading">Загрузка каналов...</div>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        // База данных каналов (демо-данные)
        let channels = [
            {
                id: 1,
                name: "Fashion Style 👠",
                description: "Эксклюзивные подарки модной тематики",
                subscribers: 1250,
                posts: 45,
                category: "fashion",
                price: 25.50,
                owner: "Maria Fashion",
                avatar: "👗",
                tags: ["мода", "стиль", "обувь"],
                dateAdded: new Date('2024-01-15')
            },
            {
                id: 2,
                name: "Cat Lovers 🐱",
                description: "Милые подарки для любителей котиков",
                subscribers: 890,
                posts: 32,
                category: "animals",
                price: 15.25,
                owner: "CatMom",
                avatar: "🐱",
                tags: ["котики", "животные", "мило"],
                dateAdded: new Date('2024-01-20')
            },
            {
                id: 3,
                name: "Tech Store 🔌",
                description: "Технические подарки и гаджеты",
                subscribers: 2100,
                posts: 67,
                category: "tech",
                price: 45.00,
                owner: "TechGuru",
                avatar: "⚡",
                tags: ["техника", "гаджеты", "инновации"],
                dateAdded: new Date('2024-01-10')
            },
            {
                id: 4,
                name: "Sweet Treats 🧁",
                description: "Сладкие подарки и десерты",
                subscribers: 756,
                posts: 28,
                category: "food",
                price: 18.75,
                owner: "SweetChef",
                avatar: "🍰",
                tags: ["сладости", "десерты", "выпечка"],
                dateAdded: new Date('2024-01-25')
            },
            {
                id: 5,
                name: "Space Explorer 🚀",
                description: "Космические подарки и артефакты",
                subscribers: 1890,
                posts: 54,
                category: "entertainment",
                price: 67.30,
                owner: "SpaceMan",
                avatar: "🌌",
                tags: ["космос", "наука", "футуристика"],
                dateAdded: new Date('2024-01-12')
            }
        ];
        
        let currentView = 'market';
        let showAddForm = false;
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
                'Загрузка каналов',
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
        
        // Применение фильтров
        function applyFilters() {
            const searchValue = document.getElementById('searchBox').value.toLowerCase();
            const categoryFilter = document.getElementById('categoryFilter').value;
            const sortFilter = document.getElementById('sortFilter').value;
            
            currentFilters.search = searchValue;
            currentFilters.category = categoryFilter;
            currentFilters.sort = sortFilter;
            
            let filteredChannels = [...channels];
            
            // Поиск по названию и описанию
            if (searchValue) {
                filteredChannels = filteredChannels.filter(channel => 
                    channel.name.toLowerCase().includes(searchValue) ||
                    channel.description.toLowerCase().includes(searchValue) ||
                    channel.owner.toLowerCase().includes(searchValue)
                );
            }
            
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
            
            renderChannels(filteredChannels);
        }
        
        function clearFilters() {
            document.getElementById('searchBox').value = '';
            document.getElementById('categoryFilter').value = '';
            document.getElementById('sortFilter').value = 'recent';
            currentFilters = { search: '', category: '', sort: 'recent' };
            renderChannels(channels);
        }
        
        function renderChannels(channelsToRender) {
            const grid = document.getElementById('channelsGrid');
            
            if (channelsToRender.length === 0) {
                grid.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 18px; margin-bottom: 10px;">Каналы не найдены</div>
                        <div style="font-size: 14px;">Попробуйте изменить параметры поиска</div>
                    </div>
                `;
                return;
            }
            
            grid.innerHTML = channelsToRender.map(channel => `
                <div class="channel-card" onclick="viewChannel(${channel.id})">
                    <div class="channel-header">
                        <div class="channel-avatar">${channel.avatar}</div>
                        <div class="channel-info">
                            <h3>${channel.name}</h3>
                            <p>от ${channel.owner}</p>
                        </div>
                    </div>
                    
                    <div class="channel-stats">
                        <div class="stat-item">
                            <span class="stat-icon">👥</span>
                            <span>${channel.subscribers}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-icon">📝</span>
                            <span>${channel.posts}</span>
                        </div>
                    </div>
                    
                    <div class="channel-tags">
                        ${channel.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                    </div>
                    
                    <p style="color: rgba(255,255,255,0.8); font-size: 13px; margin-bottom: 15px;">${channel.description}</p>
                    
                    <div class="channel-price">
                        <div class="price-display">
                            <div class="ton-icon"></div>
                            <span>${channel.price} TON</span>
                        </div>
                        <button class="buy-btn" onclick="event.stopPropagation(); buyChannel(${channel.id})">
                            Купить
                        </button>
                    </div>
                </div>
            `).join('');
        }
        
        function showMarket() {
            document.getElementById('filtersSection').classList.remove('filters-hidden');
            renderChannels(channels);
        }
        
        function showMyChannel() {
            document.getElementById('filtersSection').classList.add('filters-hidden');
            const grid = document.getElementById('channelsGrid');
            
            if (showAddForm) {
                renderAddChannelForm();
            } else {
                // Показываем пустое состояние или мои каналы
                renderMyChannels();
            }
        }
        
        function renderMyChannels() {
            const grid = document.getElementById('channelsGrid');
            grid.innerHTML = `
                <div class="my-channel-container">
                    <div class="channel-header-new">
                        <div class="channel-title-new">
                            <span class="channel-icon">📺</span>
                            Мои каналы
                        </div>
                        <button class="add-channel-btn" onclick="showAddChannelForm()">
                            <span>+</span>
                            Добавить канал
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
                        <div class="empty-icon-new">📺</div>
                        <div class="empty-title-new">Добавьте свой первый канал!</div>
                        <div class="empty-subtitle-new">
                            Начните продавать доступ к своему Telegram каналу 
                            с эксклюзивными подарками и зарабатывайте TON
                        </div>
                        <button class="create-channel-btn" onclick="showAddChannelForm()">
                            <span>📺</span>
                            Создать канал
                        </button>
                    </div>
                </div>
                
                <button class="floating-add-btn" onclick="showAddChannelForm()">+</button>
            `;
        }
        
        function renderAddChannelForm() {
            const grid = document.getElementById('channelsGrid');
            grid.innerHTML = `
                <div class="my-channel-container">
                    <div class="channel-header-new">
                        <div class="channel-title-new">
                            <span class="channel-icon">➕</span>
                            Добавить канал
                        </div>
                        <button class="add-channel-btn" onclick="hideAddChannelForm()">
                            <span>←</span>
                            Назад
                        </button>
                    </div>
                    
                    <div class="add-channel-form">
                        <div class="form-group">
                            <label class="form-label">Название канала</label>
                            <input type="text" class="form-input" id="channelName" placeholder="Например: Fashion Style 👠">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Описание</label>
                            <textarea class="form-input form-textarea" id="channelDesc" placeholder="Расскажите о подарках в вашем канале..."></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Категория</label>
                            <select class="form-select" id="channelCategory">
                                <option value="">Выберите категорию</option>
                                <option value="fashion">Мода</option>
                                <option value="food">Еда</option>
                                <option value="animals">Животные</option>
                                <option value="tech">Технологии</option>
                                <option value="entertainment">Развлечения</option>
                                <option value="sports">Спорт</option>
                                <option value="misc">Разное</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Цена (TON)</label>
                            <input type="number" class="form-input" id="channelPrice" placeholder="0.00" step="0.01" min="0">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Количество подписчиков</label>
                            <input type="number" class="form-input" id="channelSubs" placeholder="Например: 1000" min="0">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Ссылка на канал</label>
                            <input type="text" class="form-input" id="channelLink" placeholder="@your_channel или t.me/your_channel">
                        </div>
                        
                        <div class="form-buttons">
                            <button class="btn-cancel" onclick="hideAddChannelForm()">Отмена</button>
                            <button class="btn-submit" onclick="submitChannel()">Добавить канал</button>
                        </div>
                    </div>
                </div>
            `;
        }
        
        function showAddChannelForm() {
            showAddForm = true;
            renderAddChannelForm();
        }
        
        function hideAddChannelForm() {
            showAddForm = false;
            renderMyChannels();
        }
        
        function submitChannel() {
            const name = document.getElementById('channelName').value.trim();
            const description = document.getElementById('channelDesc').value.trim();
            const category = document.getElementById('channelCategory').value;
            const price = parseFloat(document.getElementById('channelPrice').value);
            const subscribers = parseInt(document.getElementById('channelSubs').value);
            const link = document.getElementById('channelLink').value.trim();
            
            if (!name || !description || !category || !price || !subscribers || !link) {
                tg.showAlert('Пожалуйста, заполните все поля');
                return;
            }
            
            // Создаем новый канал
            const newChannel = {
                id: channels.length + 1,
                name: name,
                description: description,
                subscribers: subscribers,
                posts: Math.floor(Math.random() * 50) + 10, // Случайное количество постов
                category: category,
                price: price,
                owner: "Вы", // В реальном приложении это будет имя пользователя
                avatar: getRandomAvatar(category),
                tags: getTagsForCategory(category),
                dateAdded: new Date()
            };
            
            channels.unshift(newChannel); // Добавляем в начало массива
            
            tg.showAlert('Канал успешно добавлен!');
            hideAddChannelForm();
            
            // Переключаемся на маркет, чтобы показать добавленный канал
            setTimeout(() => {
                switchTab('market');
            }, 1000);
        }
        
        function getRandomAvatar(category) {
            const avatars = {
                fashion: ['👗', '👠', '💄', '👜'],
                food: ['🍰', '🧁', '🍕', '🍔'],
                animals: ['🐱', '🐶', '🐰', '🦊'],
                tech: ['⚡', '💻', '📱', '🔌'],
                entertainment: ['🎬', '🎮', '🎵', '🎨'],
                sports: ['⚽', '🏀', '🏆', '🥇'],
                misc: ['⭐', '💎', '🔥', '✨']
            };
            
            const categoryAvatars = avatars[category] || avatars.misc;
            return categoryAvatars[Math.floor(Math.random() * categoryAvatars.length)];
        }
        
        function getTagsForCategory(category) {
            const tags = {
                fashion: ['мода', 'стиль', 'одежда'],
                food: ['еда', 'рецепты', 'кулинария'],
                animals: ['животные', 'питомцы', 'милота'],
                tech: ['технологии', 'гаджеты', 'инновации'],
                entertainment: ['развлечения', 'фильмы', 'игры'],
                sports: ['спорт', 'фитнес', 'здоровье'],
                misc: ['разное', 'интересное', 'полезное']
            };
            
            return tags[category] || tags.misc;
        }
        
        function switchTab(tab) {
            currentView = tab;
            showAddForm = false;
            
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            
            if (tab === 'market') {
                document.querySelectorAll('.tab')[0].classList.add('active');
                showMarket();
            } else if (tab === 'my-channel') {
                document.querySelectorAll('.tab')[1].classList.add('active');
                showMyChannel();
            }
        }
        
        function viewChannel(id) {
            const channel = channels.find(c => c.id === id);
            tg.showAlert(`Просмотр канала: ${channel.name}\\n\\nОписание: ${channel.description}\\n\\nПодписчики: ${channel.subscribers}\\nЦена: ${channel.price} TON`);
        }
        
        function buyChannel(id) {
            const channel = channels.find(c => c.id === id);
            tg.showAlert(`Покупка канала: ${channel.name}\\nЦена: ${channel.price} TON\\n\\nДля завершения покупки подключите TON кошелек`);
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
        f"💰 Продавайте доступ к своим каналам\n"
        f"🎁 Покупайте эксклюзивные каналы с подарками\n"
        f"💎 Зарабатывайте TON с каждой продажи\n\n"
        f"Нажми кнопку чтобы открыть маркетплейс:",
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
    
    print("🎁 GiftRoom Market - Маркетплейс каналов запущен!")
    print(f"🌐 URL: {WEBAPP_URL}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
