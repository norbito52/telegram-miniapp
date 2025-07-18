"""
Telegram Bot обробники для GiftRoom Marketplace
"""
import asyncio
import logging
from typing import Dict, Any, Optional
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, MenuButtonWebApp, BotCommand
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database import AsyncSessionLocal
from app.models import User, Channel, Transaction
from app.config import TransactionStatus
from services.telegram_service import TelegramService
from services.notification_service import NotificationService

logger = logging.getLogger(__name__)

# Ініціалізація бота
bot = Bot(token=settings.bot_token)
dp = Dispatcher()
router = Router()

# Сервіси
telegram_service = TelegramService()
notification_service = NotificationService()

# Тексти повідомлень
MESSAGES = {
    "welcome": """
🎁 <b>Вітаємо в GiftRoom Market!</b>

Безпечний маркетплейс для купівлі-продажу Telegram каналів з подарунками.

🔒 <b>Наші переваги:</b>
• Система ескроу на TON блокчейні
• Верифікація всіх каналів
• Захист від скаму
• Комісія всього 5%

💰 <b>Реферальна програма:</b>
Запрошуйте друзів і отримуйте 2.5% з кожної угоди!

Натисніть кнопку нижче, щоб почати 👇
""",
    
    "help": """
🆘 <b>Довідка GiftRoom Market</b>

<b>Для покупців:</b>
1. Оберіть канал з подарунками
2. Натисніть "Купити"
3. Підтвердіть оплату в TON
4. Отримайте права на канал

<b>Для продавців:</b>
1. Додайте бота як адміна каналу
2. Створіть оголошення з ціною
3. Дочекайтесь покупця
4. Передайте права та отримайте кошти

<b>Команди:</b>
/start - Головне меню
/help - Ця довідка
/profile - Ваш профіль
/channels - Ваші канали
/support - Підтримка
""",
    
    "profile": """
👤 <b>Ваш профіль</b>

🆔 ID: {user_id}
📱 Telegram: {username}
💰 Баланс: {balance} TON

📊 <b>Статистика:</b>
• Куплено каналів: {bought}
• Продано каналів: {sold}
• Загальний оборот: {volume} TON

🎯 <b>Реферальна програма:</b>
• Запрошено друзів: {referrals}
• Заробок: {earnings} TON
• Ваш код: <code>{referral_code}</code>
""",
    
    "no_channels": """
📝 <b>У вас немає каналів</b>

Щоб створити оголошення:
1. Зробіть бота адміном вашого каналу
2. Відкрийте marketplace через кнопку нижче
3. Створіть оголошення з ціною

💡 <b>Порада:</b> Канали з унікальними подарунками продаються швидше!
""",
    
    "transaction_created": """
🔄 <b>Транзакцію створено!</b>

📋 <b>Деталі:</b>
• Канал: {channel_name}
• Сума: {amount} TON
• Комісія: {commission} TON
• Статус: Очікування оплати

⏰ <b>Час на оплату: 60 хвилин</b>

Покупець має підтвердити оплату в додатку.
""",
    
    "transaction_paid": """
✅ <b>Оплата підтверджена!</b>

У вас є 60 хвилин для передачі прав на канал покупцю.

📋 <b>Що робити:</b>
1. Зайдіть в налаштування каналу
2. Видаліть себе з адміністраторів
3. Додайте покупця як власника
4. Підтвердіть передачу в додатку

⚠️ <b>Увага:</b> Якщо не передасте права вчасно, кошти будуть повернуті покупцю.
""",
    
    "transaction_completed": """
🎉 <b>Угода завершена!</b>

Канал успішно передано покупцю.
Кошти зараховані на ваш баланс.

💰 <b>Отримано:</b>
• Основна сума: {seller_amount} TON
• Реферальна винагорода: {referral} TON

Дякуємо за користування GiftRoom Market!
""",
    
    "transaction_cancelled": """
❌ <b>Угода скасована</b>

Причина: {reason}

💰 Кошти повернуті покупцю.
📝 Канал знову доступний для продажу.
""",
    
    "support": """
🆘 <b>Підтримка</b>

Якщо у вас виникли питання або проблеми:

📞 <b>Контакти:</b>
• Telegram: @support_giftroom
• Email: support@giftroom.market

🕐 <b>Час роботи:</b>
Цілодобово, відповідь протягом 1-2 годин

❓ <b>Часті питання:</b>
• Як стати адміном каналу?
• Що робити якщо транзакція зависла?
• Як отримати реферальну винагороду?

Всі відповіді є в нашій базі знань в додатку.
"""
}


