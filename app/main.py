"""
Головний файл FastAPI для GiftRoom Marketplace
"""
import os
import logging
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Налаштовуємо логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Створюємо FastAPI додаток
app = FastAPI(
    title="GiftRoom Marketplace",
    description="Безпечний маркетплейс для продажу Telegram каналів з подарунками",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Додаємо CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # У продакшн змініть на конкретні домени
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статичні файли
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Головна сторінка - Telegram Mini App"""
    try:
        # Шукаємо HTML файл
        html_path = Path(__file__).parent.parent / "frontend" / "index.html"
        
        if html_path.exists():
            with open(html_path, "r", encoding="utf-8") as f:
                content = f.read()
            return HTMLResponse(content=content)
        else:
            # Fallback HTML
            return HTMLResponse(content=get_fallback_html())
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        return HTMLResponse(content=get_fallback_html())

@app.get("/health")
async def health_check():
    """Перевірка здоров'я системи"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "message": "GiftRoom Marketplace is running"
    }

@app.get("/info")
async def app_info():
    """Інформація про додаток"""
    return {
        "app_name": "GiftRoom Marketplace",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "features": {
            "telegram_bot": True,
            "ton_integration": True,
            "referral_system": True
        }
    }

def get_fallback_html() -> str:
    """Резервний HTML"""
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
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                max-width: 400px;
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
            .rocket {
                font-size: 48px;
                margin-bottom: 20px;
                animation: bounce 2s ease-in-out infinite;
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="rocket">🚀</div>
            <h1>GiftRoom Market</h1>
            <div class="status">Сервер працює</div>
            <p>Маркетплейс Telegram каналів з подарунками</p>
            <p>Версія: 1.0.0</p>
        </div>
    </body>
    </html>
    """

# Обробка помилок
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Обробка 404 помилок"""
    return JSONResponse(
        status_code=404,
        content={"message": "Сторінка не знайдена", "path": str(request.url.path)}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """Обробка внутрішніх помилок"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Внутрішня помилка сервера"}
    )

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
