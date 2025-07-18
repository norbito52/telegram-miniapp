"""
Простий main.py для Render
"""
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    """Головна сторінка"""
    try:
        # Шукаємо HTML файл
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

def get_simple_html():
    """Простий HTML"""
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
            <div class="status">✅ Сервер працює</div>
            <p>Маркетплейс Telegram каналів з подарунками</p>
            <p>Render деплой успішний!</p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
