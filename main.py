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
        
        /* Profile Page Styles */
        .profile-container {
            background: #0F0F19;
            padding: 20px;
            min-height: calc(100vh - 140px);
        }
        
        .profile-header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #2a2a3e;
        }
        
        .profile-title {
            color: white;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .profile-subtitle {
            color: rgba(255,255,255,0.6);
            font-size: 14px;
        }
        
        .balance-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
        }
        
        .balance-label {
            color: rgba(255,255,255,0.8);
            font-size: 14px;
            margin-bottom: 8px;
        }
        
        .balance-amount {
            color: white;
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .balance-amount .ton-icon {
            width: 32px;
            height: 32px;
        }
        
        .balance-actions {
            display: flex;
            gap: 15px;
            justify-content: center;
        }
        
        .balance-action-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .balance-action-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .stat-card {
            background: #2a2a3e;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .stat-card:hover {
            border-color: #3d5afe;
            transform: translateY(-2px);
        }
        
        .stat-icon {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .stat-value {
            color: #64B5F6;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: rgba(255,255,255,0.7);
            font-size: 12px;
        }
        
        .settings-section {
            margin-bottom: 25px;
        }
        
        .settings-title {
            color: white;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            padding-left: 5px;
        }
        
        .settings-item {
            background: #2a2a3e;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .settings-item:hover {
            background: #3a3a5c;
            border-color: #3d5afe;
        }
        
        .settings-item-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .settings-item-icon {
            font-size: 20px;
        }
        
        .settings-item-info {
            flex: 1;
        }
        
        .settings-item-title {
            color: white;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 2px;
        }
        
        .settings-item-desc {
            color: rgba(255,255,255,0.6);
            font-size: 14px;
        }
        
        .settings-item-value {
            color: #64B5F6;
            font-size: 14px;
            font-weight: 600;
        }
        
        .settings-item-arrow {
            color: rgba(255,255,255,0.4);
            font-size: 16px;
        }
        
        .referral-section {
            background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 8px 30px rgba(78, 205, 196, 0.3);
        }
        
        .referral-title {
            color: white;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .referral-subtitle {
            color: rgba(255,255,255,0.8);
            font-size: 14px;
            margin-bottom: 20px;
        }
        
        .referral-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .referral-stat {
            background: rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 15px;
            backdrop-filter: blur(10px);
        }
        
        .referral-stat-value {
            color: white;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        
        .referral-stat-label {
            color: rgba(255,255,255,0.8);
            font-size: 12px;
        }
        
        .referral-link-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .referral-link-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
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
            box-shadow: 0 8px 25px rgba(255,107,107,
