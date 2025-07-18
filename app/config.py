"""
Конфігурація GiftRoom Marketplace
"""
import os
from typing import List, Optional
from pydantic import BaseSettings, validator
from functools import lru_cache


class Settings(BaseSettings):
    """Налаштування додатка"""
    
    # Basic App Settings
    app_name: str = "GiftRoom Marketplace"
    app_version: str = "1.0.0"
    debug: bool = False
    testing: bool = False
    environment: str = "development"
    
    # Database
    database_url: str
    database_url_test: Optional[str] = None
    
    # Telegram Bot
    bot_token: str
    webapp_url: str
    bot_webhook_url: Optional[str] = None
    telegram_api_id: Optional[int] = None
    telegram_api_hash: Optional[str] = None
    
    # TON Blockchain
    ton_network: str = "testnet"
    ton_api_key: Optional[str] = None
    ton_rpc_url: str = "https://testnet.toncenter.com/api/v2/jsonRPC"
    ton_wallet_seed: Optional[str] = None
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Business Logic
    market_commission: float = 0.05  # 5%
    referral_commission: float = 0.025  # 2.5%
    transaction_timeout_minutes: int = 60
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000"]
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    
    @validator('allowed_origins', pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [item.strip() for item in v.split(",")]
        return v
    
    @validator('market_commission', 'referral_commission')
    def validate_commission(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Commission must be between 0 and 1')
        return v
    
    @validator('bot_token')
    def validate_bot_token(cls, v):
        if not v or len(v) < 10:
            raise ValueError('Bot token is required and must be valid')
        return v
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        if not v or len(v) < 32:
            raise ValueError('Secret key must be at least 32 characters long')
        return v
    
    @property
    def is_production(self) -> bool:
        """Чи працює додаток у продакшені"""
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        """Чи працює додаток у розробці"""
        return self.environment == "development"
    
    @property
    def is_testing(self) -> bool:
        """Чи працює додаток у тестуванні"""
        return self.testing
    
    @property
    def database_url_sync(self) -> str:
        """Синхронний URL для бази даних"""
        return self.database_url.replace("postgresql://", "postgresql+psycopg2://")
    
    @property
    def database_url_async(self) -> str:
        """Асинхронний URL для бази даних"""
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Константи для статусів
class TransactionStatus:
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    EXPIRED = "expired"


class ChannelStatus:
    ACTIVE = "active"
    SOLD = "sold"
    HIDDEN = "hidden"
    PENDING = "pending"
    REJECTED = "rejected"


class UserRole:
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class GiftCategories:
    """Категорії подарунків"""
    FASHION = "fashion"
    ANIMALS = "animals"
    TECH = "tech"
    FOOD = "food"
    ENTERTAINMENT = "entertainment"
    SPORTS = "sports"
    MISC = "misc"


# Mapping подарунків за ID
GIFT_MAPPING = {
    1: {"name": "HEELS", "category": GiftCategories.FASHION},
    2: {"name": "BUTTON", "category": GiftCategories.MISC},
    3: {"name": "CATS", "category": GiftCategories.ANIMALS},
    4: {"name": "SOCKS", "category": GiftCategories.FASHION},
    5: {"name": "BICEPS", "category": GiftCategories.SPORTS},
    6: {"name": "LAMP", "category": GiftCategories.TECH},
    7: {"name": "BOUQUET", "category": GiftCategories.MISC},
    8: {"name": "CUPCAKE", "category": GiftCategories.FOOD},
    9: {"name": "MARCH 8", "category": GiftCategories.MISC},
    10: {"name": "DYSON", "category": GiftCategories.TECH},
    11: {"name": "BOILER", "category": GiftCategories.TECH},
    12: {"name": "CLOVER", "category": GiftCategories.MISC},
    13: {"name": "AMULET", "category": GiftCategories.MISC},
    14: {"name": "MOSQUE", "category": GiftCategories.MISC},
    15: {"name": "DOSHIK", "category": GiftCategories.FOOD},
    16: {"name": "POOP", "category": GiftCategories.ENTERTAINMENT},
    17: {"name": "MONKEY", "category": GiftCategories.ANIMALS},
    18: {"name": "BRICK", "category": GiftCategories.TECH},
    19: {"name": "ROCKET", "category": GiftCategories.TECH},
    20: {"name": "KULICH", "category": GiftCategories.FOOD},
    21: {"name": "RABBIT", "category": GiftCategories.ANIMALS},
    22: {"name": "1 MAY", "category": GiftCategories.MISC},
    23: {"name": "MEDAL", "category": GiftCategories.SPORTS},
    24: {"name": "PIGEON", "category": GiftCategories.ANIMALS},
    25: {"name": "STAR", "category": GiftCategories.MISC},
    26: {"name": "CREAMY ICE CREAM", "category": GiftCategories.FOOD},
    27: {"name": "ESKIMO", "category": GiftCategories.MISC},
    28: {"name": "PLUMBER", "category": GiftCategories.ENTERTAINMENT},
    29: {"name": "NIPPLE", "category": GiftCategories.MISC},
    30: {"name": "EAGLE", "category": GiftCategories.ANIMALS},
    31: {"name": "STATUE", "category": GiftCategories.MISC},
    32: {"name": "TORCH", "category": GiftCategories.SPORTS},
    33: {"name": "WESTSIDE SIGN", "category": GiftCategories.ENTERTAINMENT},
    34: {"name": "LOW RIDER", "category": GiftCategories.ENTERTAINMENT},
    35: {"name": "SNOOP CIGAR", "category": GiftCategories.ENTERTAINMENT},
    36: {"name": "SWAG BAG", "category": GiftCategories.FASHION},
    37: {"name": "SNOOP DOGG", "category": GiftCategories.ENTERTAINMENT},
}


@lru_cache()
def get_settings() -> Settings:
    """Отримати налаштування додатка (з кешуванням)"""
    return Settings()


# Експортуємо налаштування для зручності
settings = get_settings()