# Клавіатури
def get_main_keyboard() -> InlineKeyboardMarkup:
    """Головна клавіатура"""
    webapp = WebAppInfo(url=settings.webapp_url)
    
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="🎁 Відкрити Marketplace",
            web_app=webapp
        )
    )
    keyboard.add(
        InlineKeyboardButton(text="👤 Профіль", callback_data="profile"),
        InlineKeyboardButton(text="📋 Мої канали", callback_data="my_channels")
    )
    keyboard.add(
        InlineKeyboardButton(text="🆘 Допомога", callback_data="help"),
        InlineKeyboardButton(text="💬 Підтримка", callback_data="support")
    )
    keyboard.adjust(1, 2, 2)
    
    return keyboard.as_markup()


def get_profile_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура профілю"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="🎯 Реферальна програма", callback_data="referrals"),
        InlineKeyboardButton(text="💰 Поповнити баланс", callback_data="top_up")
    )
    keyboard.add(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")
    )
    keyboard.adjust(2, 1)
    
    return keyboard.as_markup()


def get_channels_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура каналів"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="➕ Створити канал", callback_data="create_channel"),
        InlineKeyboardButton(text="🔄 Оновити подарунки", callback_data="refresh_gifts")
    )
    keyboard.add(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")
    )
    keyboard.adjust(2, 1)
    
    return keyboard.as_markup()


def get_transaction_keyboard(transaction_id: int, is_seller: bool = False) -> InlineKeyboardMarkup:
    """Клавіатура транзакції"""
    keyboard = InlineKeyboardBuilder()
    
    if is_seller:
        keyboard.add(
            InlineKeyboardButton(
                text="✅ Підтвердити передачу",
                callback_data=f"confirm_transfer_{transaction_id}"
            )
        )
    else:
        keyboard.add(
            InlineKeyboardButton(
                text="💰 Оплатити",
                callback_data=f"pay_transaction_{transaction_id}"
            )
        )
    
    keyboard.add(
        InlineKeyboardButton(
            text="❌ Скасувати",
            callback_data=f"cancel_transaction_{transaction_id}"
        )
    )
    keyboard.adjust(1, 1)
    
    return keyboard.as_markup()


# Утиліти
async def get_db() -> AsyncSession:
    """Отримання сесії БД"""
    async with AsyncSessionLocal() as session:
        yield session


