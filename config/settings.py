"""
🎁 GiftRoom Market - Налаштування додатка
Централізоване керування конфігурацією через змінні середовища
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Основні налаштування додатка"""
    
    # Telegram Bot
    bot_token: str = Field(..., env="BOT_TOKEN")
    bot_username: str = Field("giftroom_market_bot", env="BOT_USERNAME")
    
    # Web Application
    webapp_url: str = Field(..., env="WEBAPP_URL")
    port: int = Field(8000, env="PORT")
    debug: bool = Field(False, env="DEBUG")
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    
    # TON Blockchain
    ton_connect_manifest_url: str = Field(..., env="TON_CONNECT_MANIFEST_URL")
    ton_api_key: Optional[str] = Field(None, env="TON_API_KEY")
    ton_mainnet: bool = Field(True, env="TON_MAINNET")
    
    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Admin Configuration
    admin_ids: List[int] = Field(default_factory=list)
    super_admin_id: Optional[int] = Field(None, env="SUPER_ADMIN_ID")
    
    # Commission & Fees
    marketplace_commission: float = Field(0.025, env="MARKETPLACE_COMMISSION")  # 2.5%
    referral_commission: float = Field(0.025, env="REFERRAL_COMMISSION")        # 2.5%
    
    # Escrow Settings
    deal_timeout_minutes: int = Field(60, env="DEAL_TIMEOUT_MINUTES")
    min_withdrawal_amount: float = Field(0.1, env="MIN_WITHDRAWAL_AMOUNT")
    
    # External Services
    redis_url: Optional[str] = Field(None, env="REDIS_URL")
    webhook_url: Optional[str] = Field(None, env="WEBHOOK_URL")
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("logs/giftroom.log", env="LOG_FILE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Парсимо ADMIN_IDS зі строки в список
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        if admin_ids_str:
            try:
                self.admin_ids = [int(id_.strip()) for id_ in admin_ids_str.split(",") if id_.strip()]
            except ValueError:
                self.admin_ids = []
    
    @property
    def is_production(self) -> bool:
        """Перевіряємо чи це продакшн оточення"""
        return not self.debug and "localhost" not in self.webapp_url
    
    @property
    def database_is_postgres(self) -> bool:
        """Перевіряємо чи використовується PostgreSQL"""
        return self.database_url.startswith("postgresql://")
    
    @property
    def ton_network(self) -> str:
        """Повертаємо мережу TON"""
        return "mainnet" if self.ton_mainnet else "testnet"


class TONSettings:
    """Налаштування для TON Connect"""
    
    # TON Connect Manifest
    MANIFEST = {
        "url": "",  # Буде заповнено з settings.webapp_url
        "name": "GiftRoom Market",
        "iconUrl": "",  # Буде заповнено з settings.webapp_url + "/static/icon.png"
        "termsOfUseUrl": "",  # settings.webapp_url + "/terms"
        "privacyPolicyUrl": "",  # settings.webapp_url + "/privacy"
    }
    
    # Підтримувані кошельки
    SUPPORTED_WALLETS = [
        "tonkeeper",
        "tonhub", 
        "dewallet",
        "xtonwallet",
        "tonwallet"
    ]
    
    # TON Connect параметри
    CONNECT_REQUEST_PAYLOAD = {
        "manifestUrl": "",  # Буде заповнено
        "items": [
            {
                "name": "ton_addr"
            },
            {
                "name": "ton_proof",
                "payload": ""  # Буде генеровано
            }
        ]
    }


class DatabaseSettings:
    """Налаштування бази даних"""
    
    # SQLite налаштування для розробки
    SQLITE_CONFIG = {
        "echo": False,
        "pool_pre_ping": True,
        "connect_args": {"check_same_thread": False}
    }
    
    # PostgreSQL налаштування для продакшну
    POSTGRES_CONFIG = {
        "echo": False,
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
        "pool_recycle": 3600
    }


# Глобальний екземпляр налаштувань
settings = Settings()

# Оновлюємо TON налаштування з основними
TONSettings.MANIFEST["url"] = settings.webapp_url
TONSettings.MANIFEST["iconUrl"] = f"{settings.webapp_url}/static/images/icon.png"
TONSettings.MANIFEST["termsOfUseUrl"] = f"{settings.webapp_url}/terms"
TONSettings.MANIFEST["privacyPolicyUrl"] = f"{settings.webapp_url}/privacy"
TONSettings.CONNECT_REQUEST_PAYLOAD["manifestUrl"] = settings.ton_connect_manifest_url
