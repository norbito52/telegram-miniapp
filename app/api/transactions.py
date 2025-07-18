"""
API для транзакцій GiftRoom Marketplace
"""
from datetime import datetime, timedelta
from typing import List, Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload

from app.config import settings, TransactionStatus
from app.database import get_db
from app.models import User, Channel, Transaction, ReferralEarning
from app.schemas import (
    TransactionCreate, Transaction as TransactionSchema,
    TransactionWithDetails, BaseResponse, PaginationParams, PaginatedResponse
)
from app.api.auth import get_current_active_user
from services.ton_service import TONService
from services.escrow_service import EscrowService
from services.notification_service import NotificationService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
ton_service = TONService()
escrow_service = EscrowService()
notification_service = NotificationService()


@router.post("/", response_model=TransactionSchema)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Створення нової транзакції (покупка каналу)
    """
    try:
        # Знаходимо канал
        result = await db.execute(
            select(Channel).where(Channel.id == transaction_data.channel_id)
        )
        channel = result.scalar_one_or_none()
        
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found"
            )
        
        # Перевіряємо доступність каналу
        if not channel.can_be_bought_by(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Channel cannot be purchased"
            )
        
        # Перевіряємо що це не власник каналу
        if channel.owner_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot buy your own channel"
            )
        
        # Розраховуємо комісії
        amount = transaction_data.amount
        commission = amount * Decimal(str(settings.market_commission))
        
        # Реферальна комісія
        referral_commission = Decimal('0')
        seller_result = await db.execute(
            select(User).where(User.id == channel.owner_id)
        )
        seller = seller_result.scalar_one()
        
        if seller.referred_by:
            referral_commission = amount * Decimal(str(settings.referral_commission))
        
        # Перевіряємо баланс користувача
        total_cost = amount + commission
        if current_user.balance < total_cost:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )
        
        # Створюємо транзакцію
        transaction = Transaction(
            buyer_id=current_user.id,
            seller_id=channel.owner_id,
            channel_id=channel.id,
            amount=amount,
            commission=commission,
            referral_commission=referral_commission,
            status=TransactionStatus.PENDING,
            expires_at=datetime.utcnow() + timedelta(
                minutes=settings.transaction_timeout_minutes
            )
        )
        
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        
        # Списуємо кошти з балансу покупця (заморожуємо)
        current_user.balance -= total_cost
        await db.commit()
        
        # Створюємо ескроу
        try:
            escrow_address = await escrow_service.create_escrow(
                transaction.id,
                amount,
                current_user.id,
                seller.id
            )
            
            transaction.escrow_address = escrow_address
            await db.commit()
            
        except Exception as e:
            logger.error(f"Failed to create escrow for transaction {transaction.id}: {e}")
            # Повертаємо кошти
            current_user.balance += total_cost
            await db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create escrow"
            )
        
        # Сповіщаємо продавця
        await notification_service.send_transaction_created(transaction)
        
        logger.info(f"Transaction created: {transaction.id}")
        
        return TransactionSchema.from_orm(transaction)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create transaction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create transaction"
        )


@router.get("/", response_model=PaginatedResponse)
async def get_transactions(
    pagination: PaginationParams = Depends(),
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Отримання транзакцій користувача
    """
    try:
        # Базовий запит - транзакції де користувач покупець або продавець
        query = select(Transaction).where(
            or_(
                Transaction.buyer_id == current_user.id,
                Transaction.seller_id == current_user.id
            )
        )
        
        # Фільтр по статусу
        if status_filter:
            query = query.where(Transaction.status == status_filter)
        
        # Підрахунок загальної кількості
        from sqlalchemy import func
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Пагінація та сортування
        query = query.order_by(Transaction.created_at.desc())
        query = query.offset(pagination.offset).limit(pagination.size)
        
        # Завантажуємо з додатковими даними
        query = query.options(
            selectinload(Transaction.buyer),
            selectinload(Transaction.seller),
            selectinload(Transaction.channel)
        )
        
        result = await db.execute(query)
        transactions = result.scalars().all()
        
        return PaginatedResponse(
            success=True,
            total=total,
            page=pagination.page,
            size=pagination.size,
            data=[TransactionSchema.from_orm(t) for t in transactions]
        )
        
    except Exception as e:
        logger.error(f"Failed to get transactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve transactions"
        )


