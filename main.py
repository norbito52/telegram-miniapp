"""
Головний файл для запуску на Render
"""
import os
import sys
from pathlib import Path

# Додаємо корінь проєкту в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Встановлюємо PYTHONPATH
os.environ['PYTHONPATH'] = str(project_root)

# Імпортуємо FastAPI додаток
from app.main import app

# Експортуємо додаток для uvicorn
__all__ = ['app']

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
