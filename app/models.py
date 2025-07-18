"""
Моделі бази даних для GiftRoom Marketplace
"""
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, BigInteger, String, Text, Decimal as SQLDecimal,
    DateTime, Boolean, ForeignKey, Index, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from app.config import settings, TransactionStatus, ChannelStatus

Base = declarative_base()


class TimestampMixin:
    """Міксин для додавання полів created_at та updated_at"""
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class User(Base, TimestampMixin):
    """Модель користувача"""
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    
    # Гаманець та баланс
    ton_wallet = Column(String(255), nullable=True)
    balance = Column(SQLDecimal(20, 8), default=Decimal('0'), nullable=False)
    
    # Реферальна система
    referral_code = Column(String(50), unique=True, nullable=True, index=True)
    referred_by = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    
    # Статистика
    total_bought = Column(Integer, default=0, nullable=False)
    total_sold = Column(Integer, default=0, nullable=False)
    total_volume = Column(SQLDecimal(20, 8), default=Decimal('0'), nullable=False)
    
    # Активність
    last_activity = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True, nullable=False)
    is_banned = Column(Boolean, default=False, nullable=False)
    
    # Зв'язки
    referrer = relationship("User", remote_side=[id], backref="referrals")
    owned_channels = relationship("Channel", back_populates="owner")
    bought_transactions = relationship("Transaction", foreign_keys="Transaction.buyer_id", back_populates="buyer")
    sold_transactions = relationship("Transaction", foreign_keys="Transaction.seller_id", back_populates="seller")
    referral_earnings = relationship("ReferralEarning", foreign_keys="ReferralEarning.referrer_id", back_populates="referrer")
    
    # Індекси
    __table_args__ = (
        Index('idx_user_telegram_id', 'telegram_id'),
        Index('idx_user_referral_code', 'referral_code'),
        Index('idx_user_activity', 'last_activity'),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"
    
    @property
    def display_name(self) -> str:
        """Відображуване ім'я користувача"""
        if self.username:
            return f"@{self.username}"
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or f"User {self.id}"
    
    def can_create_channel(self) -> bool:
        """Чи може користувач створити канал"""
        return self.is_active and not self.is_banned
    
    def update_activity(self):
        """Оновити час останньої активності"""
        self.last_activity = func.now()


class Channel(Base, TimestampMixin):
    """Модель каналу"""
    __tablename__ = "channels"
    
    id = Column(BigInteger, primary_key=True, index=True)
    telegram_channel_id = Column(BigInteger, unique=True, nullable=False, index=True)
    channel_username = Column(String(255), nullable=True)
    channel_title = Column(String(255), nullable=True)
    channel_description = Column(Text, nullable=True)
    
    # Власник
    owner_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    
    # Ціна та статус
    price = Column(SQLDecimal(20, 8), nullable=False)
    status = Column(String(50), default=ChannelStatus.ACTIVE, nullable=False)
    
    # Верифікація
    bot_is_admin = Column(Boolean, default=False, nullable=False)
    verification_date = Column(DateTime, nullable=True)
    
    # Статистика
    views_count = Column(Integer, default=0, nullable=False)
    subscribers_count = Column(Integer, default=0, nullable=False)
    posts_count = Column(Integer, default=0, nullable=False)
    
    # Зв'язки
    owner = relationship("User", back_populates="owned_channels")
    gifts = relationship("ChannelGift", back_populates="channel", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="channel")
    
    # Індекси
    __table_args__ = (
        Index('idx_channel_telegram_id', 'telegram_channel_id'),
        Index('idx_channel_owner', 'owner_id'),
        Index('idx_channel_status', 'status'),
        Index('idx_channel_price', 'price'),
        CheckConstraint('price > 0', name='check_positive_price'),
    )
    
    def __repr__(self):
        return f"<Channel(id={self.id}, username={self.channel_username}, price={self.price})>"
    
    @property
    def display_name(self) -> str:
        """Відображувана назва каналу"""
        if self.channel_username:
            return f"@{self.channel_username}"
        return self.channel_title or f"Channel {self.id}"
    
    @property
    def total_gifts(self) -> int:
        """Загальна кількість подарунків"""
        return sum(gift.count for gift in self.gifts)
    
    @property
    def unique_gifts(self) -> int:
        """Кількість унікальних подарунків"""
        return len(self.gifts)
    
    def is_available(self) -> bool:
        """Чи доступний канал для покупки"""
        return self.status == ChannelStatus.ACTIVE and self.bot_is_admin
    
    def can_be_bought_by(self, user_id: int) -> bool:
        """Чи може користувач купити цей канал"""
        return self.is_available() and self.owner_id != user_id


class ChannelGift(Base, TimestampMixin):
    """Модель подарунку в каналі"""
    __tablename__ = "channel_gifts"
    
    id = Column(BigInteger, primary_key=True, index=True)
    channel_id = Column(BigInteger, ForeignKey("channels.id"), nullable=False)
    gift_id = Column(Integer, nullable=False)
    gift_name = Column(String(255), nullable=False)
    gift_image_url = Column(Text, nullable=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime, default=func.now())
    
    # Зв'язки
    channel = relationship("Channel", back_populates="gifts")
    
    # Індекси
    __table_args__ = (
        Index('idx_gift_channel', 'channel_id'),
        Index('idx_gift_id', 'gift_id'),
        Index('idx_gift_name', 'gift_name'),
        UniqueConstraint('channel_id', 'gift_id', name='uq_channel_gift'),
        CheckConstraint('count >= 0', name='check_non_negative_count'),
    )
    
    def __repr__(self):
        return f"<ChannelGift(id={self.id}, gift_name={self.gift_name}, count={self.count})>"


class Transaction(Base, TimestampMixin):
    """Модель транзакції"""
    __tablename__ = "transactions"
    
    id = Column(BigInteger, primary_key=True, index=True)
    
    # Учасники
    buyer_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    seller_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    channel_id = Column(BigInteger, ForeignKey("channels.id"), nullable=False)
    
    # Фінанси
    amount = Column(SQLDecimal(20, 8), nullable=False)
    commission = Column(SQLDecimal(20, 8), nullable=False)
    referral_commission = Column(SQLDecimal(20, 8), default=Decimal('0'))
    
    # Статус та час
    status = Column(String(50), default=TransactionStatus.PENDING, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Блокчейн
    escrow_address = Column(String(255), nullable=True)
    ton_transaction_hash = Column(String(255), nullable=True)
    
    # Зв'язки
    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="bought_transactions")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="sold_transactions")
    channel = relationship("Channel", back_populates="transactions")
    referral_earnings = relationship("ReferralEarning", back_populates="transaction")
    
    # Індекси
    __table_args__ = (
        Index('idx_transaction_buyer', 'buyer_id'),
        Index('idx_transaction_seller', 'seller_id'),
        Index('idx_transaction_channel', 'channel_id'),
        Index('idx_transaction_status', 'status'),
        Index('idx_transaction_expires', 'expires_at'),
        CheckConstraint('amount > 0', name='check_positive_amount'),
        CheckConstraint('commission >= 0', name='check_non_negative_commission'),
        CheckConstraint('buyer_id != seller_id', name='check_different_users'),
    )
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, status={self.status})>"
    
    @property
    def seller_amount(self) -> Decimal:
        """Сума, яку отримає продавець"""
        return self.amount - self.commission - self.referral_commission
    
    @property
    def is_expired(self) -> bool:
        """Чи закінчився час транзакції"""
        return datetime.utcnow() > self.expires_at
    
    @property
    def time_left(self) -> Optional[timedelta]:
        """Скільки часу залишилось"""
        if self.status != TransactionStatus.PENDING:
            return None
        remaining = self.expires_at - datetime.utcnow()
        return remaining if remaining.total_seconds() > 0 else timedelta(0)
    
    def can_be_completed(self) -> bool:
        """Чи може транзакція бути завершена"""
        return self.status == TransactionStatus.PENDING and not self.is_expired
    
    def can_be_cancelled(self) -> bool:
        """Чи може транзакція бути скасована"""
        return self.status == TransactionStatus.PENDING


