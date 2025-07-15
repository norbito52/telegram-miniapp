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
            background: #0F0F19;
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
        
        /* Profile Page Styles - ОНОВЛЕНІ СТИЛІ */
        .profile-container {
            background: #0F0F19;
            padding: 0;
            height: calc(100vh - 160px);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            position: relative;
            margin: 0;
            width: 100%;
        }
        
        .profile-avatar-container {
            text-align: center;
            width: 100%;
            max-width: 300px;
            position: relative;
            z-index: 2;
            margin: 0 auto;
        }
        
        .profile-avatar {
            width: 120px;
            height: 120px;
            border-radius: 12px;
            background: linear-gradient(135deg, #4285f4 0%, #34a853 25%, #fbbc04 50%, #ea4335 75%, #9c27b0 100%);
            margin: 0 auto 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 42px;
            font-weight: 700;
            color: white;
            box-shadow: 0 15px 35px rgba(66, 133, 244, 0.4);
            border: 3px solid rgba(255,255,255,0.15);
            animation: profileFloat 3s ease-in-out infinite;
            background-size: cover;
            background-position: center;
            position: relative;
            overflow: hidden;
        }
        
        .profile-avatar::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            right: -50%;
            bottom: -50%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: shimmer 2.5s linear infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(200%) rotate(45deg); }
        }
        
        @keyframes profileFloat {
            0%, 100% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-8px) scale(1.05); }
        }
        
        .profile-username {
            font-size: 32px;
            font-weight: 700;
            color: white;
            margin-bottom: 50px;
            line-height: 1.2;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .profile-stats {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            gap: 30px;
            width: 100%;
            max-width: 350px;
        }
        
        .profile-stat {
            text-align: center;
            flex: 1;
        }
        
        .profile-stat-value {
            font-size: 28px;
            font-weight: 700;
            color: white;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .profile-stat-label {
            font-size: 11px;
            color: rgba(255,255,255,0.7);
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        
        .ton-symbol {
            width: 18px;
            height: 18px;
            background-image: url('https://i.postimg.cc/kX2nWB4M/121-20250711185549.png');
            background-size: cover;
            background-position: center;
            border-radius: 50%;
        }
        
        .gift-icon-stat {
            font-size: 18px;
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
        
        .gifts-grid.profile-grid {
            display: flex !important;
            align-items: flex-start !important;
            justify-content: center !important;
            height: 100vh !important;
            margin: 0 !important;
            padding: 40px 0 0 0 !important;
            grid-template-columns: none !important;
            gap: 0 !important;
        }
        
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
            background: #2196F3;
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
        
        /* My Ads Container Styles */
        .my-ads-container {
            background: #0F0F19;
            padding: 20px;
            min-height: calc(100vh - 140px);
        }
        
        .my-ads-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            border-bottom: 1px solid #2a2a3e;
            padding-bottom: 15px;
        }
        
        .my-ads-title {
            color: white;
            font-size: 20px;
            font-weight: 600;
        }
        
        .add-ad-btn {
            background: #3d5afe;
            color: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 20px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .add-ad-btn:hover {
            background: #5c7cfa;
            transform: scale(1.05);
        }
        
        /* Empty State Styles */
        .empty-ads-state {
            text-align: center;
            padding: 60px 20px;
        }
        
        .empty-ads-icon {
            margin-bottom: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .empty-ads-icon img {
            filter: drop-shadow(0 8px 20px rgba(0,0,0,0.3));
            animation: giftFloat 3s ease-in-out infinite;
            background: transparent;
        }
        
        @keyframes giftFloat {
            0%, 100% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-10px) scale(1.05); }
        }
        
        @keyframes modalSlideOut {
            from { 
                opacity: 1;
                transform: translateY(0);
            }
            to { 
                opacity: 0;
                transform: translateY(100%);
            }
        }
        
        .empty-ads-title {
            font-size: 22px;
            color: white;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        .empty-ads-subtitle {
            font-size: 16px;
            color: rgba(255,255,255,0.7);
            margin-bottom: 30px;
        }
        
        .create-ad-btn {
            background: #3d5afe;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .create-ad-btn:hover {
            background: #5c7cfa;
            transform: translateY(-2px);
        }
        
        /* Create Ad Form Styles */
        .create-ad-container {
            background: #0F0F19;
            padding: 0;
            min-height: 100vh;
        }
        
        .create-ad-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            border-bottom: 1px solid #2a2a3e;
            background: #0F0F19;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        
        .back-btn {
            background: none;
            border: none;
            color: white;
            font-size: 18px;
            cursor: pointer;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .back-btn:hover {
            background: #2a2a3e;
        }
        
        .create-ad-title {
            color: white;
            font-size: 18px;
            font-weight: 600;
        }
        
        .create-ad-form {
            padding: 20px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-label {
            display: block;
            color: white;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .form-input {
            width: 100%;
            background: #2a2a3e;
            border: 2px solid #3a3a5c;
            border-radius: 12px;
            padding: 12px 15px;
            color: white;
            font-size: 16px;
            transition: all 0.3s ease;
            box-sizing: border-box;
        }
        
        .form-input:focus {
            outline: none;
            border-color: #3d5afe;
            box-shadow: 0 0 0 3px rgba(61, 90, 254, 0.1);
        }
        
        .form-input::placeholder {
            color: rgba(255,255,255,0.5);
        }
        
        .form-help {
            color: rgba(255,255,255,0.6);
            font-size: 14px;
            margin-top: 6px;
        }
        
        /* Important Info Styles */
        .important-info {
            background: rgba(255, 193, 7, 0.1);
            border: 1px solid rgba(255, 193, 7, 0.3);
            border-radius: 12px;
            padding: 15px;
            margin: 20px 0;
            display: flex;
            gap: 12px;
        }
        
        .info-icon {
            font-size: 20px;
            flex-shrink: 0;
        }
        
        .info-content {
            flex: 1;
        }
        
        .info-title {
            color: #ffc107;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .info-text {
            color: rgba(255,255,255,0.9);
            font-size: 14px;
            margin-bottom: 8px;
        }
        
        .info-list {
            margin-bottom: 12px;
        }
        
        .info-item {
            color: rgba(255,255,255,0.8);
            font-size: 14px;
            margin-bottom: 4px;
        }
        
        .req-title {
            color: rgba(255,255,255,0.9);
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 6px;
        }
        
        .req-item {
            color: rgba(255,255,255,0.8);
            font-size: 14px;
            margin-bottom: 3px;
        }
        
        .create-btn {
            width: 100%;
            background: #3d5afe;
            color: white;
            border: none;
            padding: 15px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            margin-top: 20px;
            transition: all 0.3s ease;
        }
        
        .create-btn:hover {
            background: #5c7cfa;
            transform: translateY(-1px);
        }
        
        /* Ads Table Styles */
        .ads-table {
            background: #2a2a3e;
            border-radius: 12px;
            overflow: hidden;
        }
        
        .table-header {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 15px;
            padding: 15px 20px;
            background: #3a3a5c;
            color: rgba(255,255,255,0.8);
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .table-row {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 15px;
            padding: 15px 20px;
            border-bottom: 1px solid #3a3a5c;
            align-items: center;
        }
        
        .table-row:last-child {
            border-bottom: none;
        }
        
        .channel-info {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .channel-icon {
            font-size: 24px;
            background: #3d5afe;
            padding: 8px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .channel-details {
            flex: 1;
        }
        
        .channel-name {
            color: white;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 2px;
        }
        
        .channel-type {
            color: rgba(255,255,255,0.6);
            font-size: 12px;
            margin-bottom: 2px;
        }
        
        .channel-title {
            color: rgba(255,255,255,0.8);
            font-size: 12px;
        }
        
        .col-price {
            color: #64B5F6;
            font-size: 14px;
            font-weight: 600;
        }
        
        .col-count {
            color: white;
            font-size: 14px;
            font-weight: 600;
        }
        
        .col-actions {
            display: flex;
            gap: 8px;
        }
        
        .edit-btn, .delete-btn {
            background: none;
            border: none;
            padding: 8px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .edit-btn {
            color: #64B5F6;
        }
        
        .edit-btn:hover {
            background: rgba(100, 181, 246, 0.1);
        }
        
        .delete-btn {
            color: #ff4757;
        }
        
        .delete-btn:hover {
            background: rgba(255, 71, 87, 0.1);
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
            background: #0F0F19;
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
            background: #0F0F19;
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
            padding: 20px;
        }
        
        .gift-card {
            background: #2a2a3e;
            border-radius: 8px;
            padding: 8px 12px;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 6px;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .gift-image {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 6px;
            background-size: cover;
            background-position: center;
            border: 1px solid #3a3a5c;
            flex-shrink: 0;
        }
        
        .gift-info {
            flex: 1;
            min-width: 0;
        }
        
        .gift-title {
            color: white;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 2px;
            text-transform: uppercase;
        }
        
        .gift-count {
            color: rgba(255,255,255,0.7);
            font-size: 12px;
        }
        
        .buy-channel-btn {
            background: #2196F3;
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
            background: #1976D2;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(33, 150, 243, 0.4);
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
            <div class="tab" onclick="switchTab('referral')">Реферали</div>
            <div class="tab" onclick="switchTab('profile')">Профіль</div>
        </div>
        
        <!-- Нижні кнопки категорій -->
        <div class="category-tabs">
            <div class="category-tab active" onclick="switchCategory('all')">Всі</div>
            <div class="category-tab" onclick="switchCategory('new')">Нові</div>
            <div class="category-tab" onclick="switchCategory('sorting')">Сортування</div>
            <div class="category-tab" onclick="switchCategory('extras')">Доп</div>
            <div class="clear-selection-btn" onclick="clearAllSelections()">✕</div>
        </div>
        
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
                
                <div class="gifts-modal-body">
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
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        // ПОВНА БАЗА ДАННЫХ з усіма 37 подарунками в правильному порядку та назвах
        const ALL_GIFTS = {
            37: {id: 37, name: "SNOOP DOGG", desc: "Legendary rapper", image: "https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"},
            36: {id: 36, name: "SWAG BAG", desc: "Stylish bag", image: "https://i.postimg.cc/d1cwkrNg/Gifts-Gifts-Gifts-Ag-AD5-XMAAmjze-Us.png"},
            35: {id: 35, name: "SNOOP CIGAR", desc: "Smoking cigar", image: "https://i.postimg.cc/FKMsy2zW/Gifts-Gifts-Gifts-Ag-ADi38-AAg-7c-Es.png"},
            34: {id: 34, name: "LOW RIDER", desc: "Cool car", image: "https://i.postimg.cc/7Y96Fsth/Gifts-Gifts-Gifts-Ag-ADNWw-AAg5ze-Es.png"},
            33: {id: 33, name: "WESTSIDE SIGN", desc: "West coast sign", image: "https://i.postimg.cc/GtkBTbjx/Gifts-Gifts-Gifts-Ag-ADV4-QAAiibe-Us.png"},
            32: {id: 32, name: "TORCH", desc: "Olympic torch", image: "https://i.postimg.cc/wv1LMKPw/Gifts-Gifts-Gifts-Ag-AD2-XQAAk-VPSEs.png"},
            31: {id: 31, name: "STATUE", desc: "Ancient statue", image: "https://i.postimg.cc/V6hvVdKR/Gifts-Gifts-Gifts-Ag-ADi-IYAAqf-LQEs.png"},
            30: {id: 30, name: "EAGLE", desc: "Majestic eagle", image: "https://i.postimg.cc/0QXK1ty7/Gifts-Gifts-Gifts-Ag-ADzn-IAAl-Gn-QEs.png"},
            29: {id: 29, name: "NIPPLE", desc: "Baby nipple", image: "https://i.postimg.cc/BQrDvwcg/Gifts-Gifts-Gifts-Ag-ADD3-IAAm-RNKUo.png"},
            28: {id: 28, name: "PLUMBER", desc: "Mario plumber", image: "https://i.postimg.cc/85pLSJBg/Gifts-Gifts-Gifts-Ag-ADKX4-AAuw-O2-Ek.png"},
            27: {id: 27, name: "ESKIMO", desc: "Cold eskimo", image: "https://i.postimg.cc/L4y3mTbC/Gifts-Gifts-Gifts-Ag-ADy-XEAAky04-Ek.png"},
            26: {id: 26, name: "CREAMY ICE CREAM", desc: "Creamy ice cream", image: "https://i.postimg.cc/ydjXgXYN/Gifts-Gifts-Gifts-Ag-AD0-Ww-AAs4-T4-Ek.png"},
            25: {id: 25, name: "STAR", desc: "Shining star", image: "https://i.postimg.cc/3Nr1nfbp/Gifts-Gifts-Gifts-Ag-ADbn-UAAl-XNEUk.png"},
            24: {id: 24, name: "PIGEON", desc: "City pigeon", image: "https://i.postimg.cc/QxJsBFcy/Gifts-Gifts-Gifts-Ag-ADa3-QAAtw-JEEk.png"},
            23: {id: 23, name: "MEDAL", desc: "Gold medal", image: "https://i.postimg.cc/N0zQgZRG/Gifts-Gifts-Gifts-Ag-ADO3c-AAqb-DEEk.png"},
            22: {id: 22, name: "1 MAY", desc: "Labor day", image: "https://i.postimg.cc/gJxk8GG6/Gifts-Gifts-Gifts-Ag-ADMm4-AAj-Ll6-Ug.png"},
            21: {id: 21, name: "RABBIT", desc: "Fluffy rabbit", image: "https://i.postimg.cc/WtLRDv4j/Gifts-Gifts-Gifts-Ag-ADh-HUAAg-O6-IUg.png"},
            20: {id: 20, name: "KULICH", desc: "Easter cake", image: "https://i.postimg.cc/tTJGwkf0/Gifts-Gifts-Gifts-Ag-ADBa-UAAk8-WKEg.png"},
            19: {id: 19, name: "ROCKET", desc: "Space rocket", image: "https://i.postimg.cc/nhfZrvs7/Gifts-Gifts-Gifts-Ag-ADIo-UAAk3-J2-Es.png"},
            18: {id: 18, name: "BRICK", desc: "Building brick", image: "https://i.postimg.cc/c1jdyq0F/Gifts-Gifts-Gifts-Ag-ADg2o-AAg-R5g-Us.png"},
            17: {id: 17, name: "MONKEY", desc: "Playful monkey", image: "https://i.postimg.cc/bN7Yn75Z/Gifts-Gifts-Gifts-Ag-AEZAACV66-BSw.png"},
            16: {id: 16, name: "POOP", desc: "Funny poop", image: "https://i.postimg.cc/05HykMdd/Gifts-Gifts-Gifts-Ag-AD82w-AAk-FZg-Es.png"},
            15: {id: 15, name: "DOSHIK", desc: "Instant noodles", image: "https://i.postimg.cc/k5F5qTfB/Gifts-Gifts-Gifts-Ag-AD4-GQAAq8-Xg-Us.png"},
            14: {id: 14, name: "MOSQUE", desc: "Beautiful mosque", image: "https://i.postimg.cc/pr1T3ykC/Gifts-Gifts-Gifts-Ag-ADV3-MAAnv-We-Us.png"},
            13: {id: 13, name: "AMULET", desc: "Protection amulet", image: "https://i.postimg.cc/hGFJSzn3/Gifts-Gifts-Gifts-Ag-AD-HEAAq-9c-Us.png"},
            12: {id: 12, name: "CLOVER", desc: "Lucky clover", image: "https://i.postimg.cc/NfJmwjLW/Gifts-Gifts-Gifts-Ag-ADf-GYAAjfaw-Uo.png"},
            11: {id: 11, name: "BOILER", desc: "Hot boiler", image: "https://i.postimg.cc/Dfc1Bghf/Gifts-Gifts-Gifts-Ag-ADe-WMAAp-Rw-IUs.png"},
            10: {id: 10, name: "DYSON", desc: "Powerful vacuum", image: "https://i.postimg.cc/3NZjGj8R/Gifts-Gifts-Gifts-Ag-ADhmw-AAl1-Zc-Uo.png"},
            9: {id: 9, name: "MARCH 8", desc: "Women's day", image: "https://i.postimg.cc/d1y4hTZk/Gifts-Gifts-Gifts-Ag-ADh2o-AAoa-Dc-Eo.png"},
            8: {id: 8, name: "CUPCAKE", desc: "Sweet cupcake", image: "https://i.postimg.cc/gkqtyRS3/Gifts-Gifts-Gifts-Ag-ADB3-AAAr-Pqc-Eo.png"},
            7: {id: 7, name: "BOUQUET", desc: "Beautiful bouquet", image: "https://i.postimg.cc/TY8BJTRv/Gifts-Gifts-Gifts-Ag-ADk3-AAAiy-WGEs.png"},
            6: {id: 6, name: "LAMP", desc: "Table lamp", image: "https://i.postimg.cc/hjfNpjzc/Gifts-Gifts-Gifts-Ag-ADj-Gw-AAkl0c-Eo.png"},
            5: {id: 5, name: "BICEPS", desc: "Strong muscles", image: "https://i.postimg.cc/K4Xf7cLq/Gifts-Gifts-Gifts-Ag-ADB3-UAAp5-V0-Uk.png"},
            4: {id: 4, name: "SOCKS", desc: "Warm socks", image: "https://i.postimg.cc/bwxCTnmQ/Gifts-Gifts-Gifts-Ag-ADKmk-AAt0-L2-Ek.png"},
            3: {id: 3, name: "CATS", desc: "Cute cats", image: "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"},
            2: {id: 2, name: "BUTTON", desc: "Simple button", image: "https://i.postimg.cc/XqDSnCRZ/Gifts-Gifts-Gifts-Ag-ADWWg-AAhwgi-Uk.png"},
            1: {id: 1, name: "HEELS", desc: "High heels", image: "https://i.postimg.cc/jdsL20Gt/Gifts-Gifts-Gifts-Ag-ADBmg-AAnz-Oe-Ek.png"}
        };
        
        // База данных каналов з оновленими подарунками
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
                    {id: 1, name: "HEELS", desc: "High heels", count: "11500", image: "https://i.postimg.cc/jdsL20Gt/Gifts-Gifts-Gifts-Ag-ADBmg-AAnz-Oe-Ek.png"},
                    {id: 4, name: "SOCKS", desc: "Warm socks", count: "2834", image: "https://i.postimg.cc/bwxCTnmQ/Gifts-Gifts-Gifts-Ag-ADKmk-AAt0-L2-Ek.png"},
                    {id: 36, name: "SWAG BAG", desc: "Stylish bag", count: "34", image: "https://i.postimg.cc/d1cwkrNg/Gifts-Gifts-Gifts-Ag-AD5-XMAAmjze-Us.png"},
                    {id: 2, name: "BUTTON", desc: "Simple button", count: "356", image: "https://i.postimg.cc/XqDSnCRZ/Gifts-Gifts-Gifts-Ag-ADWWg-AAhwgi-Uk.png"},
                    {id: 23, name: "STAR", desc: "Shining star", count: "1240", image: "https://i.postimg.cc/N0zQgZRG/Gifts-Gifts-Gifts-Ag-ADO3c-AAqb-DEEk.png"},
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
                    {id: 3, name: "CATS", desc: "Cute cats", count: "2945", image: "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"},
                    {id: 17, name: "MONKEY", desc: "Playful monkey", count: "1401", image: "https://i.postimg.cc/bN7Yn75Z/Gifts-Gifts-Gifts-Ag-AEZAACV66-BSw.png"},
                    {id: 21, name: "RABBIT", desc: "Fluffy rabbit", count: "967", image: "https://i.postimg.cc/WtLRDv4j/Gifts-Gifts-Gifts-Ag-ADh-HUAAg-O6-IUg.png"},
                    {id: 1, name: "HEELS", desc: "High heels", count: "250", image: "https://i.postimg.cc/jdsL20Gt/Gifts-Gifts-Gifts-Ag-ADBmg-AAnz-Oe-Ek.png"},
                    {id: 14, name: "PIGEON", desc: "City pigeon", count: "723", image: "https://i.postimg.cc/pr1T3ykC/Gifts-Gifts-Gifts-Ag-ADV3-MAAnv-We-Us.png"},
                    {id: 12, name: "EAGLE", desc: "Majestic eagle", count: "567", image: "https://i.postimg.cc/NfJmwjLW/Gifts-Gifts-Gifts-Ag-ADf-GYAAjfaw-Uo.png"}
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
                    {id: 6, name: "LAMP", desc: "Table lamp", count: "2612", image: "https://i.postimg.cc/hjfNpjzc/Gifts-Gifts-Gifts-Ag-ADj-Gw-AAkl0c-Eo.png"},
                    {id: 10, name: "DYSON", desc: "Powerful vacuum", count: "2178", image: "https://i.postimg.cc/3NZjGj8R/Gifts-Gifts-Gifts-Ag-ADhmw-AAl1-Zc-Uo.png"},
                    {id: 19, name: "ROCKET", desc: "Space rocket", count: "1189", image: "https://i.postimg.cc/nhfZrvs7/Gifts-Gifts-Gifts-Ag-ADIo-UAAk3-J2-Es.png"},
                    {id: 2, name: "BUTTON", desc: "Simple button", count: "890", image: "https://i.postimg.cc/XqDSnCRZ/Gifts-Gifts-Gifts-Ag-ADWWg-AAhwgi-Uk.png"},
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
                    {id: 8, name: "CUPCAKE", desc: "Sweet cupcake", count: "2390", image: "https://i.postimg.cc/gkqtyRS3/Gifts-Gifts-Gifts-Ag-ADB3-AAAr-Pqc-Eo.png"},
                    {id: 15, name: "DOSHIK", desc: "Instant noodles", count: "1623", image: "https://i.postimg.cc/k5F5qTfB/Gifts-Gifts-Gifts-Ag-AD4-GQAAq8-Xg-Us.png"},
                    {id: 26, name: "CREAMY ICE CREAM", desc: "Creamy ice cream", count: "423", image: "https://i.postimg.cc/ydjXgXYN/Gifts-Gifts-Gifts-Ag-AD0-Ww-AAs4-T4-Ek.png"},
                    {id: 3, name: "CATS", desc: "Cute cats", count: "150", image: "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"},
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
                    {id: 37, name: "SNOOP DOGG", desc: "Legendary rapper", count: "15", image: "https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"},
                    {id: 33, name: "WESTSIDE SIGN", desc: "West coast sign", count: "67", image: "https://i.postimg.cc/GtkBTbjx/Gifts-Gifts-Gifts-Ag-ADV4-QAAiibe-Us.png"},
                    {id: 34, name: "LOW RIDER", desc: "Cool car", count: "23", image: "https://i.postimg.cc/7Y96Fsth/Gifts-Gifts-Gifts-Ag-ADNWw-AAg5ze-Es.png"},
                    {id: 36, name: "SWAG BAG", desc: "Stylish bag", count: "89", image: "https://i.postimg.cc/d1cwkrNg/Gifts-Gifts-Gifts-Ag-AD5-XMAAmjze-Us.png"},
                    {id: 35, name: "SNOOP CIGAR", desc: "Smoking cigar", count: "345", image: "https://i.postimg.cc/FKMsy2zW/Gifts-Gifts-Gifts-Ag-ADi38-AAg-7c-Es.png"},
                    {id: 32, name: "TORCH", desc: "Olympic torch", count: "178", image: "https://i.postimg.cc/wv1LMKPw/Gifts-Gifts-Gifts-Ag-AD2-XQAAk-VPSEs.png"}
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
                    {id: 2, name: "BUTTON", desc: "Simple button", count: "5600", image: "https://i.postimg.cc/XqDSnCRZ/Gifts-Gifts-Gifts-Ag-ADWWg-AAhwgi-Uk.png"},
                    {id: 6, name: "LAMP", desc: "Table lamp", count: "234", image: "https://i.postimg.cc/hjfNpjzc/Gifts-Gifts-Gifts-Ag-ADj-Gw-AAkl0c-Eo.png"},
                    {id: 5, name: "BICEPS", desc: "Strong muscles", count: "567", image: "https://i.postimg.cc/K4Xf7cLq/Gifts-Gifts-Gifts-Ag-ADB3-UAAp5-V0-Uk.png"},
                    {id: 16, name: "1 MAY", desc: "Labor day", count: "89", image: "https://i.postimg.cc/05HykMdd/Gifts-Gifts-Gifts-Ag-AD82w-AAk-FZg-Es.png"},
                    {id: 28, name: "CLOVER", desc: "Lucky clover", count: "234", image: "https://i.postimg.cc/85pLSJBg/Gifts-Gifts-Gifts-Ag-ADKX4-AAuw-O2-Ek.png"},
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
                    {id: 16, name: "1 MAY", desc: "Labor day", count: "1234", image: "https://i.postimg.cc/05HykMdd/Gifts-Gifts-Gifts-Ag-AD82w-AAk-FZg-Es.png"},
                    {id: 29, name: "MARCH 8", desc: "Women's day", count: "456", image: "https://i.postimg.cc/BQrDvwcg/Gifts-Gifts-Gifts-Ag-ADD3-IAAm-RNKUo.png"},
                    {id: 5, name: "BICEPS", desc: "Strong muscles", count: "789", image: "https://i.postimg.cc/K4Xf7cLq/Gifts-Gifts-Gifts-Ag-ADB3-UAAp5-V0-Uk.png"},
                    {id: 7, name: "PLUMBER", desc: "Mario plumber", count: "123", image: "https://i.postimg.cc/TY8BJTRv/Gifts-Gifts-Gifts-Ag-ADk3-AAAiy-WGEs.png"},
                    {id: 13, name: "STATUE", desc: "Ancient statue", count: "345", image: "https://i.postimg.cc/hGFJSzn3/Gifts-Gifts-Gifts-Ag-AD-HEAAq-9c-Us.png"},
                    {id: 32, name: "TORCH", desc: "Olympic torch", count: "678", image: "https://i.postimg.cc/wv1LMKPw/Gifts-Gifts-Gifts-Ag-AD2-XQAAk-VPSEs.png"}
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
                    {id: 30, name: "BOILER", desc: "Hot boiler", count: "789", image: "https://i.postimg.cc/0QXK1ty7/Gifts-Gifts-Gifts-Ag-ADzn-IAAl-Gn-QEs.png"},
                    {id: 27, name: "STATUE", desc: "Ancient statue", count: "345", image: "https://i.postimg.cc/L4y3mTbC/Gifts-Gifts-Gifts-Ag-ADy-XEAAky04-Ek.png"},
                    {id: 23, name: "STAR", desc: "Shining star", count: "567", image: "https://i.postimg.cc/N0zQgZRG/Gifts-Gifts-Gifts-Ag-ADO3c-AAqb-DEEk.png"}
                ]
            }
        ];
        
        let currentView = 'market';
        let currentCategory = 'all';
        let currentExtrasCategory = 'all'; // Для вкладки "Доп"
        let currentChannelModal = null;
        let selectedGiftFilter = null;
        let selectedGifts = new Set();
        let currentSorting = 'all';
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
        
        function renderGiftsFilterList(gifts) {
            const grid = document.getElementById('giftsGrid');
            
            grid.innerHTML = gifts.map(gift => `
                <div class="gift-filter-item" onclick="selectGiftForFilter(${gift.id})">
                    <div class="gift-filter-checkbox ${selectedGifts.has(gift.id) ? 'checked' : ''}" onclick="event.stopPropagation(); toggleGiftSelection(${gift.id})"></div>
                    <div class="gift-filter-image" style="background-image: url('${gift.image}')"></div>
                    <div class="gift-filter-info">
                        <div class="gift-filter-name">${gift.name}</div>
                        <div class="gift-filter-count">${gift.totalCount} шт</div>
                    </div>
                    <div class="gift-filter-price">${(Math.random() * 50 + 5).toFixed(1)} TON</div>
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
        
        function selectGiftForFilter(giftId) {
            selectedGiftFilter = giftId;
            showChannelsWithGift(giftId);
        }
        
        function applyGiftFilter() {
            let channelsToShow = [...channelListings];
            
            if (selectedGifts.size > 0) {
                channelsToShow = channelsToShow.filter(channel => {
                    return channel.gifts.some(gift => selectedGifts.has(gift.id));
                });
            }
            
            if (currentSorting === 'expensive') {
                channelsToShow.sort((a, b) => b.price - a.price);
            } else if (currentSorting === 'cheap') {
                channelsToShow.sort((a, b) => a.price - b.price);
            }
            
            renderChannelListings(channelsToShow);
        }
        
        function showAllGiftsFilter() {
            document.getElementById('giftsGrid').className = 'gifts-filter-grid';
            
            const allGifts = new Map();
            
            // Створюємо мапу всіх подарунків
            Object.values(ALL_GIFTS).forEach(giftTemplate => {
                allGifts.set(giftTemplate.id, {
                    ...giftTemplate,
                    totalCount: 0,
                    channels: []
                });
            });
            
            // Додаємо дані з каналів
            channelListings.forEach(channel => {
                channel.gifts.forEach(gift => {
                    if (allGifts.has(gift.id)) {
                        const existing = allGifts.get(gift.id);
                        existing.totalCount += parseInt(gift.count);
                        if (!existing.channels.includes(channel.id)) {
                            existing.channels.push(channel.id);
                        }
                    }
                });
            });
            
            // Конвертуємо в масив і сортуємо за ID від 37 до 1
            const giftsArray = Array.from(allGifts.values()).sort((a, b) => b.id - a.id);
            
            renderGiftsFilterList(giftsArray);
        }
        
        function showChannelsWithGift(giftId) {
            const channelsWithGift = channelListings.filter(channel => 
                channel.gifts.some(gift => gift.id === giftId)
            );
            
            channelsWithGift.sort((a, b) => {
                const aGift = a.gifts.find(gift => gift.id === giftId);
                const bGift = b.gifts.find(gift => gift.id === giftId);
                return parseInt(bGift.count) - parseInt(aGift.count);
            });
            
            renderChannelListings(channelsWithGift);
        }
        
        function showExtrasOptions() {
            document.getElementById('giftsGrid').className = 'gifts-filter-grid';
            
            const grid = document.getElementById('giftsGrid');
            grid.innerHTML = `
                <div class="gift-filter-item" onclick="applyExtrasFilter('all')">
                    <div class="gift-filter-checkbox ${currentExtrasCategory === 'all' ? 'checked' : ''}"></div>
                    <div class="gift-filter-image" style="background: linear-gradient(45deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; font-size: 20px;">🎁</div>
                    <div class="gift-filter-info">
                        <div class="gift-filter-name">Всі</div>
                        <div class="gift-filter-stats">
                            <span class="gift-filter-count">Всі канали з подарунками</span>
                        </div>
                    </div>
                </div>
                
                <div class="gift-filter-item" onclick="applyExtrasFilter('with-extras')">
                    <div class="gift-filter-checkbox ${currentExtrasCategory === 'with-extras' ? 'checked' : ''}"></div>
                    <div class="gift-filter-image" style="background: linear-gradient(45deg, #4ecdc4, #44a08d); display: flex; align-items: center; justify-content: center; font-size: 20px;">🎈</div>
                    <div class="gift-filter-info">
                        <div class="gift-filter-name">З доп подарунками</div>
                        <div class="gift-filter-stats">
                            <span class="gift-filter-count">Канали з різними подарунками</span>
                        </div>
                    </div>
                </div>
                
                <div class="gift-filter-item" onclick="applyExtrasFilter('without-extras')">
                    <div class="gift-filter-checkbox ${currentExtrasCategory === 'without-extras' ? 'checked' : ''}"></div>
                    <div class="gift-filter-image" style="background: linear-gradient(45deg, #ff6b6b, #ff8e8e); display: flex; align-items: center; justify-content: center; font-size: 20px;">📦</div>
                    <div class="gift-filter-info">
                        <div class="gift-filter-name">Без доп подарунків</div>
                        <div class="gift-filter-stats">
                            <span class="gift-filter-count">Канали тільки одного виду</span>
                        </div>
                    </div>
                </div>
            `;
        }
        
        function applyExtrasFilter(extrasType) {
            currentExtrasCategory = extrasType;
            updateClearButton();
            
            let channelsToShow = [...channelListings];
            
            if (extrasType === 'with-extras') {
                // Показуємо канали з різними подарунками (більше 3 різних типів)
                channelsToShow = channelsToShow.filter(channel => {
                    const uniqueGifts = new Set(channel.gifts.map(gift => gift.id));
                    return uniqueGifts.size > 3;
                });
            } else if (extrasType === 'without-extras') {
                // Показуємо канали з одним типом подарунків (1-2 різних типи)
                channelsToShow = channelsToShow.filter(channel => {
                    const uniqueGifts = new Set(channel.gifts.map(gift => gift.id));
                    return uniqueGifts.size <= 2;
                });
            }
            
            // Відображаємо результат
            if (extrasType === 'all') {
                showExtrasOptions();
            } else {
                renderChannelListings(channelsToShow);
            }
        }
        
        function clearAllSelections() {
            selectedGifts.clear();
            currentSorting = 'all';
            currentExtrasCategory = 'all';
            
            updateClearButton();
            
            if (currentCategory === 'new') {
                showAllGiftsFilter();
            } else if (currentCategory === 'all') {
                applyGiftFilter();
            } else if (currentCategory === 'sorting') {
                showSortingOptions();
            } else if (currentCategory === 'extras') {
                showExtrasOptions();
            }
        }
        
        function renderChannelListings(channelsToRender) {
            const grid = document.getElementById('giftsGrid');
            grid.className = 'gifts-grid';
            
            if (channelsToRender.length === 0) {
                grid.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 18px; margin-bottom: 10px;">Каналы не найдены</div>
                        <div style="font-size: 14px;">Попробуйте изменить фильтры</div>
                    </div>
                `;
                return;
            }
            
            grid.innerHTML = channelsToRender.map(channel => {
                const mainGift = channel.gifts[0];
                // Беремо правильні дані з бази ALL_GIFTS за ID
                const correctGift = ALL_GIFTS[mainGift.id];
                
                // Генеруємо демо @ назву для відображення
                let displayChannelName = '';
                switch(channel.id) {
                    case 1: displayChannelName = '@fashion_style'; break;
                    case 2: displayChannelName = '@cat_lovers'; break;
                    case 3: displayChannelName = '@tech_store'; break;
                    case 4: displayChannelName = '@sweet_treats'; break;
                    case 5: displayChannelName = '@hiphop_central'; break;
                    case 6: displayChannelName = '@button_collectors'; break;
                    case 7: displayChannelName = '@sports_arena'; break;
                    case 8: displayChannelName = '@cultural_gifts'; break;
                    default: displayChannelName = channel.name;
                }
                
                return `
                    <div class="gift-card-main" onclick="openGiftsModal(${channel.id})">
                        <div class="gift-image-main" style="background-image: url('${correctGift.image}')"></div>
                        <div class="gift-name-main">${correctGift.name}</div>
                        <div class="gift-channel-name">${displayChannelName}</div>
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
            selectedGiftFilter = null;
            
            // Відновлюємо поточну категорію без зміни стану
            if (currentCategory === 'all') {
                document.getElementById('giftsGrid').className = 'gifts-grid';
                applyGiftFilter();
            } else if (currentCategory === 'new') {
                document.getElementById('giftsGrid').className = 'gifts-filter-grid';
                showAllGiftsFilter();
            } else if (currentCategory === 'sorting') {
                document.getElementById('giftsGrid').className = 'gifts-filter-grid';
                showSortingOptions();
            } else if (currentCategory === 'extras') {
                document.getElementById('giftsGrid').className = 'gifts-filter-grid';
                showExtrasOptions();
            }
        }
        
        function showMyChannels() {
            document.querySelector('.category-tabs').classList.add('hidden');
            const grid = document.getElementById('giftsGrid');
            grid.className = 'gifts-grid my-channel-grid';
            
            // Перевіряємо чи є створені канали (поки що завжди пусто для демо)
            const hasChannels = false; // В майбутньому тут буде перевірка реальних даних
            
            if (!hasChannels) {
                // Показуємо пустий стан
                grid.innerHTML = `
                    <div class="my-ads-container">
                        <div class="my-ads-header">
                            <div class="my-ads-title">Мои объявления</div>
                            <button class="add-ad-btn" onclick="showCreateAdForm()">+</button>
                        </div>
                        
                        <div class="empty-ads-state">
                            <div class="empty-ads-icon">
                                <img src="https://i.postimg.cc/ncnSj3rD/1752485903244.png" alt="Gift" style="width: 120px; height: 120px; object-fit: contain; background: transparent;">
                            </div>
                            <div class="empty-ads-title">Нет объявлений</div>
                            <div class="empty-ads-subtitle">Создайте ваше первое объявление</div>
                            <button class="create-ad-btn" onclick="showCreateAdForm()">Добавить объявление</button>
                        </div>
                    </div>
                `;
            } else {
                // Показуємо список каналів
                showMyChannelsList();
            }
        }
        
        function showReferral() {
            document.querySelector('.category-tabs').classList.add('hidden');
            const grid = document.getElementById('giftsGrid');
            grid.className = 'gifts-grid';
            
            // Получаем ID пользователя из Telegram WebApp
            const user = tg.initDataUnsafe?.user;
            let userId = user?.id || '123456789';
            let referralLink = `https://t.me/giftroom_market_bot?start=${userId}`;
            
            grid.innerHTML = `
                <div class="referral-container">
                    <div class="referral-header">
                        <div class="referral-title">Реферальна система</div>
                        <div class="referral-subtitle">Приглашай друзей и получай комиссию от их покупок</div>
                        <div class="referral-commission">2.5% комиссии</div>
                    </div>
                    
                    <div class="referral-link-section">
                        <div class="referral-link-title">Твоя реферальна ссылка</div>
                        <div class="referral-link-container">
                            <input 
                                type="text" 
                                class="referral-link-input" 
                                value="${referralLink}"
                                readonly
                                id="referralLink"
                            >
                            <button class="copy-btn" onclick="copyReferralLink()">Копія</button>
                        </div>
                    </div>
                    
                    <div class="referral-stats">
                        <div class="referral-stat">
                            <div class="referral-stat-value">
                                12
                                <span style="font-size: 18px;">👥</span>
                            </div>
                            <div class="referral-stat-label">Рефералів</div>
                        </div>
                        <div class="referral-stat">
                            <div class="referral-stat-value">
                                34.8 
                                <div style="width: 16px; height: 16px; background-image: url('https://i.postimg.cc/kX2nWB4M/121-20250711185549.png'); background-size: cover; background-position: center; border-radius: 50%;"></div>
                            </div>
                            <div class="referral-stat-label">Заробили</div>
                        </div>
                    </div>
                    
                    <div class="referral-balance">
                        <div class="referral-balance-title">Реферальний баланс</div>
                        <div class="referral-balance-value">
                            15.2 
                            <div style="width: 20px; height: 20px; background-image: url('https://i.postimg.cc/kX2nWB4M/121-20250711185549.png'); background-size: cover; background-position: center; border-radius: 50%;"></div>
                        </div>
                        <div class="referral-actions">
                            <button class="referral-action-btn primary" onclick="withdrawToMarket()">На маркет</button>
                            <button class="referral-action-btn" onclick="withdrawToWallet()">На гаманець</button>
                        </div>
                    </div>
                </div>
            `;
        }
            document.querySelector('.category-tabs').classList.add('hidden');
            const grid = document.getElementById('giftsGrid');
            grid.className = 'gifts-grid profile-grid';
            
            // Получаем данные пользователя из Telegram WebApp
            const user = tg.initDataUnsafe?.user;
            let username = user?.username || user?.first_name || 'xr00y';
            
            // Создаем аватар как в концепте
            let avatarContent = '';
            let avatarStyle = `
                background: linear-gradient(135deg, #ff1744 0%, #8b0000 100%);
                color: white;
                font-size: 48px;
                font-weight: 700;
                display: flex;
                align-items: center;
                justify-content: center;
            `;
            
            // Если есть фото пользователя, используем его
            if (user?.photo_url) {
                avatarContent = '';
                avatarStyle = `background-image: url('${user.photo_url}'); background-size: cover; background-position: center;`;
            } else {
                // Иконка как в концепте 
                avatarContent = 'LR';
            }
            
            grid.innerHTML = `
                <div style="text-align: center; width: 100%; max-width: 300px;">
                    <div style="width: 100px; height: 100px; border-radius: 12px; ${avatarStyle} margin: 0 auto 12px; box-shadow: 0 10px 25px rgba(255, 23, 68, 0.4); border: 2px solid rgba(255,255,255,0.15);">${avatarContent}</div>
                    <div style="font-size: 26px; font-weight: 700; color: white; margin-bottom: 25px; line-height: 1.1;">${username}</div>
                    
                    <div style="display: flex; justify-content: space-around; gap: 30px; width: 100%; max-width: 350px;">
                        <div style="text-align: center; flex: 1;">
                            <div style="font-size: 22px; font-weight: 700; color: white; margin-bottom: 6px; display: flex; align-items: center; justify-content: center; gap: 6px;">
                                207.5 
                                <div style="width: 16px; height: 16px; background-image: url('https://i.postimg.cc/kX2nWB4M/121-20250711185549.png'); background-size: cover; background-position: center; border-radius: 50%;"></div>
                            </div>
                            <div style="font-size: 9px; color: rgba(255,255,255,0.7); text-transform: uppercase; font-weight: 600;">TOTAL VOLUME</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div style="font-size: 22px; font-weight: 700; color: white; margin-bottom: 6px; display: flex; align-items: center; justify-content: center; gap: 6px;">
                                0 
                                <span style="font-size: 16px;">🎁</span>
                            </div>
                            <div style="font-size: 9px; color: rgba(255,255,255,0.7); text-transform: uppercase; font-weight: 600;">BOUGHT</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div style="font-size: 22px; font-weight: 700; color: white; margin-bottom: 6px; display: flex; align-items: center; justify-content: center; gap: 6px;">
                                8 
                                <span style="font-size: 16px;">🎁</span>
                            </div>
                            <div style="font-size: 9px; color: rgba(255,255,255,0.7); text-transform: uppercase; font-weight: 600;">SOLD</div>
                        </div>
                    </div>
                </div>
            `;
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
            showSortingOptions();
        }
        
        function updateClearButton() {
            // Хрестик тепер завжди видимий
            const clearBtn = document.querySelector('.clear-selection-btn');
            clearBtn.style.display = 'flex';
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
            } else if (category === 'extras') {
                document.querySelectorAll('.category-tab')[3].classList.add('active');
                if (currentView === 'market') {
                    showExtrasOptions();
                }
            }
            
            updateClearButton();
        }
        
        function showCreateAdForm() {
            const grid = document.getElementById('giftsGrid');
            grid.innerHTML = `
                <div class="create-ad-container">
                    <div class="create-ad-header">
                        <button class="back-btn" onclick="showMyChannels()">←</button>
                        <div class="create-ad-title">Новое объявление</div>
                        <div style="width: 32px;"></div>
                    </div>
                    
                    <div class="create-ad-form">
                        <div class="form-group">
                            <label class="form-label">Ссылка на канал *</label>
                            <input 
                                type="text" 
                                class="form-input" 
                                placeholder="@channel_name или https://t.me/channel"
                                id="channelLink"
                            >
                            <div class="form-help">Введите ссылку на канал, который продаете</div>
                        </div>
                        
                        <div class="important-info">
                            <div class="info-icon">⚠️</div>
                            <div class="info-content">
                                <div class="info-title">Важная информация для продажи канала</div>
                                <div class="info-text">Перед добавлением канала на маркет, сначала добавьте в него бота @Giftroom_market_bot и назначьте его администратором.</div>
                                <div class="info-requirements">
                                    <div class="req-title">Внимание:</div>
                                    <div class="req-item">— канал должен быть публичным</div>
                                    <div class="req-item">— подарки в нём должны быть видимыми (не скрытыми)</div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Цена (TON) *</label>
                            <input 
                                type="number" 
                                class="form-input" 
                                placeholder="0.00"
                                id="channelPrice"
                                step="0.01"
                                min="0"
                            >
                        </div>
                        
                        <button class="create-btn" onclick="createChannelAd()">СОЗДАТЬ</button>
                    </div>
                </div>
            `;
        }
        
        function showMyChannelsList() {
            const grid = document.getElementById('giftsGrid');
            grid.innerHTML = `
                <div class="my-ads-container">
                    <div class="my-ads-header">
                        <div class="my-ads-title">Мои объявления</div>
                        <button class="add-ad-btn" onclick="showCreateAdForm()">+</button>
                    </div>
                    
                    <div class="ads-table">
                        <div class="table-header">
                            <div class="col-model">МОДЕЛЬ</div>
                            <div class="col-price">ЦЕНА</div>
                            <div class="col-count">КОЛ-ВО</div>
                            <div class="col-actions">ДЕЙСТВИЯ</div>
                        </div>
                        
                        <div class="table-row">
                            <div class="col-model">
                                <div class="channel-info">
                                    <div class="channel-icon">🔥</div>
                                    <div class="channel-details">
                                        <div class="channel-name">35 факел...</div>
                                        <div class="channel-type">Канал</div>
                                        <div class="channel-title">🔥 Torch of freedom</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-price">💎 64,8 TON</div>
                            <div class="col-count">38</div>
                            <div class="col-actions">
                                <button class="edit-btn" onclick="editChannel()">✏️</button>
                                <button class="delete-btn" onclick="deleteChannel()">🗑️</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        function createChannelAd() {
            const channelLink = document.getElementById('channelLink').value;
            const channelPrice = document.getElementById('channelPrice').value;
            
            if (!channelLink || !channelPrice) {
                tg.showAlert('Заполните все обязательные поля');
                return;
            }
            
            // Симулюємо створення каналу
            tg.showAlert(`Канал ${channelLink} создан за ${channelPrice} TON!`);
            
            // Переходимо до списку каналів
            showMyChannelsList();
        }
        
        function editChannel() {
            tg.showAlert('Редактирование канала');
        }
        
        function deleteChannel() {
            tg.showAlert('Удаление канала');
        }
        
        function openGiftsModal(channelId) {
            const channel = channelListings.find(c => c.id === channelId);
            if (!channel) return;
            
            currentChannelModal = channel;
            
            // Генеруємо @ назву для демо на основі ID
            let demoChannelName = '';
            switch(channelId) {
                case 1: demoChannelName = '@fashion_style'; break;
                case 2: demoChannelName = '@cat_lovers'; break;
                case 3: demoChannelName = '@tech_store'; break;
                case 4: demoChannelName = '@sweet_treats'; break;
                case 5: demoChannelName = '@hiphop_central'; break;
                case 6: demoChannelName = '@button_collectors'; break;
                case 7: demoChannelName = '@sports_arena'; break;
                case 8: demoChannelName = '@cultural_gifts'; break;
                default: demoChannelName = channel.name;
            }
            
            document.getElementById('modalChannelName').innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
                    <div style="font-size: 18px; font-weight: 600;">Подарки канала</div>
                    <div style="font-size: 16px; color: #64B5F6;">${demoChannelName}</div>
                </div>
            `;
            
            document.getElementById('buyChannelBtn').innerHTML = `
                <div class="ton-icon"></div>
                <span>Купить канал за ${channel.price} TON</span>
            `;
            
            const giftsGrid = document.getElementById('giftsModalGrid');
            
            giftsGrid.innerHTML = channel.gifts.map(gift => {
                const correctGift = ALL_GIFTS[gift.id];
                return `
                    <div class="gift-card">
                        <div class="gift-image" style="background-image: url('${correctGift.image}')"></div>
                        <div class="gift-info">
                            <div class="gift-title">${correctGift.name}</div>
                            <div class="gift-count">${gift.count} шт</div>
                        </div>
                    </div>
                `;
            }).join('');
            
            // Блокуємо скрол на основній сторінці без зміни позиції
            document.body.style.overflow = 'hidden';
            document.body.style.position = 'fixed';
            document.body.style.width = '100%';
            document.body.style.top = '0';
            document.body.style.left = '0';
            
            // Показуємо модальне вікно з анімацією
            const modal = document.getElementById('giftsModal');
            modal.classList.add('show');
            
            // Скролимо модальне вікно на початок
            setTimeout(() => {
                const modalGrid = document.getElementById('giftsModalGrid');
                if (modalGrid) {
                    modalGrid.scrollTop = 0;
                }
            }, 100);
        }
        
        function closeGiftsModal() {
            const modal = document.getElementById('giftsModal');
            modal.style.animation = 'modalSlideOut 0.3s ease-in forwards';
            
            setTimeout(() => {
                modal.classList.remove('show');
                modal.style.animation = '';
                currentChannelModal = null;
                
                // Відновлюємо скрол основної сторінки
                document.body.style.overflow = '';
                document.body.style.position = '';
                document.body.style.width = '';
                document.body.style.top = '';
                document.body.style.left = '';
            }, 300);
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
            } else if (tab === 'referral') {
                document.querySelectorAll('.tab')[2].classList.add('active');
                showReferral();
            } else if (tab === 'profile') {
                document.querySelectorAll('.tab')[3].classList.add('active');
                showProfile();
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
        
        function copyReferralLink() {
            const linkInput = document.getElementById('referralLink');
            linkInput.select();
            linkInput.setSelectionRange(0, 99999);
            
            try {
                document.execCommand('copy');
                tg.showAlert('Реферальная ссылка скопирована!');
            } catch (err) {
                console.error('Ошибка копирования:', err);
                tg.showAlert('Ошибка копирования ссылки');
            }
        }
        
        function withdrawToMarket() {
            tg.showAlert('Средства переведены на баланс маркета!');
        }
        
        function withdrawToWallet() {
            tg.showAlert('Вывод средств на TON кошелек...');
        }
        
        // Start loading when page loads
        window.addEventListener('load', startLoading);
        
        // Убираем главную кнопку Telegram
        tg.MainButton.hide();
        
        // Адаптация к теме
        if (tg.colorScheme === 'dark') {
            document.body.style.background = '#0F0F19';
        }
    </script>
</body>
</html>
    """

async def run_bot():
    await dp.start_polling(bot)

def start_bot():
    asyncio.run(run_bot())

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("🎁 GiftRoom Market з правильним порядком подарунків запущен!")
    print(f"🌐 URL: {WEBAPP_URL}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
