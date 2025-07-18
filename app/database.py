"""
Підключення до бази даних для GiftRoom Marketplace
"""
import asyncio
from typing import AsyncGenerator, Optional
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from app.config import settings
from app.models import Base
import logging

logger = logging.getLogger(__name__)

# Синхронний движок для міграцій та адмінки
sync_engine = create_engine(
    settings.database_url_sync,
    poolclass=pool.QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.debug
)

# Асинхронний движок для API
async_engine = create_async_engine(
    settings.database_url_async,
    poolclass=pool.QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.debug
)

# Сесії
SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


# Dependency для FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency для отримання асинхронної сесії бази даних
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db() -> Session:
    """
    Отримання синхронної сесії бази даних
    """
    return SyncSessionLocal()


# Функції для управління базою даних
async def create_tables():
    """
    Створення всіх таблиць (для розробки)
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")


async def drop_tables():
    """
    Видалення всіх таблиць (для розробки)
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Database tables dropped")


async def init_db():
    """
    Ініціалізація бази даних
    """
    try:
        # Перевіряємо підключення
        async with async_engine.begin() as conn:
            await conn.execute("SELECT 1")
        
        logger.info("Database connection established")
        
        # Створюємо таблиці якщо їх немає
        if settings.is_development:
            await create_tables()
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def close_db():
    """
    Закриття підключення до бази даних
    """
    await async_engine.dispose()
    sync_engine.dispose()
    logger.info("Database connections closed")


# Утиліти для роботи з базою даних
class DatabaseManager:
    """
    Менеджер для роботи з базою даних
    """
    
    @staticmethod
    async def health_check() -> bool:
        """
        Перевірка здоров'я бази даних
        """
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute("SELECT 1")
                return result.scalar() == 1
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    @staticmethod
    async def get_db_info() -> dict:
        """
        Отримання інформації про базу даних
        """
        try:
            async with AsyncSessionLocal() as session:
                # Отримуємо версію PostgreSQL
                result = await session.execute("SELECT version()")
                version = result.scalar()
                
                # Отримуємо кількість активних з'єднань
                result = await session.execute(
                    "SELECT count(*) FROM pg_stat_activity WHERE state = 'active'"
                )
                active_connections = result.scalar()
                
                return {
                    "version": version,
                    "active_connections": active_connections,
                    "pool_size": async_engine.pool.size(),
                    "checked_in": async_engine.pool.checkedin(),
                    "checked_out": async_engine.pool.checkedout()
                }
        except Exception as e:
            logger.error(f"Failed to get database info: {e}")
            return {"error": str(e)}
    
    @staticmethod
    async def cleanup_expired_transactions():
        """
        Очищення застарілих транзакцій
        """
        from datetime import datetime
        from app.models import Transaction
        from app.config import TransactionStatus
        
        try:
            async with AsyncSessionLocal() as session:
                # Знаходимо всі просрочені транзакції
                expired_transactions = await session.execute(
                    f"""
                    UPDATE transactions 
                    SET status = '{TransactionStatus.EXPIRED}', 
                        updated_at = NOW()
                    WHERE status = '{TransactionStatus.PENDING}' 
                    AND expires_at < NOW()
                    RETURNING id
                    """
                )
                
                expired_count = len(expired_transactions.fetchall())
                await session.commit()
                
                if expired_count > 0:
                    logger.info(f"Expired {expired_count} transactions")
                
                return expired_count
                
        except Exception as e:
            logger.error(f"Failed to cleanup expired transactions: {e}")
            return 0


# Тестове підключення
async def test_connection():
    """
    Тестування підключення до бази даних
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute("SELECT 'Database connection successful' as message")
            message = result.scalar()
            print(f"✅ {message}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


# Ініціалізація при імпорті
async def startup_database():
    """
    Запуск бази даних при старті додатка
    """
    try:
        await init_db()
        
        # Перевірка здоров'я
        if await DatabaseManager.health_check():
            logger.info("Database is healthy")
        else:
            logger.warning("Database health check failed")
            
    except Exception as e:
        logger.error(f"Database startup failed: {e}")
        raise


# Для використання в FastAPI
database_manager = DatabaseManager()


if __name__ == "__main__":
    # Тестування підключення
    asyncio.run(test_connection())