async def get_or_create_user(user_data: Dict[str, Any]) -> User:
    """Отримання або створення користувача"""
    async with AsyncSessionLocal() as db:
        # Пошук існуючого користувача
        result = await db.execute(
            select(User).where(User.telegram_id == user_data['id'])
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Створюємо нового користувача
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
            
            logger.info(f"New user created: {user.telegram_id}")
        
        return user


# Обробники команд
@router.message(CommandStart())
async def start_command(message: Message):
    """Команда /start"""
    try:
        # Отримуємо або створюємо користувача
        user = await get_or_create_user(message.from_user.model_dump())
        
        # Перевіряємо реферальний код
        if message.text and len(message.text.split()) > 1:
            referral_code = message.text.split()[1]
            # Обробляємо реферальний код
            await process_referral_code(user, referral_code)
        
        # Встановлюємо кнопку меню
        webapp = WebAppInfo(url=settings.webapp_url)
        menu_button = MenuButtonWebApp(text="🎁 GiftRoom", web_app=webapp)
        await bot.set_chat_menu_button(
            chat_id=message.chat.id,
            menu_button=menu_button
        )
        
        await message.answer(
            MESSAGES["welcome"],
            parse_mode="HTML",
            reply_markup=get_main_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await message.answer("Виникла помилка. Спробуйте ще раз.")


@router.message(Command("help"))
async def help_command(message: Message):
    """Команда /help"""
    await message.answer(
        MESSAGES["help"],
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )


@router.message(Command("profile"))
async def profile_command(message: Message):
    """Команда /profile"""
    try:
        user = await get_or_create_user(message.from_user.model_dump())
        
        # Отримуємо статистику користувача
        # TODO: Реалізувати отримання статистики з БД
        stats = {
            "user_id": user.id,
            "username": user.display_name,
            "balance": user.balance,
            "bought": user.total_bought,
            "sold": user.total_sold,
            "volume": user.total_volume,
            "referrals": 0,  # TODO: підрахувати з БД
            "earnings": 0,   # TODO: підрахувати з БД
            "referral_code": user.referral_code
        }
        
        await message.answer(
            MESSAGES["profile"].format(**stats),
            parse_mode="HTML",
            reply_markup=get_profile_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Error in profile command: {e}")
        await message.answer("Не вдалося завантажити профіль.")


@router.message(Command("channels"))
async def channels_command(message: Message):
    """Команда /channels"""
    try:
        user = await get_or_create_user(message.from_user.model_dump())
        
        # Отримуємо канали користувача
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Channel).where(Channel.owner_id == user.id)
            )
            channels = result.scalars().all()
        
        if not channels:
            await message.answer(
                MESSAGES["no_channels"],
                parse_mode="HTML",
                reply_markup=get_channels_keyboard()
            )
            return
        
        # Формуємо список каналів
        channels_text = "📋 <b>Ваші канали:</b>\n\n"
        for channel in channels:
            channels_text += f"• {channel.display_name}\n"
            channels_text += f"  💰 {channel.price} TON\n"
            channels_text += f"  📊 {channel.status}\n\n"
        
        await message.answer(
            channels_text,
            parse_mode="HTML",
            reply_markup=get_channels_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Error in channels command: {e}")
        await message.answer("Не вдалося завантажити канали.")


# Обробники callback'ів
@router.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    """Callback профілю"""
    await callback.message.edit_text(
        MESSAGES["profile"],
        parse_mode="HTML",
        reply_markup=get_profile_keyboard()
    )


@router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    """Callback допомоги"""
    await callback.message.edit_text(
        MESSAGES["help"],
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )


@router.callback_query(F.data == "support")
async def support_callback(callback: CallbackQuery):
    """Callback підтримки"""
    await callback.message.edit_text(
        MESSAGES["support"],
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )


@router.callback_query(F.data == "back_to_main")
async def back_to_main_callback(callback: CallbackQuery):
    """Callback повернення в головне меню"""
    await callback.message.edit_text(
        MESSAGES["welcome"],
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )


@router.callback_query(F.data.startswith("pay_transaction_"))
async def pay_transaction_callback(callback: CallbackQuery):
    """Callback оплати транзакції"""
    try:
        transaction_id = int(callback.data.split("_")[2])
        
        # Знаходимо транзакцію
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Transaction).where(Transaction.id == transaction_id)
            )
            transaction = result.scalar_one_or_none()
        
        if not transaction:
            await callback.answer("Транзакція не знайдена", show_alert=True)
            return
        
        # Перевіряємо статус
        if transaction.status != TransactionStatus.PENDING:
            await callback.answer("Транзакція вже оброблена", show_alert=True)
            return
        
        # Відправляємо на оплату через webapp
        webapp_url = f"{settings.webapp_url}/pay/{transaction_id}"
        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(
                text="💰 Оплатити через TON",
                web_app=WebAppInfo(url=webapp_url)
            )
        )
        
        await callback.message.edit_text(
            f"💰 <b>Оплата транзакції #{transaction_id}</b>\n\n"
            f"Сума: {transaction.amount} TON\n"
            f"Комісія: {transaction.commission} TON\n\n"
            f"Натисніть кнопку для оплати через TON Connect",
            parse_mode="HTML",
            reply_markup=keyboard.as_markup()
        )
        
    except Exception as e:
        logger.error(f"Error in pay transaction callback: {e}")
        await callback.answer("Виникла помилка при оплаті", show_alert=True)