@router.get("/{transaction_id}", response_model=TransactionWithDetails)
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Отримання детальної інформації про транзакцію
    """
    try:
        # Знаходимо транзакцію з додатковими даними
        query = select(Transaction).where(Transaction.id == transaction_id).options(
            selectinload(Transaction.buyer),
            selectinload(Transaction.seller),
            selectinload(Transaction.channel).selectinload(Channel.gifts)
        )
        result = await db.execute(query)
        transaction = result.scalar_one_or_none()
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Перевіряємо права доступу
        if transaction.buyer_id != current_user.id and transaction.seller_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return TransactionWithDetails.from_orm(transaction)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get transaction {transaction_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve transaction"
        )


@router.post("/{transaction_id}/complete", response_model=BaseResponse)
async def complete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Завершення транзакції (підтвердження передачі каналу)
    """
    try:
        # Знаходимо транзакцію
        result = await db.execute(
            select(Transaction).where(Transaction.id == transaction_id)
        )
        transaction = result.scalar_one_or_none()
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Перевіряємо що це продавець
        if transaction.seller_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only seller can complete transaction"
            )
        
        # Перевіряємо статус
        if transaction.status != TransactionStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction is not pending"
            )
        
        # Перевіряємо чи не закінчився час
        if transaction.is_expired:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction has expired"
            )
        
        # Перевіряємо передачу прав через Telegram API
        from services.telegram_service import get_telegram_service
        telegram_service = get_telegram_service()
        
        channel_transferred = await telegram_service.verify_channel_ownership_transfer(
            transaction.channel.telegram_channel_id,
            transaction.buyer_id
        )
        
        if not channel_transferred:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Channel ownership has not been transferred yet"
            )
        
        # Завершуємо транзакцію через ескроу сервіс
        success = await escrow_service.complete_transaction(transaction_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to complete transaction"
            )
        
        return BaseResponse(
            success=True,
            message="Transaction completed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to complete transaction {transaction_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete transaction"
        )


@router.post("/{transaction_id}/cancel", response_model=BaseResponse)
async def cancel_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Скасування транзакції
    """
    try:
        # Знаходимо транзакцію
        result = await db.execute(
            select(Transaction).where(Transaction.id == transaction_id)
        )
        transaction = result.scalar_one_or_none()
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Перевіряємо права (покупець або продавець можуть скасувати)
        if transaction.buyer_id != current_user.id and transaction.seller_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Перевіряємо статус
        if transaction.status != TransactionStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction cannot be cancelled"
            )
        
        # Скасовуємо через ескроу сервіс
        reason = f"Cancelled by {'seller' if transaction.seller_id == current_user.id else 'buyer'}"
        success = await escrow_service.cancel_transaction(transaction_id, reason)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to cancel transaction"
            )
        
        return BaseResponse(
            success=True,
            message="Transaction cancelled successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cancel transaction {transaction_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel transaction"
        )


@router.get("/active/count", response_model=dict)
async def get_active_transactions_count(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Кількість активних транзакцій користувача
    """
    try:
        # Підраховуємо активні транзакції
        from sqlalchemy import func
        
        # Як покупець
        buyer_count = await db.execute(
            select(func.count()).where(
                and_(
                    Transaction.buyer_id == current_user.id,
                    Transaction.status == TransactionStatus.PENDING
                )
            )
        )
        
        # Як продавець
        seller_count = await db.execute(
            select(func.count()).where(
                and_(
                    Transaction.seller_id == current_user.id,
                    Transaction.status == TransactionStatus.PENDING
                )
            )
        )
        
        return {
            "as_buyer": buyer_count.scalar(),
            "as_seller": seller_count.scalar(),
            "total": buyer_count.scalar() + seller_count.scalar()
        }
        
    except Exception as e:
        logger.error(f"Failed to get active transactions count: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get transactions count"
        )


@router.get("/stats/summary", response_model=dict)
async def get_transaction_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Статистика транзакцій користувача
    """
    try:
        from sqlalchemy import func
        
        # Статистика як покупець
        buyer_stats = await db.execute(
            select(
                func.count(Transaction.id).label('count'),
                func.coalesce(func.sum(Transaction.amount), 0).label('total_amount')
            ).where(
                and_(
                    Transaction.buyer_id == current_user.id,
                    Transaction.status == TransactionStatus.COMPLETED
                )
            )
        )
        buyer_result = buyer_stats.first()
        
        # Статистика як продавець
        seller_stats = await db.execute(
            select(
                func.count(Transaction.id).label('count'),
                func.coalesce(func.sum(Transaction.amount - Transaction.commission - Transaction.referral_commission), 0).label('total_amount')
            ).where(
                and_(
                    Transaction.seller_id == current_user.id,
                    Transaction.status == TransactionStatus.COMPLETED
                )
            )
        )
        seller_result = seller_stats.first()
        
        return {
            "as_buyer": {
                "transactions": buyer_result.count,
                "total_spent": float(buyer_result.total_amount)
            },
            "as_seller": {
                "transactions": seller_result.count,
                "total_earned": float(seller_result.total_amount)
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get transaction stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get transaction stats"
        )
