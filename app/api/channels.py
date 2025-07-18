"""
API для роботи з каналами GiftRoom Marketplace
"""
from typing import List, Optional, Dict, Any
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.config import settings, ChannelStatus
from app.database import get_db
from app.models import User, Channel, ChannelGift, Transaction
from app.schemas import (
    ChannelCreate, ChannelUpdate, Channel as ChannelSchema,
    ChannelListItem, ChannelFilters, PaginationParams, PaginatedResponse,
    BaseResponse, ErrorResponse
)
from app.api.auth import get_current_active_user
from services.telegram_service import TelegramService
from services.gift_parser import GiftParser
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
telegram_service = TelegramService()
gift_parser = GiftParser()


@router.get("/", response_model=PaginatedResponse)
async def get_channels(
    pagination: PaginationParams = Depends(),
    filters: ChannelFilters = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Отримання списку каналів з фільтрами та пагінацією
    """
    try:
        # Базовий запит
        query = select(Channel).where(
            and_(
                Channel.status == ChannelStatus.ACTIVE,
                Channel.bot_is_admin == True
            )
        )
        
        # Додаємо фільтри
        if filters.min_price:
            query = query.where(Channel.price >= filters.min_price)
        
        if filters.max_price:
            query = query.where(Channel.price <= filters.max_price)
        
        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.where(
                or_(
                    Channel.channel_username.ilike(search_term),
                    Channel.channel_title.ilike(search_term),
                    Channel.channel_description.ilike(search_term)
                )
            )
        
        # Фільтр по подарунках
        if filters.gift_ids:
            query = query.join(ChannelGift).where(
                ChannelGift.gift_id.in_(filters.gift_ids)
            )
        
        # Підрахунок загальної кількості
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Сортування
        if filters.sort_by == "price":
            if filters.sort_order == "asc":
                query = query.order_by(Channel.price.asc())
            else:
                query = query.order_by(Channel.price.desc())
        elif filters.sort_by == "gifts":
            # Сортування по кількості подарунків
            query = query.outerjoin(ChannelGift).group_by(Channel.id)
            if filters.sort_order == "asc":
                query = query.order_by(func.sum(ChannelGift.count).asc())
            else:
                query = query.order_by(func.sum(ChannelGift.count).desc())
        else:
            # За замовчуванням сортування по даті створення
            if filters.sort_order == "asc":
                query = query.order_by(Channel.created_at.asc())
            else:
                query = query.order_by(Channel.created_at.desc())
        
        # Пагінація
        query = query.offset(pagination.offset).limit(pagination.size)
        
        # Завантажуємо з подарунками
        query = query.options(selectinload(Channel.gifts))
        
        # Виконуємо запит
        result = await db.execute(query)
        channels = result.scalars().all()
        
        # Формуємо відповідь
        channel_items = []
        for channel in channels:
            # Знаходимо основний подарунок (з найбільшою кількістю)
            main_gift = None
            if channel.gifts:
                main_gift = max(channel.gifts, key=lambda g: g.count)
            
            channel_item = ChannelListItem(
                id=channel.id,
                display_name=channel.display_name,
                price=channel.price,
                total_gifts=channel.total_gifts,
                unique_gifts=channel.unique_gifts,
                status=channel.status,
                created_at=channel.created_at,
                main_gift=main_gift
            )
            channel_items.append(channel_item)
        
        return PaginatedResponse(
            success=True,
            total=total,
            page=pagination.page,
            size=pagination.size,
            data=channel_items
        )
        
    except Exception as e:
        logger.error(f"Failed to get channels: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve channels"
        )


@router.get("/{channel_id}", response_model=ChannelSchema)
async def get_channel(
    channel_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Отримання детальної інформації про канал
    """
    try:
        # Знаходимо канал з подарунками
        query = select(Channel).where(Channel.id == channel_id).options(
            selectinload(Channel.gifts)
        )
        result = await db.execute(query)
        channel = result.scalar_one_or_none()
        
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found"
            )
        
        # Перевіряємо доступність
        if channel.status != ChannelStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Channel is not available"
            )
        
        # Збільшуємо лічильник переглядів
        channel.views_count += 1
        await db.commit()
        
        return ChannelSchema.from_orm(channel)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get channel {channel_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve channel"
        )


