"""
Головний файл FastAPI для GiftRoom Marketplace
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import asyncio
import threading

# Імпорти нашого додатка
from app.config import settings
from app.database import startup_database, close_db, database_manager
from app.api import auth, channels, gifts, transactions, referrals, wallet

# Налаштування логування
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Telegram Bot
from bot.handlers import setup_bot, start_bot_webhook, stop_bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Менеджер життєвого циклу додатка
    """
    # Startup
    logger.info("🚀 Starting GiftRoom Marketplace...")
    
    try:
        # Ініціалізація бази даних
        await startup_database()
        logger.info("✅ Database initialized")
        
        # Запуск Telegram Bot
        await setup_bot()
        logger.info("✅ Telegram Bot initialized")
        
        # Запуск періодичних задач
        asyncio.create_task(periodic_tasks())
        logger.info("✅ Periodic tasks started")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down GiftRoom Marketplace...")
    
    try:
        await stop_bot()
        await close_db()
        logger.info("✅ Graceful shutdown completed")
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")


# Створення додатка
app = FastAPI(
    title=settings.app_name,
    description="Безпечний маркетплейс для продажу Telegram каналів з подарунками",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.onrender.com", "giftroom-marketplace.onrender.com"]
    )

# Статичні файли
if os.path.exists("frontend/static"):
    app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# API роути
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Автентифікація"])
app.include_router(channels.router, prefix="/api/v1/channels", tags=["Канали"])
app.include_router(gifts.router, prefix="/api/v1/gifts", tags=["Подарунки"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Транзакції"])
app.include_router(referrals.router, prefix="/api/v1/referrals", tags=["Реферали"])
app.include_router(wallet.router, prefix="/api/v1/wallet", tags=["Гаманець"])


# Основні роути
@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Головна сторінка - Telegram Mini App
    """
    try:
        # Читаємо HTML файл
        html_path = os.path.join("frontend", "index.html")
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Замінюємо змінні в HTML
            content = content.replace("{{WEBAPP_URL}}", settings.webapp_url)
            return HTMLResponse(content=content)
        else:
            # Якщо файл не знайдено, повертаємо базовий HTML
            return HTMLResponse(content=get_fallback_html())
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        return HTMLResponse(content=get_fallback_html())


@app.get("/health")
async def health_check():
    """
    Перевірка здоров'я системи
    """
    try:
        # Перевірка бази даних
        db_healthy = await database_manager.health_check()
        
        # Перевірка бота (якщо потрібно)
        # bot_healthy = await bot_health_check()
        
        return JSONResponse(
            content={
                "status": "healthy" if db_healthy else "unhealthy",
                "version": settings.app_version,
                "database": "ok" if db_healthy else "error",
                "environment": settings.environment
            },
            status_code=200 if db_healthy else 503
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=503
        )


@app.get("/info")
async def app_info():
    """
    Інформація про додаток
    """
    try:
        db_info = await database_manager.get_db_info()
        
        return {
            "app_name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "debug": settings.debug,
            "database": db_info,
            "features": {
                "ton_integration": True,
                "referral_system": True,
                "escrow_system": True,
                "telegram_bot": True
            }
        }
    except Exception as e:
        logger.error(f"Failed to get app info: {e}")
        return {"error": str(e)}


@app.post("/webhook/bot")
async def bot_webhook(request: Request):
    """
    Webhook для Telegram Bot
    """
    try:
        from bot.handlers import handle_webhook
        
        data = await request.json()
        await handle_webhook(data)
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Bot webhook error: {e}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")


# Обробка помилок
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """
    Обробка 404 помилок
    """
    return JSONResponse(
        status_code=404,
        content={"message": "Сторінка не знайдена", "path": request.url.path}
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """
    Обробка внутрішніх помилок
    """
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Внутрішня помилка сервера"}
    )


# Періодичні задачі
async def periodic_tasks():
    """
    Періодичні задачі системи
    """
    while True:
        try:
            # Очищення застарілих транзакцій кожні 5 хвилин
            await database_manager.cleanup_expired_transactions()
            
            # Оновлення статистики подарунків кожні 30 хвилин
            # await update_gift_statistics()
            
            await asyncio.sleep(300)  # 5 хвилин
            
        except Exception as e:
            logger.error(f"Periodic task error: {e}")
            await asyncio.sleep(60)  # При помилці чекаємо 1 хвилину


def get_fallback_html() -> str:
    """
    Резервний HTML якщо основний файл не знайдено
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GiftRoom Market</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background: #0F0F19;
                color: white;
                text-align: center;
            }
            .container {
                max-width: 400px;
                margin: 50px auto;
                padding: 30px;
                background: #2a2a3e;
                border-radius: 20px;
            }
            h1 {
                color: #3d5afe;
                margin-bottom: 20px;
            }
            .status {
                background: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 25px;
                display: inline-block;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎁 GiftRoom Market</h1>
            <div class="status">Сервер працює</div>
            <p>Маркетплейс Telegram каналів з подарунками</p>
            <p>Версія: """ + settings.app_version + """</p>
            <p>Середовище: """ + settings.environment + """</p>
        </div>
    </body>
    </html>
    """


# Якщо запускаємо напряму
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"🎁 Starting GiftRoom Marketplace on port {port}")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