class ReferralEarning(Base, TimestampMixin):
    """Модель реферальних нарахувань"""
    __tablename__ = "referral_earnings"
    
    id = Column(BigInteger, primary_key=True, index=True)
    referrer_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    referred_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    transaction_id = Column(BigInteger, ForeignKey("transactions.id"), nullable=False)
    
    amount = Column(SQLDecimal(20, 8), nullable=False)
    status = Column(String(50), default="pending", nullable=False)  # pending, paid
    paid_at = Column(DateTime, nullable=True)
    
    # Зв'язки
    referrer = relationship("User", foreign_keys=[referrer_id], back_populates="referral_earnings")
    referred = relationship("User", foreign_keys=[referred_id])
    transaction = relationship("Transaction", back_populates="referral_earnings")
    
    # Індекси
    __table_args__ = (
        Index('idx_referral_referrer', 'referrer_id'),
        Index('idx_referral_referred', 'referred_id'),
        Index('idx_referral_transaction', 'transaction_id'),
        Index('idx_referral_status', 'status'),
        CheckConstraint('amount > 0', name='check_positive_referral_amount'),
        CheckConstraint('referrer_id != referred_id', name='check_different_referral_users'),
    )
    
    def __repr__(self):
        return f"<ReferralEarning(id={self.id}, amount={self.amount}, status={self.status})>"


class SystemSettings(Base, TimestampMixin):
    """Модель системних налаштувань"""
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<SystemSettings(key={self.key}, value={self.value})>"
