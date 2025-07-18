"""
API модуль для GiftRoom Marketplace
"""

from fastapi import APIRouter

# Імпорт всіх роутерів
from . import auth, channels, gifts, transactions, referrals, wallet

# Головний роутер API
api_router = APIRouter()

# Додаємо всі роутери
api_router.include_router(auth.router, prefix="/auth", tags=["Автентифікація"])
api_router.include_router(channels.router, prefix="/channels", tags=["Канали"])
api_router.include_router(gifts.router, prefix="/gifts", tags=["Подарунки"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Транзакції"])
api_router.include_router(referrals.router, prefix="/referrals", tags=["Реферали"])
api_router.include_router(wallet.router, prefix="/wallet", tags=["Гаманець"])

__all__ = ["api_router"]
