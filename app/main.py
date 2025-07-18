"""
main.py з базовими API для GiftRoom Marketplace
"""
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
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

# Демо дані
DEMO_USER = User(
    id=1,
    telegram_id=123456789,
    username="demo_user",
    first_name="Demo User",
    balance=50.0,
    total_bought=3,
    total_sold=8,
    total_volume=207.5
)

DEMO_CHANNELS = [
    Channel(
        id=1,
        display_name="@fashion_style",
        price=25.50,
        total_gifts=15000,
        unique_gifts=6,
        status="active",
        main_gift=Gift(
            id=1,
            gift_name="HEELS",
            count=11500,
            gift_image_url="https://i.postimg.cc/jdsL20Gt/Gifts-Gifts-Gifts-Ag-ADBmg-AAnz-Oe-Ek.png"
        ),
        gifts=[
            Gift(id=1, gift_name="HEELS", count=11500, gift_image_url="https://i.postimg.cc/jdsL20Gt/Gifts-Gifts-Gifts-Ag-ADBmg-AAnz-Oe-Ek.png"),
            Gift(id=4, gift_name="SOCKS", count=2834, gift_image_url="https://i.postimg.cc/bwxCTnmQ/Gifts-Gifts-Gifts-Ag-ADKmk-AAt0-L2-Ek.png"),
            Gift(id=36, gift_name="SWAG BAG", count=34, gift_image_url="https://i.postimg.cc/d1cwkrNg/Gifts-Gifts-Gifts-Ag-AD5-XMAAmjze-Us.png"),
        ]
    ),
    Channel(
        id=2,
        display_name="@cat_lovers",
        price=15.25,
        total_gifts=8500,
        unique_gifts=6,
        status="active",
        main_gift=Gift(
            id=3,
            gift_name="CATS",
            count=2945,
            gift_image_url="https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"
        ),
        gifts=[
            Gift(id=3, gift_name="CATS", count=2945, gift_image_url="https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png"),
            Gift(id=17, gift_name="MONKEY", count=1401, gift_image_url="https://i.postimg.cc/bN7Yn75Z/Gifts-Gifts-Gifts-Ag-AEZAACV66-BSw.png"),
            Gift(id=21, gift_name="RABBIT", count=967, gift_image_url="https://i.postimg.cc/WtLRDv4j/Gifts-Gifts-Gifts-Ag-ADh-HUAAg-O6-IUg.png"),
        ]
    ),
    Channel(
        id=3,
        display_name="@tech_store",
        price=45.00,
        total_gifts=12000,
        unique_gifts=6,
        status="active",
        main_gift=Gift(
            id=6,
            gift_name="LAMP",
            count=2612,
            gift_image_url="https://i.postimg.cc/hjfNpjzc/Gifts-Gifts-Gifts-Ag-ADj-Gw-AAkl0c-Eo.png"
        ),
        gifts=[
            Gift(id=6, gift_name="LAMP", count=2612, gift_image_url="https://i.postimg.cc/hjfNpjzc/Gifts-Gifts-Gifts-Ag-ADj-Gw-AAkl0c-Eo.png"),
            Gift(id=10, gift_name="DYSON", count=2178, gift_image_url="https://i.postimg.cc/3NZjGj8R/Gifts-Gifts-Gifts-Ag-ADhmw-AAl1-Zc-Uo.png"),
            Gift(id=19, gift_name="ROCKET", count=1189, gift_image_url="https://i.postimg.cc/nhfZrvs7/Gifts-Gifts-Gifts-Ag-ADIo-UAAk3-J2-Es.png"),
        ]
    ),
    Channel(
        id=4,
        display_name="@hiphop_central",
        price=67.30,
        total_gifts=890,
        unique_gifts=6,
        status="active",
        main_gift=Gift(
            id=37,
            gift_name="SNOOP DOGG",
            count=15,
            gift_image_url="https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"
        ),
        gifts=[
            Gift(id=37, gift_name="SNOOP DOGG", count=15, gift_image_url="https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"),
            Gift(id=33, gift_name="WESTSIDE SIGN", count=67, gift_image_url="https://i.postimg.cc/GtkBTbjx/Gifts-Gifts-Gifts-Ag-ADV4-QAAiibe-Us.png"),
            Gift(id=34, gift_name="LOW RIDER", count=23, gift_image_url="https://i.postimg.cc/7Y96Fsth/Gifts-Gifts-Gifts-Ag-ADNWw-AAg5ze-Es.png"),
        ]
    )
]

# Основні роути
@app.get("/")
async def root():
    """Головна сторінка"""
    try:
        html_path = Path("frontend/index.html")
        if html_path.exists():
            with open(html_path, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        else:
            return HTMLResponse(content=get_simple_html())
    except Exception:
        return HTMLResponse(content=get_simple_html())

@app.get("/health")
async def health():
    """Перевірка здоров'я"""
    return {"status": "healthy", "app": "GiftRoom Marketplace"}

# API роути для автентифікації
@app.post("/api/v1/auth/telegram-auth")
async def telegram_auth(init_data: str):
    """Автентифікація через Telegram"""
    # Тут має бути валідація init_data, але для демо повертаємо фіксовані дані
    return {
        "success": True,
        "access_token": "demo_token_12345",
        "token_type": "bearer",
        "user": DEMO_USER.dict()
    }

@app.get("/api/v1/auth/me")
async def get_current_user():
    """Отримання поточного користувача"""
    return DEMO_USER.dict()

# API роути для каналів
@app.get("/api/v1/channels/")
async def get_channels(
    page: int = 1,
    size: int = 20,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None
):
    """Отримання списку каналів"""
    channels = DEMO_CHANNELS.copy()
    
    # Фільтрація
    if min_price:
        channels = [c for c in channels if c.price >= min_price]
    if max_price:
        channels = [c for c in channels if c.price <= max_price]
    if search:
        channels = [c for c in channels if search.lower() in c.display_name.lower()]
    
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
        "data": [c.dict() for c in page_channels]
    }

@app.get("/api/v1/channels/{channel_id}")
async def get_channel(channel_id: int):
    """Отримання деталей каналу"""
    channel = next((c for c in DEMO_CHANNELS if c.id == channel_id), None)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    return channel.dict()

@app.get("/api/v1/channels/my/channels")
async def get_my_channels():
    """Отримання каналів користувача"""
    # Для демо повертаємо пустий список
    return []

# API роути для транзакцій
@app.post("/api/v1/transactions/")
async def create_transaction(transaction_data: dict):
    """Створення транзакції"""
    return {
        "success": True,
        "message": "Транзакція створена! (демо режим)",
        "transaction_id": 12345
    }

@app.get("/api/v1/transactions/")
async def get_transactions():
    """Отримання транзакцій"""
    return {
        "success": True,
        "total": 0,
        "page": 1,
        "size": 20,
        "pages": 0,
        "data": []
    }

# API роути для гаманця
@app.post("/api/v1/wallet/connect")
async def connect_wallet():
    """Підключення гаманця"""
    return {"success": True, "message": "Wallet connected (demo)"}

@app.post("/api/v1/wallet/top-up")
async def top_up_balance():
    """Поповнення балансу"""
    return {"success": True, "message": "Balance topped up (demo)"}

def get_simple_html():
    """Простий HTML для fallback"""
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
                max-width: 400px; 
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
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎁 GiftRoom Market</h1>
            <div class="status">✅ API працює</div>
            <p>Маркетплейс Telegram каналів з подарунками</p>
            <p>Додайте frontend/index.html для повного інтерфейсу</p>
            <p><a href="/docs" style="color: #3d5afe;">📋 API Документація</a></p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
