"""
Pydantic схеми для API GiftRoom Marketplace
"""
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, root_validator
from app.config import TransactionStatus, ChannelStatus


# Базові схеми
class BaseResponse(BaseModel):
    """Базова схема відповіді"""
    success: bool = True
    message: Optional[str] = None
    
    class Config:
        orm_mode = True


class PaginationParams(BaseModel):
    """Параметри пагінації"""
    page: int = Field(1, ge=1, description="Номер сторінки")
    size: int = Field(20, ge=1, le=100, description="Кількість елементів на сторінці")
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


class PaginatedResponse(BaseResponse):
    """Пагінована відповідь"""
    total: int
    page: int
    size: int
    pages: int
    
    @validator('pages', pre=True, always=True)
    def calculate_pages(cls, v, values):
        total = values.get('total', 0)
        size = values.get('size', 20)
        return (total + size - 1) // size if total > 0 else 0


# Схеми користувачів
class UserBase(BaseModel):
    """Базова схема користувача"""
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    """Створення користувача"""
    referral_code: Optional[str] = None


class UserUpdate(BaseModel):
    """Оновлення користувача"""
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    ton_wallet: Optional[str] = None


class UserProfile(UserBase):
    """Профіль користувача"""
    id: int
    balance: Decimal
    total_bought: int
    total_sold: int
    total_volume: Decimal
    referral_code: Optional[str]
    created_at: datetime
    
    @property
    def display_name(self) -> str:
        if self.username:
            return f"@{self.username}"
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or f"User {self.id}"


class UserStats(BaseModel):
    """Статистика користувача"""
    total_channels: int
    active_channels: int
    sold_channels: int
    pending_transactions: int
    completed_transactions: int
    referrals_count: int
    referral_earnings: Decimal


# Схеми подарунків
class GiftBase(BaseModel):
    """Базова схема подарунку"""
    gift_id: int
    gift_name: str
    count: int
    gift_image_url: Optional[str] = None


class GiftCreate(GiftBase):
    """Створення подарунку"""
    pass


class GiftUpdate(BaseModel):
    """Оновлення подарунку"""
    count: Optional[int] = None
    gift_image_url: Optional[str] = None


class Gift(GiftBase):
    """Повна схема подарунку"""
    id: int
    channel_id: int
    last_updated: datetime
    
    class Config:
        orm_mode = True


class GiftStats(BaseModel):
    """Статистика подарунку"""
    gift_id: int
    gift_name: str
    total_count: int
    channels_count: int
    average_price: Optional[Decimal] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None


# Схеми каналів
class ChannelBase(BaseModel):
    """Базова схема каналу"""
    channel_username: Optional[str] = None
    channel_title: Optional[str] = None
    channel_description: Optional[str] = None
    price: Decimal = Field(..., gt=0, description="Ціна повинна бути більше 0")


class ChannelCreate(ChannelBase):
    """Створення каналу"""
    telegram_channel_id: int
    
    @validator('telegram_channel_id')
    def validate_channel_id(cls, v):
        if v >= 0:
            raise ValueError('Channel ID must be negative for channels')
        return v


class ChannelUpdate(BaseModel):
    """Оновлення каналу"""
    channel_title: Optional[str] = None
    channel_description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    status: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        if v and v not in [ChannelStatus.ACTIVE, ChannelStatus.HIDDEN]:
            raise ValueError('Invalid status')
        return v


class Channel(ChannelBase):
    """Повна схема каналу"""
    id: int
    telegram_channel_id: int
    owner_id: int
    status: str
    bot_is_admin: bool
    views_count: int
    subscribers_count: int
    posts_count: int
    created_at: datetime
    gifts: List[Gift] = []
    
    @property
    def display_name(self) -> str:
        if self.channel_username:
            return f"@{self.channel_username}"
        return self.channel_title or f"Channel {self.id}"
    
    @property
    def total_gifts(self) -> int:
        return sum(gift.count for gift in self.gifts)
    
    @property
    def unique_gifts(self) -> int:
        return len(self.gifts)
    
    class Config:
        orm_mode = True


class ChannelListItem(BaseModel):
    """Канал в списку"""
    id: int
    display_name: str
    price: Decimal
    total_gifts: int
    unique_gifts: int
    status: str
    created_at: datetime
    main_gift: Optional[Gift] = None
    
    class Config:
        orm_mode = True


