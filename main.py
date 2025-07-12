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
        
        .gifts-grid.my-channel-grid {
            display: block;
            margin: -20px -20px 0 -20px;
            padding: 0;
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
            gap: 6px;
            font-size: 12px;
        }
        
        .price-btn .ton-icon {
            width: 16px;
            height: 16px;
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
        
        .channels-list {
            position: relative;
            z-index: 2;
        }
        
        .channel-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 18px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid rgba(255,255,255,0.15);
            transition: all 0.3s ease;
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
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }
        
        .channel-card:hover::before {
            left: 100%;
        }
        
        .channel-card:hover {
            transform: translateY(-2px);
            background: rgba(255,255,255,0.2);
        }
        
        .channel-info {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .channel-avatar {
            width: 50px;
            height: 50px;
            background: linear-gradient(45deg, #ff9a9e, #fecfef);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        .channel-details h3 {
            color: white;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .channel-details p {
            color: rgba(255,255,255,0.7);
            font-size: 13px;
            margin: 0;
        }
        
        .channel-stats {
            display: flex;
            gap: 20px;
            margin-bottom: 15px;
        }
        
        .channel-stat {
            display: flex;
            align-items: center;
            gap: 5px;
            color: rgba(255,255,255,0.8);
            font-size: 13px;
        }
        
        .channel-actions {
            display: flex;
            gap: 10px;
        }
        
        .action-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .action-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: scale(1.05);
        }
        
        .action-btn.primary {
            background: linear-gradient(45deg, #667eea, #764ba2);
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
            gap: 8px;
        }
        
        .gift-detail-price .ton-icon {
            width: 20px;
            height: 20px;
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
        <div class="app-subtitle">Магазин Telegram каналов с подарками</div>
        
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
            <div class="subtitle">Магазин Telegram каналов с подарками</div>
            
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
                    <!-- Контент буде додано через JavaScript -->
                </button>
            </div>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();
        
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
                        
                        // Initialize main app after loading
                        initializeApp();
                    }, 50);
                }, 500);
            }, 4000);
        }
        
        // Initialize main app
        function initializeApp() {
            showMarket();
        }
        
        // База данных всех подарков с вариациями для тестирования групп
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
            {id: 37, name: "SNOOP DOGG", desc: "Legendary rapper", price: "208.354", count: "15", new: true, listed: true, category: "entertainment", rarity: 5, image: "https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"},
            
            // Додаткові варіації для тестування груп
            {id: 38, name: "SNOOP DOGG", desc: "Legendary rapper - variant 2", price: "180.25", count: "8", new: true, listed: true, category: "entertainment", rarity: 5, image: "https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"},
            {id: 39, name: "SNOOP DOGG", desc: "Legendary rapper - variant 3", price: "220.15", count: "5", new: true, listed: true, category: "entertainment", rarity: 5, image: "https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"},
            
            {id: 40, name: "SNOOP CIGAR", desc: "Elite cigar - variant 2", price: "145.20", count: "25", new: true, listed: true, category: "entertainment", rarity: 5, image: "https://i.postimg.cc/FKMsy2zW/Gifts-Gifts-Gifts-Ag-ADi38-AAg-7c-Es.png"},
            
            {id: 41, name: "CATS", desc: "Cute cats - variant 2", price: "3.45", count: "2500", new: false, listed: true, category: "animals", rarity: 1, image: "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"},
            {id: 42, name: "CATS", desc: "Cute cats - variant 3", price: "3.67", count: "2200", new: false, listed: true, category: "animals", rarity: 1, image: "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"},
            
            {id: 43, name: "HEELS", desc: "High heels - variant 2", price: "2.34", count: "10800", new: false, listed: true, category: "fashion", rarity: 1, image: "https://i.postimg.cc/jdsL20Gt/Gifts-Gifts-Gifts-Ag-ADBmg-AAnz-Oe-Ek.png"},
            
            {id: 44, name: "EAGLE", desc: "Symbol of freedom - variant 2", price: "58.90", count: "140", new: true, listed: true, category: "symbols", rarity: 5, image: "https://i.postimg.cc/0QXK1ty7/Gifts-Gifts-Gifts-Ag-ADzn-IAAl-Gn-QEs.png"},
            {id: 45, name: "EAGLE", desc: "Symbol of freedom - variant 3", price: "62.15", count: "120", new: true, listed: true, category: "symbols", rarity: 5, image: "https://i.postimg.cc/0QXK1ty7/Gifts-Gifts-Gifts-Ag-ADzn-IAAl-Gn-QEs.png"}
        ];
        
        let currentView = 'market';
        let selectedFilter = null;
        let tempSelectedGift = null;
        let currentFilters = {
            giftType: '',
            sort: 'recent'
        };
        
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
            
            if (giftTypeFilter) {
                filteredGifts = filteredGifts.filter(gift => gift.category === giftTypeFilter);
            }
            
            switch (sortFilter) {
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
            
            renderGroupedGifts(filteredGifts);
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
            }
        }
        
        // Показать только listed подарки в Market
        function showMarket() {
            const grid = document.getElementById('giftsGrid');
            grid.className = 'gifts-grid';
            document.getElementById('filtersSection').classList.remove('filters-hidden');
            applyMarketFilters();
        }
        
        // Показать My Channel с WOW дизайном
        function showMyChannel() {
            document.getElementById('filtersSection').classList.add('filters-hidden');
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
        
        function openGiftModal() {
            const modal = document.getElementById('giftModal');
            const optionsList = document.getElementById('giftOptionsList');
            
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
            
            tempSelectedGift = selectedFilter;
            modal.classList.add('show');
        }
        
        function closeGiftModal() {
            document.getElementById('giftModal').classList.remove('show');
            tempSelectedGift = null;
        }
        
        function selectModalOption(giftName, element) {
            document.querySelectorAll('.gift-option').forEach(opt => opt.classList.remove('selected'));
            element.classList.add('selected');
            tempSelectedGift = giftName === '' ? null : giftName;
        }
        
        function selectModalGift() {
            selectedFilter = tempSelectedGift;
            closeGiftModal();
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
        
        function applyGiftNameFilter() {
            if (!selectedFilter) {
                applyFilters();
                return;
            }
            
            let filteredGifts = allGifts.filter(gift => gift.listed && gift.name === selectedFilter);
            
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
        
        function showCatalog() {
            const grid = document.getElementById('giftsGrid');
            grid.className = 'gifts-grid';
            document.getElementById('filtersSection').classList.add('filters-hidden');
            
            if (selectedFilter) {
                const filteredGifts = allGifts.filter(gift => gift.name === selectedFilter);
                const sortedGifts = filteredGifts.sort((a, b) => b.id - a.id);
                renderCatalogGifts(sortedGifts);
            } else {
                const sortedGifts = [...allGifts].sort((a, b) => b.id - a.id);
                renderCatalogGifts(sortedGifts);
            }
        }
        
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
        
        function selectGift(id) {
            const gift = allGifts.find(g => g.id === id);
            tg.showAlert(`Выбран подарок #${id}: ${gift.name}`);
        }
        
        function groupGiftsByName(gifts) {
            const groups = {};
            gifts.forEach(gift => {
                if (!groups[gift.name]) {
                    groups[gift.name] = [];
                }
                groups[gift.name].push(gift);
            });
            return Object.values(groups);
        }
        
        function renderGroupedGifts(gifts) {
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
            
            const groupedGifts = groupGiftsByName(gifts);
            
            grid.innerHTML = groupedGifts.map(group => {
                const count = group.length;
                const firstGift = group[0];
                
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
                    <div class="gift-group-card" onclick="openGiftGroupDetail('${firstGift.name}')">
                        <div class="gift-group-count">${count}</div>
                        <div class="gift-group-images ${containerClass}">
                            ${imagesToShow.map(gift => `
                                <div class="gift-group-image ${imageClass}" style="background-image: url('${gift.image}')"></div>
                            `).join('')}
                        </div>
                        <div class="gift-group-title">${firstGift.name}</div>
                        <button class="price-btn" onclick="event.stopPropagation(); showGiftGroupPrices('${firstGift.name}')">
                            <div class="ton-icon"></div>
                            <span>${firstGift.price}</span>
                        </button>
                    </div>
                `;
            }).join('');
        }
        
        function switchTab(tab) {
            currentView = tab;
            
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
        
        function openGiftGroupDetail(giftName) {
            const giftsInGroup = allGifts.filter(gift => gift.name === giftName);
            if (giftsInGroup.length === 1) {
                openGiftDetail(giftsInGroup[0].id);
            } else {
                tg.showAlert(`Группа ${giftName}: ${giftsInGroup.length} подарков`);
            }
        }
        
        function showGiftGroupPrices(giftName) {
            const giftsInGroup = allGifts.filter(gift => gift.name === giftName && gift.listed);
            const prices = giftsInGroup.map(gift => `${gift.price} TON (${gift.count})`).join(', ');
            tg.showAlert(`Цены ${giftName}: ${prices}`);
        }
        
        let currentGiftDetail = null;
        function openGiftDetail(giftId) {
            const gift = allGifts.find(g => g.id === giftId);
            if (!gift) return;
            
            currentGiftDetail = gift;
            
            document.getElementById('giftDetailImage').style.backgroundImage = `url('${gift.image}')`;
            document.getElementById('giftDetailTitle').textContent = gift.name;
            document.getElementById('giftDetailId').textContent = `#${gift.id}`;
            
            // Оновлюємо кнопку ціни з TON іконкою
            const priceBtn = document.getElementById('giftDetailPrice');
            priceBtn.innerHTML = `
                <div class="ton-icon"></div>
                <span>${gift.price} TON</span>
                <span>(${gift.count})</span>
            `;
            
            document.getElementById('giftDetailModal').classList.add('show');
        }
        
        function closeGiftDetail() {
            document.getElementById('giftDetailModal').classList.remove('show');
            currentGiftDetail = null;
        }
        
        function buyGiftFromDetail() {
            if (currentGiftDetail) {
                buyGift(currentGiftDetail.id);
                closeGiftDetail();
            }
        }
        
        function buyGift(id) {
            const gift = allGifts.find(g => g.id === id);
            tg.showAlert(`Покупаем подарок #${id}: ${gift.name} за ${gift.price} TON`);
        }
        
        function createChannel() {
            tg.showAlert('Создание Telegram канала для продажи подарков');
        }
        
        function createAd() {
            createChannel();
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
        f"📺 Магазин Telegram каналов с подарками\n"
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
    
    print("🎁 GiftRoom Market з My Channel запущен!")
    print(f"🌐 URL: {WEBAPP_URL}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