@router.callback_query(F.data.startswith("confirm_transfer_"))
async def confirm_transfer_callback(callback: CallbackQuery):
    """Callback підтвердження передачі каналу"""
    try:
        transaction_id = int(callback.data.split("_")[2])
        
        # Знаходимо транзакцію
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Transaction).where(Transaction.id == transaction_id)
            )
            transaction = result.scalar_one_or_none()
        
        if not transaction:
            await callback.answer("Транзакція не знайдена", show_alert=True)
            return
        
        # Перевіряємо чи користувач є продавцем
        user = await get_or_create_user(callback.from_user.model_dump())
        if transaction.seller_id != user.id:
            await callback.answer("Ви не є продавцем цієї транзакції", show_alert=True)
            return
        
        # Перевіряємо статус
        if transaction.status != TransactionStatus.PENDING:
            await callback.answer("Транзакція вже оброблена", show_alert=True)
            return
        
        # Перевіряємо передачу прав через Telegram API
        channel_transferred = await telegram_service.verify_channel_ownership_transfer(
            transaction.channel.telegram_channel_id,
            transaction.buyer_id
        )
        
        if not channel_transferred:
            await callback.answer(
                "Права на канал ще не передано. Спочатку передайте канал покупцю.",
                show_alert=True
            )
            return
        
        # Завершуємо транзакцію
        await complete_transaction(transaction_id)
        
        await callback.message.edit_text(
            "✅ <b>Транзакція завершена!</b>\n\n"
            "Канал успішно передано покупцю.\n"
            f"Кошти ({transaction.seller_amount} TON) зараховані на ваш баланс.",
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"Error in confirm transfer callback: {e}")
        await callback.answer("Виникла помилка при підтвердженні", show_alert=True)


@router.callback_query(F.data.startswith("cancel_transaction_"))
async def cancel_transaction_callback(callback: CallbackQuery):
    """Callback скасування транзакції"""
    try:
        transaction_id = int(callback.data.split("_")[2])
        
        # Скасовуємо транзакцію
        await cancel_transaction(transaction_id, "Скасовано користувачем")
        
        await callback.message.edit_text(
            "❌ <b>Транзакція скасована</b>\n\n"
            "Кошти повернуті покупцю.",
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"Error in cancel transaction callback: {e}")
        await callback.answer("Виникла помилка при скасуванні", show_alert=True)


# Бізнес-логіка
async def process_referral_code(user: User, referral_code: str):
    """Обробка реферального коду"""
    try:
        async with AsyncSessionLocal() as db:
            # Шукаємо реферера
            result = await db.execute(
                select(User).where(User.referral_code == referral_code)
            )
            referrer = result.scalar_one_or_none()
            
            if referrer and referrer.id != user.id and not user.referred_by:
                user.referred_by = referrer.id
                await db.commit()
                
                logger.info(f"User {user.id} referred by {referrer.id}")
                
                # Сповіщаємо реферера
                await bot.send_message(
                    referrer.telegram_id,
                    f"🎉 <b>Новий реферал!</b>\n\n"
                    f"Користувач {user.display_name} приєднався за вашим посиланням.\n"
                    f"Тепер ви будете отримувати 2.5% з його угод!",
                    parse_mode="HTML"
                )
                
    except Exception as e:
        logger.error(f"Error processing referral code: {e}")


