"""
API автентифікації для GiftRoom Marketplace
"""
import hmac
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from urllib.parse import unquote, parse_qsl
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database import get_db
from app.models import User
from app.schemas import (
    UserCreate, UserProfile, UserUpdate, BotUser, WebAppInitData, 
    BaseResponse, ErrorResponse
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()


# Утиліти для роботи з JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Створення JWT токена"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_telegram_web_app_data(init_data: str) -> Dict[str, Any]:
    """
    Верифікація даних Telegram Web App
    """
    try:
        # Парсимо дані
        parsed_data = dict(parse_qsl(init_data))
        
        # Витягуємо хеш
        received_hash = parsed_data.pop('hash', '')
        
        # Створюємо рядок для перевірки
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(parsed_data.items()))
        
        # Створюємо секретний ключ
        secret_key = hmac.new(
            "WebAppData".encode(),
            settings.bot_token.encode(),
            hashlib.sha256
        ).digest()
        
        # Перевіряємо хеш
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(calculated_hash, received_hash):
            raise ValueError("Invalid hash")
        
        # Перевіряємо час
        auth_date = int(parsed_data.get('auth_date', '0'))
        if datetime.utcnow().timestamp() - auth_date > 86400:  # 24 години
            raise ValueError("Data is too old")
        
        # Парсимо дані користувача
        user_data = json.loads(parsed_data.get('user', '{}'))
        
        return {
            'user': user_data,
            'auth_date': auth_date,
            'chat_instance': parsed_data.get('chat_instance'),
            'chat_type': parsed_data.get('chat_type')
        }
        
    except Exception as e:
        logger.error(f"Failed to verify Telegram Web App data: {e}")
        raise ValueError("Invalid Telegram Web App data")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Отримання поточного користувача з JWT токена
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        telegram_id: int = payload.get("sub")
        if telegram_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Знаходимо користувача в базі
    result = await db.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    # Оновлюємо активність
    user.update_activity()
    await db.commit()
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Отримання поточного активного користувача
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    if current_user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is banned"
        )
    
    return current_user


# API endpoints
@router.post("/telegram-auth", response_model=Dict[str, Any])
async def telegram_auth(
    init_data: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Автентифікація через Telegram Web App
    """
    try:
        # Верифікуємо дані
        verified_data = verify_telegram_web_app_data(init_data)
        user_data = verified_data['user']
        
        # Шукаємо користувача
        result = await db.execute(
            select(User).where(User.telegram_id == user_data['id'])
        )
        user = result.scalar_one_or_none()
        
        # Якщо користувач не існує, створюємо
        if not user:
            user = User(
                telegram_id=user_data['id'],
                username=user_data.get('username'),
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                referral_code=f"ref_{user_data['id']}"
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            
            logger.info(f"New user registered: {user.telegram_id}")
        else:
            # Оновлюємо дані користувача
            user.username = user_data.get('username')
            user.first_name = user_data.get('first_name')
            user.last_name = user_data.get('last_name')
            user.update_activity()
            await db.commit()
        
        # Створюємо JWT токен
        access_token = create_access_token(
            data={"sub": str(user.telegram_id)},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserProfile.from_orm(user)
        }
        
    except ValueError as e:
        logger.warning(f"Invalid Telegram auth attempt: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram Web App data"
        )
    except Exception as e:
        logger.error(f"Telegram auth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )


@router.post("/register", response_model=Dict[str, Any])
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Реєстрація користувача (для бота)
    """
    try:
        # Перевіряємо чи існує користувач
        result = await db.execute(
            select(User).where(User.telegram_id == user_data.telegram_id)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
        
        # Обробляємо реферальний код
        referrer = None
        if user_data.referral_code:
            result = await db.execute(
                select(User).where(User.referral_code == user_data.referral_code)
            )
            referrer = result.scalar_one_or_none()
        
        # Створюємо користувача
        user = User(
            telegram_id=user_data.telegram_id,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            referral_code=f"ref_{user_data.telegram_id}",
            referred_by=referrer.id if referrer else None
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        logger.info(f"User registered: {user.telegram_id}, referrer: {referrer.id if referrer else None}")
        
        # Створюємо токен
        access_token = create_access_token(
            data={"sub": str(user.telegram_id)}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserProfile.from_orm(user),
            "is_new_user": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Отримання профілю поточного користувача
    """
    return UserProfile.from_orm(current_user)


@router.patch("/me", response_model=UserProfile)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Оновлення профілю поточного користувача
    """
    try:
        # Оновлюємо дані
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        current_user.update_activity()
        await db.commit()
        await db.refresh(current_user)
        
        logger.info(f"User profile updated: {current_user.telegram_id}")
        
        return UserProfile.from_orm(current_user)
        
    except Exception as e:
        logger.error(f"Profile update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed"
        )


@router.post("/logout", response_model=BaseResponse)
async def logout(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Вихід з системи
    """
    try:
        # Можемо додати логіку для інвалідації токенів
        # Наразі просто оновлюємо активність
        current_user.update_activity()
        await db.commit()
        
        return BaseResponse(message="Successfully logged out")
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/validate-token", response_model=Dict[str, Any])
async def validate_token(
    current_user: User = Depends(get_current_active_user)
):
    """
    Валідація JWT токена
    """
    return {
        "valid": True,
        "user": UserProfile.from_orm(current_user),
        "expires_in": settings.access_token_expire_minutes * 60
    }


@router.post("/refresh-token", response_model=Dict[str, Any])
async def refresh_token(
    current_user: User = Depends(get_current_active_user)
):
    """
    Оновлення JWT токена
    """
    try:
        # Створюємо новий токен
        access_token = create_access_token(
            data={"sub": str(current_user.telegram_id)}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserProfile.from_orm(current_user)
        }
        
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )
