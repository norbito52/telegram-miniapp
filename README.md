# 🎁 GiftRoom Market

> **Безпечний маркетплейс для продажу Telegram каналів з подарунками**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![TON](https://img.shields.io/badge/blockchain-TON-0088CC.svg)](https://ton.org)
[![Telegram](https://img.shields.io/badge/telegram-bot-blue.svg)](https://telegram.org)

## 🚀 Про проєкт

**GiftRoom Market** - це інноваційний маркетплейс для безпечної купівлі-продажу Telegram каналів з телеграм подарунками. Проєкт вирішує проблему скаму в OTC чатах через систему ескроу на блокчейні TON.

### ✨ Ключові особливості

- 🔒 **Безпечні угоди** - система ескроу на TON блокчейні
- ⏱️ **Автоматизація** - таймер на 60 хвилин для передачі прав
- 💰 **Реферальна система** - 2.5% комісії за залучення друзів
- 🎯 **Верифікація** - перевірка прав адміністратора в каналах
- 📊 **Аналітика** - детальна статистика подарунків

## 🛠️ Технології

### Backend
- **FastAPI** - швидкий веб-фреймворк
- **PostgreSQL** - надійна база даних
- **Redis** - кешування та черги
- **SQLAlchemy** - ORM
- **Celery** - асинхронні задачі

### Blockchain
- **TON SDK** - робота з TON блокчейном
- **TON Connect** - підключення гаманців
- **Smart Contracts** - ескроу система

### Bot & Frontend
- **aiogram** - Telegram Bot API
- **HTML/CSS/JS** - Mini App інтерфейс
- **Telegram Web App** - нативна інтеграція

## 🎯 Як це працює

### Для продавця:
1. **Додає бота** `@giftroom_market_bot` як адміна каналу
2. **Створює оголошення** з ціною в TON
3. **Чекає покупця** та підтверджує передачу прав
4. **Отримує кошти** після успішної угоди

### Для покупця:
1. **Обирає канал** з подарунками
2. **Замораживає кошти** в ескроу
3. **Отримує права** на канал від продавця
4. **Автоматично стає власником** після верифікації

## 📦 Швидкий старт

### Локальна розробка

```bash
# Клонуємо репозиторій
git clone https://github.com/your-username/giftroom-marketplace.git
cd giftroom-marketplace

# Створюємо віртуальне середовище
python -m venv venv
source venv/bin/activate  # Linux/Mac
# або
venv\Scripts\activate     # Windows

# Встановлюємо залежності
pip install -r requirements.txt

# Налаштовуємо змінні середовища
cp .env.example .env
# Заповніть .env файл своїми даними

# Запускаємо міграції
alembic upgrade head

# Запускаємо додаток
uvicorn app.main:app --reload
```

### Деплой на Render

1. **Форкніть репозиторій**
2. **Створіть Web Service** на [Render](https://render.com)
3. **Налаштуйте змінні середовища**
4. **Деплойте автоматично** через GitHub

## ⚙️ Конфігурація

### Змінні середовища (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/giftroom_db

# Telegram Bot
BOT_TOKEN=your_bot_token_here
WEBAPP_URL=https://your-app.onrender.com

# TON Blockchain
TON_NETWORK=testnet  # або mainnet
TON_API_KEY=your_ton_api_key

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256

# Fees
MARKET_COMMISSION=0.05  # 5%
REFERRAL_COMMISSION=0.025  # 2.5%
```

## 🏗️ Архітектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │    │   Mini App      │    │   TON Wallet    │
│                 │    │   (Frontend)    │    │                 │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                             │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   Auth Service  │  Channel Service│  Escrow Service │    API    │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │      Redis      │    │   TON Network   │
│   (Database)    │    │    (Cache)      │    │  (Blockchain)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔐 Безпека

### Система ескроу
- Кошти замораживаються в смарт-контракті
- Автоматичне розблокування після передачі прав
- Повернення коштів при скасуванні угоди

### Верифікація
- Перевірка прав адміністратора бота
- Валідація всіх вхідних даних
- Захист від SQL ін'єкцій та XSS

## 📊 API Документація

### Основні endpoints

```
GET  /api/v1/channels/          # Список каналів
POST /api/v1/channels/          # Створення каналу
GET  /api/v1/channels/{id}      # Деталі каналу
POST /api/v1/channels/{id}/buy  # Купівля каналу

GET  /api/v1/gifts/             # Список подарунків
GET  /api/v1/users/profile      # Профіль користувача
POST /api/v1/transactions/      # Створення транзакції
GET  /api/v1/referrals/stats    # Реферальна статистика
```

Повну документацію API дивіться на `/docs` (Swagger) після запуску додатка.

## 🧪 Тестування

```bash
# Юніт тести
pytest tests/unit/

# Інтеграційні тести
pytest tests/integration/

# Тести API
pytest tests/api/

# Всі тести з покриттям
pytest --cov=app tests/
```

## 🚀 Деплой

### Автоматичний деплой через GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Render

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        uses: render-com/deploy-action@v1
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

### Ручний деплой

```bash
# Збірка Docker образу
docker build -t giftroom-marketplace .

# Запуск контейнера
docker run -p 8000:8000 giftroom-marketplace
```

## 📋 TODO

- [ ] Додати підтримку інших криптовалют
- [ ] Реалізувати чат між покупцем і продавцем
- [ ] Додати систему рейтингів
- [ ] Мобільний додаток для iOS/Android
- [ ] Мультимовна підтримка
- [ ] Інтеграція з TON DNS

## 🤝 Внесок у проєкт

Вітаємо будь-які внески! Будь ласка:

1. **Форкніть** проєкт
2. **Створіть** feature branch (`git checkout -b feature/AmazingFeature`)
3. **Закомітьте** зміни (`git commit -m 'Add some AmazingFeature'`)
4. **Запуште** branch (`git push origin feature/AmazingFeature`)
5. **Створіть** Pull Request

## 📄 Ліцензія

Цей проєкт ліцензований під MIT License - дивіться [LICENSE](LICENSE) файл для деталей.

## 👥 Команда

- **Розробник** - [Ваше ім'я](https://github.com/your-username)
- **Дизайн** - [Дизайнер](https://github.com/designer-username)

## 📞 Контакти

- **Telegram**: [@your_telegram](https://t.me/your_telegram)
- **Email**: your.email@example.com
- **GitHub**: [your-username](https://github.com/your-username)

## 🎖️ Подяки

- [TON Foundation](https://ton.org) за блокчейн
- [Telegram](https://telegram.org) за Bot API
- [FastAPI](https://fastapi.tiangolo.com) за чудовий фреймворк

---

<div align="center">
  <strong>Зроблено з ❤️ в Україні</strong>
</div>

---

## 🔗 Корисні посилання

- [Live Demo](https://giftroom-marketplace.onrender.com)
- [Telegram Bot](https://t.me/giftroom_market_bot)
- [TON Blockchain](https://ton.org)
- [Документація API](https://giftroom-marketplace.onrender.com/docs)

---

*Останнє оновлення: 18 липня 2025*
