Telegram E-commerce Shopping Bot

A Telegram-based e-commerce shopping bot built with Python and TeleBot (pyTelegramBotAPI).

The bot allows customers to browse products, view product information, add products to a shopping cart, and create orders through an interactive Telegram interface.

Features

- Welcome menu with interactive buttons
- Product browsing
- Product images and descriptions
- Add products to cart
- View shopping cart
- Product quantity handling
- Automatic order total calculation
- Order summary
- Order confirmation
- Order cancellation
- Clear shopping cart
- Payment-ready order flow
- REST API integration
- Telegram inline keyboards
- Product data retrieved from backend API

«Note: The current version does not include a real payment gateway such as Stripe, Payme, or Click. The order flow is prepared so that a payment system can be integrated later.»

---

Technologies

- Python
- TeleBot / pyTelegramBotAPI
- Telegram Bot API
- REST API
- Requests
- Django REST API — backend integration
- JSON
- SQLite / Postgresql — backend database support

---

🔄 Bot Flow

/start
   │
   ▼
Welcome Menu
   │
   ├── 🛍️ Browse
   │      │
   │      ├── View Products
   │      └── Add to Cart
   │
   ├── 🛒 View Cart
   │      │
   │      ▼
   │   Order Summary
   │      │
   │      ├── ✅ Confirm
   │      └── ❌ Cancel
   │
   ├── ℹ️ Help
   │
   └── 📖 About

---

Product Browsing

The bot retrieves product information from a REST API and displays available products directly in Telegram.

Each product can contain:

- Product name
- Price
- Description
- Product image
- Add to Cart button

Product data is managed through the backend API rather than being hard-coded directly into the bot.

---

Shopping Cart

Users can add products to their personal shopping cart.

The cart supports:

- Multiple products
- Duplicate products
- Product quantities
- Automatic total calculation
- Cart clearing
- Order creation

Example:

🛒 Your Cart

T-Shirt × 2
$40

Sneakers × 1
$60

----------------
Total: $100

---

Order Management

After reviewing the cart, the customer can create an order.

The bot generates an order summary containing:

- Products
- Quantities
- Prices
- Total amount

The customer can then confirm or cancel the order.

---

Payment Flow

The current project contains a payment-ready order flow, but does not yet process real online payments.

The current flow is:

Shopping Cart
      ↓
Order Summary
      ↓
Confirm Order
      ↓
Payment / Payment Confirmation
      ↓
Order Completed

A real payment gateway such as Stripe, Payme, or Click can be integrated into this flow in a future version.

---

🔗 REST API Integration

The Telegram bot communicates with a backend REST API to retrieve product information and work with order data.

Example API endpoints:

GET  /api/products/
POST /api/orders/create/

This architecture allows the Telegram bot and backend system to remain separate.

Telegram User
      ↓
Telegram Bot
      ↓
REST API
      ↓
Django Backend
      ↓
Database

---

Installation

1. Clone the repository

git clone https://github.com/yourusername/telegram-shop-bot.git
cd telegram-shop-bot

2. Create a virtual environment

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a ".env" file:

BOT_TOKEN=your_telegram_bot_token
API_URL=http://127.0.0.1:8000/api/products/

5. Run the bot

python bot.py

---

🔐 Security

Do not expose sensitive information such as:

- Telegram Bot Token
- API credentials
- Secret keys
- Payment credentials

Make sure ".env" is included in ".gitignore".

Example:

.env
venv/
pycache/