class ChannelFilters(BaseModel):
    """Фільтри для каналів"""
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    gift_ids: Optional[List[int]] = None
    status: Optional[str] = None
    search: Optional[str] = None
    sort_by: str = Field("created_at", description="Поле для сортування")
    sort_order: str = Field("desc", regex="^(asc|desc)$")
    
    @validator('gift_ids')
    def validate_gift_ids(cls, v):
        if v and any(not isinstance(gid, int) or gid < 1 or gid > 37 for gid in v):
            raise ValueError('Gift IDs must be between 1 and 37')
        return v


# Схеми транзакцій
class TransactionBase(BaseModel):
    """Базова схема транзакції"""
    channel_id: int
    amount: Decimal = Field(..., gt=0)


class TransactionCreate(TransactionBase):
    """Створення транзакції"""
    pass


class Transaction(TransactionBase):
    """Повна схема транзакції"""
    id: int
    buyer_id: int
    seller_id: int
    commission: Decimal
    referral_commission: Decimal
    status: str
    expires_at: datetime
    completed_at: Optional[datetime] = None
    escrow_address: Optional[str] = None
    ton_transaction_hash: Optional[str] = None
    created_at: datetime
    
    @property
    def seller_amount(self) -> Decimal:
        return self.amount - self.commission - self.referral_commission
    
    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at
    
    @property
    def time_left(self) -> Optional[timedelta]:
        if self.status != TransactionStatus.PENDING:
            return None
        remaining = self.expires_at - datetime.utcnow()
        return remaining if remaining.total_seconds() > 0 else timedelta(0)
    
    class Config:
        orm_mode = True


class TransactionWithDetails(Transaction):
    """Транзакція з деталями"""
    buyer: UserProfile
    seller: UserProfile
    channel: Channel


# Схеми для ескроу
class EscrowCreate(BaseModel):
    """Створення ескроу"""
    transaction_id: int
    amount: Decimal


class EscrowStatus(BaseModel):
    """Статус ескроу"""
    address: str
    amount: Decimal
    status: str
    created_at: datetime
    expires_at: datetime


# Схеми реферальної системи
class ReferralStats(BaseModel):
    """Статистика рефералів"""
    referrals_count: int
    total_earnings: Decimal
    pending_earnings: Decimal
    paid_earnings: Decimal
    
    class Config:
        orm_mode = True


class ReferralEarning(BaseModel):
    """Реферальне нарахування"""
    id: int
    amount: Decimal
    status: str
    created_at: datetime
    referred_user: UserProfile
    transaction_id: int
    
    class Config:
        orm_mode = True


class ReferralLink(BaseModel):
    """Реферальне посилання"""
    code: str
    link: str
    clicks: int = 0
    registrations: int = 0


# Схеми для TON
class WalletConnect(BaseModel):
    """Підключення гаманця"""
    wallet_address: str
    proof: Dict[str, Any]
    
    @validator('wallet_address')
    def validate_wallet_address(cls, v):
        # Базова валідація TON адреси
        if not v or len(v) < 48:
            raise ValueError('Invalid TON wallet address')
        return v


class WalletBalance(BaseModel):
    """Баланс гаманця"""
    address: str
    balance: Decimal
    last_updated: datetime


class PaymentRequest(BaseModel):
    """Запит на оплату"""
    amount: Decimal = Field(..., gt=0)
    memo: Optional[str] = None


# Схеми для бота
class BotUser(BaseModel):
    """Користувач бота"""
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None


class WebAppInitData(BaseModel):
    """Дані ініціалізації Web App"""
    user: BotUser
    chat_instance: Optional[str] = None
    chat_type: Optional[str] = None
    auth_date: int
    hash: str


# Системні схеми
class SystemHealth(BaseModel):
    """Здоров'я системи"""
    status: str
    version: str
    database: str
    environment: str
    uptime: Optional[str] = None


class SystemStats(BaseModel):
    """Статистика системи"""
    total_users: int
    total_channels: int
    total_transactions: int
    total_volume: Decimal
    active_transactions: int
    
    class Config:
        orm_mode = True


# Схеми помилок
class ErrorResponse(BaseModel):
    """Схема помилки"""
    success: bool = False
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ValidationError(ErrorResponse):
    """Помилка валідації"""
    error_code: str = "VALIDATION_ERROR"
    field_errors: Dict[str, List[str]]
