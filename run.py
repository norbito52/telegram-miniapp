#!/usr/bin/env python3
"""
Скрипт для запуску GiftRoom Marketplace
"""
import asyncio
import os
import sys
import logging
from pathlib import Path

# Додаємо корінь проєкту в sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.config import settings
from app.database import test_connection, startup_database
from app.main import app

# Налаштування логування
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def check_environment():
    """Перевірка середовища"""
    logger.info("🔍 Checking environment...")
    
    # Перевірка змінних середовища
    required_vars = ['BOT_TOKEN', 'DATABASE_URL', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not getattr(settings, var.lower(), None):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        logger.error("Please check your .env file")
        return False
    
    logger.info("✅ Environment variables OK")
    return True


async def check_database():
    """Перевірка підключення до бази даних"""
    logger.info("🔍 Checking database connection...")
    
    try:
        success = await test_connection()
        if success:
            logger.info("✅ Database connection OK")
            return True
        else:
            logger.error("❌ Database connection failed")
            return False
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
        return False


async def run_migrations():
    """Запуск міграцій"""
    logger.info("🔄 Running database migrations...")
    
    try:
        # Запускаємо Alembic міграції
        import subprocess
        result = subprocess.run(
            ['alembic', 'upgrade', 'head'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("✅ Database migrations completed")
            return True
        else:
            logger.error(f"❌ Migration failed: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Migration error: {e}")
        return False


async def main():
    """Головна функція"""
    logger.info("🚀 Starting GiftRoom Marketplace...")
    
    # Перевірка середовища
    if not await check_environment():
        sys.exit(1)
    
    # Перевірка бази даних
    if not await check_database():
        sys.exit(1)
    
    # Запуск міграцій
    if settings.is_development:
        if not await run_migrations():
            logger.warning("⚠️  Migration failed, but continuing...")
    
    # Ініціалізація бази даних
    try:
        await startup_database()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        sys.exit(1)
    
    # Запуск сервера
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"
    
    logger.info(f"🌐 Starting server on {host}:{port}")
    logger.info(f"📱 Telegram Bot: @{settings.bot_token.split(':')[0]}")
    logger.info(f"🌍 Web App URL: {settings.webapp_url}")
    logger.info(f"📊 Environment: {settings.environment}")
    
    try:
        config = uvicorn.Config(
            app,
            host=host,
            port=port,
            log_level=settings.log_level.lower(),
            reload=settings.debug,
            access_log=True
        )
        server = uvicorn.Server(config)
        await server.serve()
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        sys.exit(1)


def run_development():
    """Запуск в режимі розробки"""
    logger.info("🔧 Starting in development mode...")
    
    # Додаткові налаштування для розробки
    os.environ['DEBUG'] = 'True'
    os.environ['ENVIRONMENT'] = 'development'
    
    # Запуск з reload
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        reload_dirs=["app", "bot", "services"],
        log_level="info"
    )


def run_production():
    """Запуск в продакшн режимі"""
    logger.info("🚀 Starting in production mode...")
    
    # Запуск через asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Application stopped")
    except Exception as e:
        logger.error(f"❌ Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Перевіряємо аргументи командного рядка
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "dev":
            run_development()
        elif command == "prod":
            run_production()
        elif command == "check":
            # Перевірка налаштувань
            asyncio.run(check_environment())
            asyncio.run(check_database())
        elif command == "migrate":
            # Запуск міграцій
            asyncio.run(run_migrations())
        else:
            print("Usage: python run.py [dev|prod|check|migrate]")
            sys.exit(1)
    else:
        # За замовчуванням запускаємо в продакшн режимі
        run_production()
