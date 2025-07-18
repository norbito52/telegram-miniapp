"""
main.py з повним інтерфейсом GiftRoom Marketplace
"""
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json

# Створюємо FastAPI додаток
app = FastAPI(title="GiftRoom Marketplace")

# Додаємо CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic моделі
class User(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    balance: float = 0.0
    total_bought: int = 0
    total_sold: int = 0
    total_volume: float = 0.0
    referral_code: Optional[str] = None

class Gift(BaseModel):
    id: int
    gift_name: str
    count: int
    gift_image_url: str

class Channel(BaseModel):
    id: int
    display_name: str
    price: float
    total_gifts: int
    unique_gifts: int
    status: str
    main_gift: Optional[Gift] = None
    gifts: List[Gift] = []

# ПОВНА база подарунків як у вашому коді
ALL_GIFTS = {
    37: {"id": 37, "name": "SNOOP DOGG", "desc": "Legendary rapper", "image": "https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"},
    36: {"id": 36, "name": "SWAG BAG", "desc": "Stylish bag", "image": "https://i.postimg.cc/d1cwkrNg/Gifts-Gifts-Gifts-Ag-AD5-XMAAmjze-Us.png"},
    35: {"id": 35, "name": "SNOOP CIGAR", "desc": "Smoking cigar", "image": "https://i.postimg.cc/FKMsy2zW/Gifts-Gifts-Gifts-Ag-ADi38-AAg-7c-Es.png"},
    34: {"id": 34, "name": "LOW RIDER", "desc": "Cool car", "image": "https://i.postimg.cc/7Y96Fsth/Gifts-Gifts-Gifts-Ag-ADNWw-AAg5ze-Es.png"},
    33: {"id": 33, "name": "WESTSIDE SIGN", "desc": "West coast sign", "image": "https://i.postimg.cc/GtkBTbjx/Gifts-Gifts-Gifts-Ag-ADV4-QAAiibe-Us.png"},
    32: {"id": 32, "name": "TORCH", "desc": "Olympic torch", "image": "https://i.postimg.cc/wv1LMKPw/Gifts-Gifts-Gifts-Ag-AD2-XQAAk-VPSEs.png"},
    31: {"id": 31, "name": "STATUE", "desc": "Ancient statue", "image": "https://i.postimg.cc/V6hvVdKR/Gifts-Gifts-Gifts-Ag-ADi-IYAAqf-LQEs.png"},
    30: {"id": 30, "name": "EAGLE", "desc": "Majestic eagle", "image": "https://i.postimg.cc/0QXK1ty7/Gifts-Gifts-Gifts-Ag-ADzn-IAAl-Gn-QEs.png"},
    29: {"id": 29, "name": "NIPPLE", "desc": "Baby nipple", "image": "https://i.postimg.cc/BQrDvwcg/Gifts-Gifts-Gifts-Ag-ADD3-IAAm-RNKUo.png"},
    28: {"id": 28, "name": "PLUMBER", "desc": "Mario plumber", "image": "https://i.postimg.cc/85pLSJBg/Gifts-Gifts-Gifts-Ag-ADKX4-AAuw-O2-Ek.png"},
    27: {"id": 27, "name": "ESKIMO", "desc": "Cold eskimo", "image": "https://i.postimg.cc/L4y3mTbC/Gifts-Gifts-Gifts-Ag-ADy-XEAAky04-Ek.png"},
    26: {"id": 26, "name": "CREAMY ICE CREAM", "desc": "Creamy ice cream", "image": "https://i.postimg.cc/ydjXgXYN/Gifts-Gifts-Gifts-Ag-AD0-Ww-AAs4-T4-Ek.png"},
    25: {"id": 25, "name": "STAR", "desc": "Shining star", "image": "https://i.postimg.cc/3Nr1nfbp/Gifts-Gifts-Gifts-Ag-ADbn-UAAl-XNEUk.png"},
    24: {"id": 24, "name": "PIGEON", "desc": "City pigeon", "image": "https://i.postimg.cc/QxJsBFcy/Gifts-Gifts-Gifts-Ag-ADa3-QAAtw-JEEk.png"},
    23: {"id": 23, "name": "MEDAL", "desc": "Gold medal", "image": "https://i.postimg.cc/N0zQgZRG/Gifts-Gifts-Gifts-Ag-ADO3c-AAqb-DEEk.png"},
    22: {"id": 22, "name": "1 MAY", "desc": "Labor day", "image": "https://i.postimg.cc/gJxk8GG6/Gifts-Gifts-Gifts-Ag-ADMm4-AAj-Ll6-Ug.png"},
    21: {"id": 21, "name": "RABBIT", "desc": "Fluffy rabbit", "image": "https://i.postimg.cc/WtLRDv4j/Gifts-Gifts-Gifts-Ag-ADh-HUAAg-O6-IUg.png"},
    20: {"id": 20, "name": "KULICH", "desc": "Easter cake", "image": "https://i.postimg.cc/tTJGwkf0/Gifts-Gifts-Gifts-Ag-ADBa-UAAk8-WKEg.png"},
    19: {"id": 19, "name": "ROCKET", "desc": "Space rocket", "image": "https://i.postimg.cc/nhfZrvs7/Gifts-Gifts-Gifts-Ag-ADIo-UAAk3-J2-Es.png"},
    18: {"id": 18, "name": "BRICK", "desc": "Building brick", "image": "https://i.postimg.cc/c1jdyq0F/Gifts-Gifts-Gifts-Ag-ADg2o-AAg-R5g-Us.png"},
    17: {"id": 17, "name": "MONKEY", "desc": "Playful monkey", "image": "https://i.postimg.cc/bN7Yn75Z/Gifts-Gifts-Gifts-Ag-AEZAACV66-BSw.png"},
    16: {"id": 16, "name": "POOP", "desc": "Funny poop", "image": "https://i.postimg.cc/05HykMdd/Gifts-Gifts-Gifts-Ag-AD82w-AAk-FZg-Es.png"},
    15: {"id": 15, "name": "DOSHIK", "desc": "Instant noodles", "image": "https://i.postimg.cc/k5F5qTfB/Gifts-Gifts-Gifts-Ag-AD4-GQAAq8-Xg-Us.png"},
    14: {"id": 14, "name": "MOSQUE", "desc": "Beautiful mosque", "image": "https://i.postimg.cc/pr1T3ykC/Gifts-Gifts-Gifts-Ag-ADV3-MAAnv-We-Us.png"},
    13: {"id": 13, "name": "AMULET", "desc": "Protection amulet", "image": "https://i.postimg.cc/hGFJSzn3/Gifts-Gifts-Gifts-Ag-AD-HEAAq-9c-Us.png"},
    12: {"id": 12, "name": "CLOVER", "desc": "Lucky clover", "image": "https://i.postimg.cc/NfJmwjLW/Gifts-Gifts-Gifts-Ag-ADf-GYAAjfaw-Uo.png"},
    11: {"id": 11, "name": "BOILER", "desc": "Hot boiler", "image": "https://i.postimg.cc/Dfc1Bghf/Gifts-Gifts-Gifts-Ag-ADe-WMAAp-Rw-IUs.png"},
    10: {"id": 10, "name": "DYSON", "desc": "Powerful vacuum", "image": "https://i.postimg.cc/3NZjGj8R/Gifts-Gifts-Gifts-Ag-ADhmw-AAl1-Zc-Uo.png"},
    9: {"id": 9, "name": "MARCH 8", "desc": "Women's day", "image": "https://i.postimg.cc/d1y4hTZk/Gifts-Gifts-Gifts-Ag-ADh2o-AAoa-Dc-Eo.png"},
    8: {"id": 8, "name": "CUPCAKE", "desc": "Sweet cupcake", "image": "https://i.postimg.cc/gkqtyRS3/Gifts-Gifts-Gifts-Ag-ADB3-AAAr-Pqc-Eo.png"},
    7: {"id": 7, "name": "BOUQUET", "desc": "Beautiful bouquet", "image": "https://i.postimg.cc/TY8BJTRv/Gifts-Gifts-Gifts-Ag-ADk3-AAAiy-WGEs.png"},
    6: {"id": 6, "name": "LAMP", "desc": "Table lamp", "image": "https://i.postimg.cc/hjfNpjzc/Gifts-Gifts-Gifts-Ag-ADj-Gw-AAkl0c-Eo.png"},
    5: {"id": 5, "name": "BICEPS", "desc": "Strong muscles", "image": "https://i.postimg.cc/K4Xf7cLq/Gifts-Gifts-Gifts-Ag-ADB3-UAAp5-V0-Uk.png"},
    4: {"id": 4, "name": "SOCKS", "desc": "Warm socks", "image": "https://i.postimg.cc/bwxCTnmQ/Gifts-Gifts-Gifts-Ag-ADKmk-AAt0-L2-Ek.png"},
    3: {"id": 3, "name": "CATS", "desc": "Cute cats", "image": "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"},
    2: {"id": 2, "name": "BUTTON", "desc": "Simple button", "image": "https://i.postimg.cc/XqDSnCRZ/Gifts-Gifts-Gifts-Ag-ADWWg-AAhwgi-Uk.png"},
    1: {"id": 1, "name": "HEELS", "desc": "High heels", "image": "https://i.postimg.cc/jdsL20Gt/Gifts-Gifts-Gifts-Ag-ADBmg-AAnz-Oe-Ek.png"}
}

# ПОВНА база каналів як у вашому коді
DEMO_CHANNELS_FULL = [
    {
        "id": 1,
        "display_name": "@fashion_style",
        "price": 25.50,
        "total_gifts": 15789,
        "unique_gifts": 6,
        "status": "active",
        "main_gift": {"id": 1, "gift_name": "HEELS", "count": 11500, "gift_image_url": ALL_GIFTS[1]["image"]},
        "gifts": [
            {"id": 1, "gift_name": "HEELS", "count": 11500, "gift_image_url": ALL_GIFTS[1]["image"]},
            {"id": 4, "gift_name": "SOCKS", "count": 2834, "gift_image_url": ALL_GIFTS[4]["image"]},
            {"id": 36, "gift_name": "SWAG BAG", "count": 34, "gift_image_url": ALL_GIFTS[36]["image"]},
            {"id": 2, "gift_name": "BUTTON", "count": 356, "gift_image_url": ALL_GIFTS[2]["image"]},
            {"id": 25, "gift_name": "STAR", "count": 1240, "gift_image_url": ALL_GIFTS[25]["image"]},
            {"id": 7, "gift_name": "BOUQUET", "count": 890, "gift_image_url": ALL_GIFTS[7]["image"]}
        ]
    },
    {
        "id": 2,
        "display_name": "@cat_lovers",
        "price": 15.25,
        "total_gifts": 7335,
        "unique_gifts": 6,
        "status": "active",
        "main_gift": {"id": 3, "gift_name": "CATS", "count": 2945, "gift_image_url": ALL_GIFTS[3]["image"]},
        "gifts": [
            {"id": 3, "gift_name": "CATS", "count": 2945, "gift_image_url": ALL_GIFTS[3]["image"]},
            {"id": 17, "gift_name": "MONKEY", "count": 1401, "gift_image_url": ALL_GIFTS[17]["image"]},
            {"id": 21, "gift_name": "RABBIT", "count": 967, "gift_image_url": ALL_GIFTS[21]["image"]},
            {"id": 1, "gift_name": "HEELS", "count": 250, "gift_image_url": ALL_GIFTS[1]["image"]},
            {"id": 24, "gift_name": "PIGEON", "count": 723, "gift_image_url": ALL_GIFTS[24]["image"]},
            {"id": 30, "gift_name": "EAGLE", "count": 567, "gift_image_url": ALL_GIFTS[30]["image"]}
        ]
    },
    {
        "id": 3,
        "display_name": "@tech_store",
        "price": 45.00,
        "total_gifts": 7659,
        "unique_gifts": 6,
        "status": "active",
        "main_gift": {"id": 6, "gift_name": "LAMP", "count": 2612, "gift_image_url": ALL_GIFTS[6]["image"]},
        "gifts": [
            {"id": 6, "gift_name": "LAMP", "count": 2612, "gift_image_url": ALL_GIFTS[6]["image"]},
            {"id": 10, "gift_name": "DYSON", "count": 2178, "gift_image_url": ALL_GIFTS[10]["image"]},
            {"id": 19, "gift_name": "ROCKET", "count": 1189, "gift_image_url": ALL_GIFTS[19]["image"]},
            {"id": 2, "gift_name": "BUTTON", "count": 890, "gift_image_url": ALL_GIFTS[2]["image"]},
            {"id": 27, "gift_name": "ESKIMO", "count": 456, "gift_image_url": ALL_GIFTS[27]["image"]},
            {"id": 18, "gift_name": "BRICK", "count": 334, "gift_image_url": ALL_GIFTS[18]["image"]}
        ]
    },
    {
        "id": 4,
        "display_name": "@sweet_treats",
        "price": 18.75,
        "total_gifts": 6609,
        "unique_gifts": 6,
        "status": "active",
        "main_gift": {"id": 8, "gift_name": "CUPCAKE", "count": 2390, "gift_image_url": ALL_GIFTS[8]["image"]},
        "gifts": [
            {"id": 8, "gift_name": "CUPCAKE", "count": 2390, "gift_image_url": ALL_GIFTS[8]["image"]},
            {"id": 15, "gift_name": "DOSHIK", "count": 1623, "gift_image_url": ALL_GIFTS[15]["image"]},
            {"id": 26, "gift_name": "CREAMY ICE CREAM", "count": 423, "gift_image_url": ALL_GIFTS[26]["image"]},
            {"id": 3, "gift_name": "CATS", "count": 150, "gift_image_url": ALL_GIFTS[3]["image"]},
            {"id": 20, "gift_name": "KULICH", "count": 789, "gift_image_url": ALL_GIFTS[20]["image"]},
            {"id": 16, "gift_name": "POOP", "count": 1234, "gift_image_url": ALL_GIFTS[16]["image"]}
        ]
    },
    {
        "id": 5,
        "display_name": "@hiphop_central",
        "price": 67.30,
        "total_gifts": 828,
        "unique_gifts": 6,
        "status": "active",
        "main_gift": {"id": 37, "gift_name": "SNOOP DOGG", "count": 15, "gift_image_url": ALL_GIFTS[37]["image"]},
        "gifts": [
            {"id": 37, "gift_name": "SNOOP DOGG", "count": 15, "gift_image_url": ALL_GIFTS[37]["image"]},
            {"id": 33, "gift_name": "WESTSIDE SIGN", "count": 67, "gift_image_url": ALL_GIFTS[33]["image"]},
            {"id": 34, "gift_name": "LOW RIDER", "count": 23, "gift_image_url": ALL_GIFTS[34]["image"]},
            {"id": 36, "gift_name": "SWAG BAG", "count": 89, "gift_image_url": ALL_GIFTS[36]["image"]},
            {"id": 35, "gift_name": "SNOOP CIGAR", "count": 345, "gift_image_url": ALL_GIFTS[35]["image"]},
            {"id": 32, "gift_name": "TORCH", "count": 178, "gift_image_url": ALL_GIFTS[32]["image"]}
        ]
    },
    {
        "id": 6,
        "display_name": "@button_collectors",
        "price": 12.50,
        "total_gifts": 6457,
        "unique_gifts": 6,
        "status": "active",
        "main_gift": {"id": 2, "gift_name": "BUTTON", "count": 5600, "gift_image_url": ALL_GIFTS[2]["image"]},
        "gifts": [
            {"id": 2, "gift_name": "BUTTON", "count": 5600, "gift_image_url": ALL_GIFTS[2]["image"]},
            {"id": 6, "gift_name": "LAMP", "count": 234, "gift_image_url": ALL_GIFTS[6]["image"]},
            {"id": 5, "gift_name": "BICEPS", "count": 567, "gift_image_url": ALL_GIFTS[5]["image"]},
            {"id": 22, "gift_name": "1 MAY", "count": 89, "gift_image_url": ALL_GIFTS[22]["image"]},
            {"id": 12, "gift_name": "CLOVER", "count": 234, "gift_image_url": ALL_GIFTS[12]["image"]},
            {"id": 9, "gift_name": "MARCH 8", "count": 567, "gift_image_url": ALL_GIFTS[9]["image"]}
        ]
    },
    {
        "id": 7,
        "display_name": "@sports_arena",
        "price": 33.75,
        "total_gifts": 3268,
        "unique_gifts": 6,
        "status": "active",
        "main_gift": {"id": 22, "gift_name": "1 MAY", "count": 1234, "gift_image_url": ALL_GIFTS[22]["image"]},
        "gifts": [
            {"id": 22, "gift_name": "1 MAY", "count": 1234, "gift_image_url": ALL_GIFTS[22]["image"]},
            {"id": 9, "gift_name": "MARCH 8", "count": 456, "gift_image_url": ALL_GIFTS[9]["image"]},
            {"id": 5, "gift_name": "BICEPS", "count": 789, "gift_image_url": ALL_GIFTS[5]["image"]},
            {"id": 28, "gift_name": "PLUMBER", "count": 123, "gift_image_url": ALL_GIFTS[28]["image"]},
            {"id": 31, "gift_name": "STATUE", "count": 345, "gift_image_url": ALL_GIFTS[31]["image"]},
            {"id": 32, "gift_name": "TORCH", "count": 678, "gift_image_url": ALL_GIFTS[32]["image"]}
        ]
    },
    {
        "id": 8,
        "display_name": "@cultural_gifts",
        "price": 41.25,
        "total_gifts": 2057,
        "unique_gifts": 5,
        "status": "active",
        "main_gift": {"id": 11, "gift_name": "BOILER", "count": 789, "gift_image_url": ALL_GIFTS[11]["image"]},
        "gifts": [
            {"id": 14, "gift_name": "MOSQUE", "count": 234, "gift_image_url": ALL_GIFTS[14]["image"]},
            {"id": 13, "gift_name": "AMULET", "count": 156, "gift_image_url": ALL_GIFTS[13]["image"]},
            {"id": 11, "gift_name": "BOILER", "count": 789, "gift_image_url": ALL_GIFTS[11]["image"]},
            {"id": 31, "gift_name": "STATUE", "count": 345, "gift_image_url": ALL_GIFTS[31]["image"]},
            {"id": 25, "gift_name": "STAR", "count": 567, "gift_image_url": ALL_GIFTS[25]["image"]}
        ]
    }
]

# Демо користувач
DEMO_USER = {
    "id": 1,
    "telegram_id": 123456789,
    "username": "xr00y",
    "first_name": "Demo User",
    "balance": 50.0,
    "total_bought": 0,
    "total_sold": 8,
    "total_volume": 207.5,
    "referral_code": "ref_123456789"
}

# Основні роути
@app.get("/")
async def root():
    """Головна сторінка з повним інтерфейсом"""
    return HTMLResponse(content=get_full_html())

@app.get("/health")
async def health():
    """Перевірка здоров'я"""
    return {"status": "healthy", "app": "GiftRoom Marketplace"}

# API роути
@app.post("/api/v1/auth/telegram-auth")
async def telegram_auth(init_data: str):
    """Автентифікація через Telegram"""
    return {
        "success": True,
        "access_token": "demo_token_12345",
        "token_type": "bearer",
        "user": DEMO_USER
    }

@app.get("/api/v1/auth/me")
async def get_current_user():
    """Отримання поточного користувача"""
    return DEMO_USER

@app.get("/api/v1/channels/")
async def get_channels(
    page: int = 1,
    size: int = 20,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    gift_ids: Optional[str] = None
):
    """Отримання списку каналів з фільтрами"""
    channels = DEMO_CHANNELS_FULL.copy()
    
    # Фільтрація по ціні
    if min_price:
        channels = [c for c in channels if c["price"] >= min_price]
    if max_price:
        channels = [c for c in channels if c["price"] <= max_price]
    
    # Фільтрація по пошуку
    if search:
        channels = [c for c in channels if search.lower() in c["display_name"].lower()]
    
    # Фільтрація по подарунках
    if gift_ids:
        gift_id_list = [int(x) for x in gift_ids.split(',') if x.isdigit()]
        if gift_id_list:
            channels = [c for c in channels if any(gift["id"] in gift_id_list for gift in c["gifts"])]
    
    # Сортування
    if sort_by == "price":
        reverse = sort_order == "desc"
        channels.sort(key=lambda x: x["price"], reverse=reverse)
    elif sort_by == "gifts":
        reverse = sort_order == "desc"
        channels.sort(key=lambda x: x["total_gifts"], reverse=reverse)
    elif sort_by == "created_at" or not sort_by:
        reverse = sort_order != "asc"
        channels.sort(key=lambda x: x["id"], reverse=reverse)
    
    # Пагінація
    start = (page - 1) * size
    end = start + size
    page_channels = channels[start:end]
    
    return {
        "success": True,
        "total": len(channels),
        "page": page,
        "size": size,
        "pages": (len(channels) + size - 1) // size,
        "data": page_channels
    }

@app.get("/api/v1/channels/{channel_id}")
async def get_channel(channel_id: int):
    """Отримання деталей каналу"""
    channel = next((c for c in DEMO_CHANNELS_FULL if c["id"] == channel_id), None)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel

@app.get("/api/v1/gifts/")
async def get_all_gifts():
    """Отримання всіх подарунків для фільтра"""
    gifts_list = []
    for gift_id, gift_data in ALL_GIFTS.items():
        # Підраховуємо загальну кількість у всіх каналах
        total_count = 0
        for channel in DEMO_CHANNELS_FULL:
            for gift in channel["gifts"]:
                if gift["id"] == gift_id:
                    total_count += gift["count"]
        
        if total_count > 0:
            gifts_list.append({
                "id": gift_id,
                "name": gift_data["name"],
                "image": gift_data["image"],
                "totalCount": total_count
            })
    
    # Сортуємо по ID від 37 до 1
    gifts_list.sort(key=lambda x: x["id"], reverse=True)
    return gifts_list

@app.get("/api/v1/channels/my/channels")
async def get_my_channels():
    """Отримання каналів користувача"""
    return []

@app.post("/api/v1/transactions/")
async def create_transaction(transaction_data: dict):
    """Створення транзакції"""
    return {
        "success": True,
        "message": "Транзакція створена! Перевірте баланс TON.",
        "transaction_id": 12345
    }

def get_full_html():
    """Повний HTML з вашим крутим кодом"""
    try:
        html_path = Path("frontend/index.html")
        if html_path.exists():
            with open(html_path, "r", encoding="utf-8") as f:
                return f.read()
    except:
        pass
    
    # Якщо frontend/index.html не знайдено, показуємо інструкцію
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>GiftRoom Market</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: #0F0F19; 
                color: white; 
                text-align: center; 
                padding: 50px;
            }
            .container { 
                max-width: 600px; 
                margin: 0 auto; 
                background: #2a2a3e; 
                padding: 30px; 
                border-radius: 20px;
            }
            h1 { color: #3d5afe; }
            .status { 
                background: #4CAF50; 
                padding: 10px 20px; 
                border-radius: 25px; 
                margin: 20px 0;
            }
            .instruction {
                background: #3d5afe;
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                text-align: left;
            }
            code {
                background: #1a1a2e;
                padding: 15px;
                border-radius: 8px;
                display: block;
                margin: 10px 0;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎁 GiftRoom Market</h1>
            <div class="status">✅ API готове і працює!</div>
            
            <div class="instruction">
                <h3>📁 Додайте ваш HTML код:</h3>
                <p>1. Створіть папку <strong>frontend/</strong></p>
                <p>2. Помістіть ваш HTML код в <strong>frontend/index.html</strong></p>
                <p>3. Закомітьте в GitHub</p>
            </div>
            
            <div class="instruction">
                <h3>🔧 Готові API endpoints:</h3>
                <code>
GET /api/v1/channels/ - всі канали з фільтрами<br>
GET /api/v1/gifts/ - всі подарунки для фільтра<br>
GET /api/v1/auth/me - профіль користувача<br>
POST /api/v1/auth/telegram-auth - авторизація<br>
GET /docs - документація API
                </code>
            </div>
            
            <p>Після додавання HTML коду ваш крутий інтерфейс буде працювати з цими API! 🚀</p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
