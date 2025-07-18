"""
Сервіс для роботи з Telegram API
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional
from aiogram import Bot
from aiogram.types import ChatMember, Chat
from aiogram.exceptions import TelegramAPIError

from app.config import settings

logger = logging.getLogger(__name__)


class TelegramService:
    """Сервіс для роботи з Telegram API"""
    
    def __init__(self):
        self.bot = Bot(token=settings.bot_token)
    
    async def get_channel_info(self, channel_id: int) -> Dict[str, Any]:
        """
        Отримання інформації про канал
        """
        try:
            chat = await self.bot.get_chat(channel_id)
            
            # Отримуємо кількість учасників
            member_count = 0
            try:
                member_count = await self.bot.get_chat_member_count(channel_id)
            except TelegramAPIError:
                pass
            
            return {
                "id": chat.id,
                "type": chat.type,
                "title": chat.title,
                "username": chat.username,
                "description": chat.description,
                "member_count": member_count,
                "invite_link": chat.invite_link,
                "photo": chat.photo.big_file_id if chat.photo else None
            }
            
        except TelegramAPIError as e:
            logger.error(f"Failed to get channel info {channel_id}: {e}")
            raise Exception(f"Cannot access channel: {e}")
    
    async def check_bot_is_admin(self, channel_id: int) -> bool:
        """
        Перевірка чи бот є адміністратором каналу
        """
        try:
            bot_info = await self.bot.get_me()
            member = await self.bot.get_chat_member(channel_id, bot_info.id)
            
            return member.status in ["administrator", "creator"]
            
        except TelegramAPIError as e:
            logger.error(f"Failed to check bot admin status {channel_id}: {e}")
            return False
    
    async def get_channel_administrators(self, channel_id: int) -> List[Dict[str, Any]]:
        """
        Отримання списку адміністраторів каналу
        """
        try:
            admins = await self.bot.get_chat_administrators(channel_id)
            
            result = []
            for admin in admins:
                user_info = {
                    "user_id": admin.user.id,
                    "username": admin.user.username,
                    "first_name": admin.user.first_name,
                    "last_name": admin.user.last_name,
                    "status": admin.status,
                    "is_anonymous": getattr(admin, 'is_anonymous', False),
                    "can_be_edited": getattr(admin, 'can_be_edited', False)
                }
                
                # Додаємо права для адміністраторів
                if admin.status == "administrator":
                    user_info.update({
                        "can_manage_chat": getattr(admin, 'can_manage_chat', False),
                        "can_post_messages": getattr(admin, 'can_post_messages', False),
                        "can_edit_messages": getattr(admin, 'can_edit_messages', False),
                        "can_delete_messages": getattr(admin, 'can_delete_messages', False),
                        "can_manage_video_chats": getattr(admin, 'can_manage_video_chats', False),
                        "can_restrict_members": getattr(admin, 'can_restrict_members', False),
                        "can_promote_members": getattr(admin, 'can_promote_members', False),
                        "can_change_info": getattr(admin, 'can_change_info', False),
                        "can_invite_users": getattr(admin, 'can_invite_users', False),
                        "can_pin_messages": getattr(admin, 'can_pin_messages', False)
                    })
                
                result.append(user_info)
            
            return result
            
        except TelegramAPIError as e:
            logger.error(f"Failed to get channel administrators {channel_id}: {e}")
            return []
    
    async def verify_channel_ownership_transfer(self, channel_id: int, new_owner_id: int) -> bool:
        """
        Перевірка передачі прав власності на канал
        """
        try:
            # Отримуємо поточних адміністраторів
            admins = await self.get_channel_administrators(channel_id)
            
            # Перевіряємо чи новий власник є адміністратором
            new_owner_is_admin = False
            bot_is_admin = False
            
            bot_info = await self.bot.get_me()
            
            for admin in admins:
                if admin["user_id"] == new_owner_id:
                    new_owner_is_admin = True
                    # Перевіряємо чи має права власника
                    if admin["status"] == "creator" or admin.get("can_manage_chat", False):
                        return True
                
                if admin["user_id"] == bot_info.id:
                    bot_is_admin = True
            
            # Якщо новий власник не є адміністратором, передача не відбулася
            if not new_owner_is_admin:
                return False
            
            # Якщо бот більше не адмін, можливо права передані
            if not bot_is_admin:
                return True
            
            return False
            
        except TelegramAPIError as e:
            logger.error(f"Failed to verify ownership transfer {channel_id}: {e}")
            return False
    
    async def get_channel_messages(self, channel_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Отримання повідомлень з каналу (для парсингу подарунків)
        """
        try:
            messages = []
            
            # Отримуємо останні повідомлення
            # Примітка: це базова реалізація, в реальності потрібно використовувати
            # Telegram Client API для отримання історії повідомлень
            
            # Для demo версії повертаємо пусті дані
            # В реальній реалізації тут буде код для отримання повідомлень
            
            return messages
            
        except TelegramAPIError as e:
            logger.error(f"Failed to get channel messages {channel_id}: {e}")
            return []
    
    async def send_notification(self, user_id: int, message: str, parse_mode: str = "HTML") -> bool:
        """
        Відправка сповіщення користувачу
        """
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode=parse_mode
            )
            return True
            
        except TelegramAPIError as e:
            logger.error(f"Failed to send notification to {user_id}: {e}")
            return False
    
    async def get_user_info(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Отримання інформації про користувача
        """
        try:
            user = await self.bot.get_chat(user_id)
            
            return {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "bio": user.bio,
                "photo": user.photo.big_file_id if user.photo else None
            }
            
        except TelegramAPIError as e:
            logger.error(f"Failed to get user info {user_id}: {e}")
            return None
    
    async def create_channel_invite_link(self, channel_id: int, expire_date: Optional[int] = None) -> Optional[str]:
        """
        Створення запрошувального посилання для каналу
        """
        try:
            invite_link = await self.bot.create_chat_invite_link(
                chat_id=channel_id,
                expire_date=expire_date,
                creates_join_request=True
            )
            return invite_link.invite_link
            
        except TelegramAPIError as e:
            logger.error(f"Failed to create invite link for {channel_id}: {e}")
            return None
    
    async def promote_user_to_admin(self, channel_id: int, user_id: int, permissions: Dict[str, bool]) -> bool:
        """
        Призначення користувача адміністратором каналу
        """
        try:
            await self.bot.promote_chat_member(
                chat_id=channel_id,
                user_id=user_id,
                can_manage_chat=permissions.get("can_manage_chat", False),
                can_post_messages=permissions.get("can_post_messages", False),
                can_edit_messages=permissions.get("can_edit_messages", False),
                can_delete_messages=permissions.get("can_delete_messages", False),
                can_manage_video_chats=permissions.get("can_manage_video_chats", False),
                can_restrict_members=permissions.get("can_restrict_members", False),
                can_promote_members=permissions.get("can_promote_members", False),
                can_change_info=permissions.get("can_change_info", False),
                can_invite_users=permissions.get("can_invite_users", False),
                can_pin_messages=permissions.get("can_pin_messages", False)
            )
            return True
            
        except TelegramAPIError as e:
            logger.error(f"Failed to promote user {user_id} in {channel_id}: {e}")
            return False
    
    async def remove_user_from_admin(self, channel_id: int, user_id: int) -> bool:
        """
        Видалення користувача з адміністраторів каналу
        """
        try:
            await self.bot.promote_chat_member(
                chat_id=channel_id,
                user_id=user_id,
                can_manage_chat=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_delete_messages=False,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_promote_members=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )
            return True
            
        except TelegramAPIError as e:
            logger.error(f"Failed to remove admin {user_id} from {channel_id}: {e}")
            return False
    
    async def get_channel_statistics(self, channel_id: int) -> Dict[str, Any]:
        """
        Отримання статистики каналу
        """
        try:
            chat = await self.bot.get_chat(channel_id)
            member_count = await self.bot.get_chat_member_count(channel_id)
            
            return {
                "member_count": member_count,
                "title": chat.title,
                "username": chat.username,
                "description": chat.description,
                "invite_link": chat.invite_link,
                "pinned_message": chat.pinned_message.message_id if chat.pinned_message else None,
                "has_protected_content": chat.has_protected_content,
                "has_visible_history": chat.has_visible_history
            }
            
        except TelegramAPIError as e:
            logger.error(f"Failed to get channel statistics {channel_id}: {e}")
            return {}
    
    async def validate_channel_access(self, channel_id: int) -> Dict[str, Any]:
        """
        Валідація доступу до каналу
        """
        try:
            # Перевіряємо доступ до каналу
            channel_info = await self.get_channel_info(channel_id)
            
            # Перевіряємо чи бот є адміністратором
            is_admin = await self.check_bot_is_admin(channel_id)
            
            # Отримуємо адміністраторів
            admins = await self.get_channel_administrators(channel_id)
            
            return {
                "accessible": True,
                "channel_info": channel_info,
                "bot_is_admin": is_admin,
                "administrators": admins,
                "validation_passed": is_admin  # Канал валідний тільки якщо бот адмін
            }
            
        except Exception as e:
            logger.error(f"Channel validation failed {channel_id}: {e}")
            return {
                "accessible": False,
                "error": str(e),
                "validation_passed": False
            }
    
    async def close(self):
        """Закриття сесії бота"""
        try:
            await self.bot.session.close()
        except Exception as e:
            logger.error(f"Error closing bot session: {e}")


# Singleton instance
_telegram_service = None

def get_telegram_service() -> TelegramService:
    """Отримання екземпляра TelegramService"""
    global _telegram_service
    if _telegram_service is None:
        _telegram_service = TelegramService()
    return _telegram_service