@router.post("/", response_model=ChannelSchema)
async def create_channel(
    channel_data: ChannelCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Створення нового каналу
    """
    try:
        # Перевіряємо чи може користувач створити канал
        if not current_user.can_create_channel():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot create channels"
            )
        
        # Перевіряємо чи канал вже існує
        existing_channel = await db.execute(
            select(Channel).where(
                Channel.telegram_channel_id == channel_data.telegram_channel_id
            )
        )
        if existing_channel.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Channel already exists"
            )
        
        # Отримуємо інформацію про канал з Telegram
        try:
            channel_info = await telegram_service.get_channel_info(
                channel_data.telegram_channel_id
            )
        except Exception as e:
            logger.error(f"Failed to get channel info: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to access channel. Make sure the bot is admin."
            )
        
        # Перевіряємо чи бот є адміністратором
        is_admin = await telegram_service.check_bot_is_admin(
            channel_data.telegram_channel_id
        )
        
        if not is_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bot must be admin of the channel"
            )
        
        # Створюємо канал
        channel = Channel(
            telegram_channel_id=channel_data.telegram_channel_id,
            channel_username=channel_info.get('username'),
            channel_title=channel_info.get('title'),
            channel_description=channel_data.channel_description,
            owner_id=current_user.id,
            price=channel_data.price,
            status=ChannelStatus.ACTIVE,
            bot_is_admin=is_admin,
            subscribers_count=channel_info.get('member_count', 0)
        )
        
        db.add(channel)
        await db.commit()
        await db.refresh(channel)
        
        # Парсимо подарунки з каналу
        try:
            gifts = await gift_parser.parse_channel_gifts(
                channel_data.telegram_channel_id
            )
            
            # Додаємо подарунки до БД
            for gift_data in gifts:
                gift = ChannelGift(
                    channel_id=channel.id,
                    gift_id=gift_data['id'],
                    gift_name=gift_data['name'],
                    gift_image_url=gift_data.get('image_url'),
                    count=gift_data['count']
                )
                db.add(gift)
            
            await db.commit()
            
        except Exception as e:
            logger.error(f"Failed to parse gifts for channel {channel.id}: {e}")
            # Не падаємо, просто логуємо помилку
        
        # Завантажуємо канал з подарунками
        await db.refresh(channel)
        query = select(Channel).where(Channel.id == channel.id).options(
            selectinload(Channel.gifts)
        )
        result = await db.execute(query)
        channel = result.scalar_one()
        
        logger.info(f"Channel created: {channel.id} by user {current_user.id}")
        
        return ChannelSchema.from_orm(channel)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create channel: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create channel"
        )


@router.patch("/{channel_id}", response_model=ChannelSchema)
async def update_channel(
    channel_id: int,
    channel_update: ChannelUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Оновлення каналу
    """
    try:
        # Знаходимо канал
        result = await db.execute(
            select(Channel).where(Channel.id == channel_id)
        )
        channel = result.scalar_one_or_none()
        
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found"
            )
        
        # Перевіряємо права
        if channel.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't own this channel"
            )
        
        # Оновлюємо дані
        update_data = channel_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(channel, field, value)
        
        await db.commit()
        await db.refresh(channel)
        
        # Завантажуємо з подарунками
        query = select(Channel).where(Channel.id == channel_id).options(
            selectinload(Channel.gifts)
        )
        result = await db.execute(query)
        channel = result.scalar_one()
        
        logger.info(f"Channel updated: {channel.id} by user {current_user.id}")
        
        return ChannelSchema.from_orm(channel)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update channel {channel_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update channel"
        )


@router.delete("/{channel_id}", response_model=BaseResponse)
async def delete_channel(
    channel_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Видалення каналу
    """
    try:
        # Знаходимо канал
        result = await db.execute(
            select(Channel).where(Channel.id == channel_id)
        )
        channel = result.scalar_one_or_none()
        
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found"
            )
        
        # Перевіряємо права
        if channel.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't own this channel"
            )
        
        # Перевіряємо активні транзакції
        active_transactions = await db.execute(
            select(Transaction).where(
                and_(
                    Transaction.channel_id == channel_id,
                    Transaction.status == "pending"
                )
            )
        )
        
        if active_transactions.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete channel with active transactions"
            )
        
        # Видаляємо канал (подарунки видаляться каскадно)
        await db.delete(channel)
        await db.commit()
        
        logger.info(f"Channel deleted: {channel_id} by user {current_user.id}")
        
        return BaseResponse(
            success=True,
            message="Channel deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete channel {channel_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete channel"
        )


@router.get("/my/channels", response_model=List[ChannelSchema])
async def get_my_channels(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Отримання каналів поточного користувача
    """
    try:
        query = select(Channel).where(
            Channel.owner_id == current_user.id
        ).options(
            selectinload(Channel.gifts)
        ).order_by(Channel.created_at.desc())
        
        result = await db.execute(query)
        channels = result.scalars().all()
        
        return [ChannelSchema.from_orm(channel) for channel in channels]
        
    except Exception as e:
        logger.error(f"Failed to get user channels: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve your channels"
        )


@router.post("/{channel_id}/refresh-gifts", response_model=BaseResponse)
async def refresh_channel_gifts(
    channel_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Оновлення подарунків каналу
    """
    try:
        # Знаходимо канал
        result = await db.execute(
            select(Channel).where(Channel.id == channel_id)
        )
        channel = result.scalar_one_or_none()
        
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found"
            )
        
        # Перевіряємо права
        if channel.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't own this channel"
            )
        
        # Парсимо подарунки знову
        gifts = await gift_parser.parse_channel_gifts(
            channel.telegram_channel_id
        )
        
        # Оновлюємо подарунки
        await db.execute(
            f"DELETE FROM channel_gifts WHERE channel_id = {channel_id}"
        )
        
        for gift_data in gifts:
            gift = ChannelGift(
                channel_id=channel.id,
                gift_id=gift_data['id'],
                gift_name=gift_data['name'],
                gift_image_url=gift_data.get('image_url'),
                count=gift_data['count']
            )
            db.add(gift)
        
        await db.commit()
        
        logger.info(f"Gifts refreshed for channel {channel_id}")
        
        return BaseResponse(
            success=True,
            message="Gifts refreshed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to refresh gifts for channel {channel_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh gifts"
        )