async def complete_transaction(transaction_id: int):
    """Завершення транзакції"""
    try:
        async with AsyncSessionLocal() as db:
            # Знаходимо транзакцію
            result = await db.execute(
                select(Transaction).where(Transaction.id == transaction_id)
            )
            transaction = result.scalar_one_or_none()
            
            if not transaction:
                return
            
            # Оновлюємо статус
            transaction.status = TransactionStatus.COMPLETED
            transaction.completed_at = func.now()
            
            # Зараховуємо кошти продавцю
            seller_result = await db.execute(
                select(User).where(User.id == transaction.seller_id)
            )
            seller = seller_result.scalar_one()
            seller.balance += transaction.seller_amount
            seller.total_sold += 1
            seller.total_volume += transaction.amount
            
            # Оновлюємо статистику покупця
            buyer_result = await db.execute(
                select(User).where(User.id == transaction.buyer_id)
            )
            buyer = buyer_result.scalar_one()
            buyer.total_bought += 1
            buyer.total_volume += transaction.amount
            
            # Оновлюємо статус каналу
            channel_result = await db.execute(
                select(Channel).where(Channel.id == transaction.channel_id)
            )
            channel = channel_result.scalar_one()
            channel.status = "sold"
            
            # Обробляємо реферальну винагороду
            if seller.referred_by:
                referral_earning = ReferralEarning(
                    referrer_id=seller.referred_by,
                    referred_id=seller.id,
                    transaction_id=transaction.id,
                    amount=transaction.referral_commission,
                    status="pending"
                )
                db.add(referral_earning)
            
            await db.commit()
            
            # Сповіщаємо учасників
            await notification_service.send_transaction_completed(transaction)
            
            logger.info(f"Transaction {transaction_id} completed")
            
    except Exception as e:
        logger.error(f"Error completing transaction {transaction_id}: {e}")


async def cancel_transaction(transaction_id: int, reason: str):
    """Скасування транзакції"""
    try:
        async with AsyncSessionLocal() as db:
            # Знаходимо транзакцію
            result = await db.execute(
                select(Transaction).where(Transaction.id == transaction_id)
            )
            transaction = result.scalar_one_or_none()
            
            if not transaction:
                return
            
            # Оновлюємо статус
            transaction.status = TransactionStatus.CANCELLED
            
            # Повертаємо кошти покупцю (якщо були списані)
            if transaction.escrow_address:
                # TODO: Повернути кошти через TON
                pass
            
            await db.commit()
            
            # Сповіщаємо учасників
            await notification_service.send_transaction_cancelled(transaction, reason)
            
            logger.info(f"Transaction {transaction_id} cancelled: {reason}")
            
    except Exception as e:
        logger.error(f"Error cancelling transaction {transaction_id}: {e}")


# Налаштування бота
async def setup_bot():
    """Налаштування бота"""
    try:
        # Встановлюємо команди
        commands = [
            BotCommand(command="start", description="Почати роботу"),
            BotCommand(command="help", description="Довідка"),
            BotCommand(command="profile", description="Мій профіль"),
            BotCommand(command="channels", description="Мої канали"),
            BotCommand(command="support", description="Підтримка"),
        ]
        await bot.set_my_commands(commands)
        
        # Додаємо роутер
        dp.include_router(router)
        
        # Налаштовуємо webhook якщо потрібно
        if settings.bot_webhook_url:
            await bot.set_webhook(
                url=settings.bot_webhook_url,
                drop_pending_updates=True
            )
            logger.info(f"Bot webhook set to {settings.bot_webhook_url}")
        
        logger.info("Bot setup completed")
        
    except Exception as e:
        logger.error(f"Bot setup failed: {e}")
        raise


async def stop_bot():
    """Зупинка бота"""
    try:
        await bot.delete_webhook()
        await bot.session.close()
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Bot stop error: {e}")


# Webhook обробник
async def handle_webhook(data: Dict[str, Any]):
    """Обробка webhook від Telegram"""
    try:
        await dp.feed_webhook_update(bot, data)
    except Exception as e:
        logger.error(f"Webhook handling error: {e}")


# Для запуску в polling режимі (розробка)
async def start_polling():
    """Запуск бота в polling режимі"""
    try:
        await setup_bot()
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.error(f"Polling start error: {e}")
        raise


# Webhook сервер для продакшн
def create_webhook_app() -> web.Application:
    """Створення webhook додатка"""
    app = web.Application()
    
    # Налаштовуємо webhook
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.secret_key[:32]  # Перші 32 символи
    )
    
    webhook_handler.register(app, path="/webhook/bot")
    setup_application(app, dp, bot=bot)
    
    return app


if __name__ == "__main__":
    # Для тестування в polling режимі
    asyncio.run(start_polling())
