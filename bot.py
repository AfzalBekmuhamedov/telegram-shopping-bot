import os
from dotenv import load_dotenv
import requests
import time
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
load_dotenv()

TOKEN = os.getenv("TOKEN")
API_URL = os.getenv("API_URL")

bot = TeleBot(TOKEN)


def load_products():
    global PRODUCT_MAP

    res = requests.get(API_URL)
    products = res.json()
    PRODUCT_MAP = {p['id']:p for p in products}

@bot.message_handler(commands=['start'])
def start(message):
    load_products()
    bot.send_chat_action(message.chat.id,"typing")
    time.sleep(1)
    markup = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton("🛍 Browse", callback_data="browse")
    button = InlineKeyboardButton("🛅 Help",callback_data="help")
    button3 = InlineKeyboardButton("ℹ️ About", callback_data='about')
    markup.add( button2,button,button3)

    bot.send_message(message.chat.id, "👋 Welcome to our shop. We glad to see you here!\n🛍 Choose your needed section below:",reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_call(call):
    bot.answer_callback_query(call.id)
    text = ("🤖 *How to use this bot:*\n\n"
            "1️⃣ /start - View all products\n"
            "2️⃣ /cart - View your cart\n"
            "3️⃣ /clear - Clears your cart\n"
            "4️⃣ /order - Make an order\n"
            "5️⃣ Pay using Stripe 💳\n"
            "6️⃣ /paid - Confirm payment \n\n")
    bot.send_message(call.message.chat.id,text,parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call:call.data == "about")
def about(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id,"ℹ️ You can view and purchase through this bot")

@bot.callback_query_handler(func=lambda call:call.data == "browse")
def browse(call):
    global PRODUCT_MAP
    bot.send_chat_action(call.message.chat.id,"typing")
    time.sleep(1)
    try:
        res = requests.get(API_URL)
        products = res.json()
        PRODUCT_MAP = {p['id']: p for p in products}
        if not products:
            bot.send_message(call.message.chat.id, "❌ This kind of product is not available")
            return
        for p in products:
            bot.send_chat_action(call.message.chat.id, "typing")
            time.sleep(0.4)
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text="🛒 Add to cart", callback_data=f"add_{p['id']}"))
            text = f"📦 {p['name']}\n🔖Description: {p['description'][:100]+"...5"}\n💰 Price: ${p['price']}"
            if p.get('image'):
                file_path = f"media/products/{p['image'].split('/')[-1]}"
                try:
                    with open(file_path,'rb') as photo:
                        bot.send_photo(call.message.chat.id,photo,caption=text,reply_markup=markup)
                except Exception as e:
                    print(e)
                    bot.send_message(call.message.chat.id, text, reply_markup=markup)
            else:
                bot.send_message(call.message.chat.id,text, reply_markup=markup)
    except Exception as e:
        print(e)
        bot.send_message(call.message.chat.id,"❌ Server error")

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🛒 View cart", callback_data="cart"))
    bot.send_message(call.message.chat.id,
                         "✅ We have received the products you selected, just click the View Cart button to see them!",
                         reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "cart")
def cart_button(call):
    view_cart(call.message)

user_cart = {}

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
def add_to_cart(call):
    user_id= call.from_user.id
    product_pk = int(call.data.split("_")[1])
    if user_id not in user_cart:
        user_cart[user_id]=[]
    user_cart[user_id].append(product_pk)
    bot.answer_callback_query(call.id,"✅ Added to cart")

@bot.message_handler(commands=['cart'])
def view_cart(message):
    bot.send_chat_action(message.chat.id,"typing")
    time.sleep(1)

    user_id = message.chat.id
    if user_id not in user_cart or not user_cart[user_id]:
        bot.send_message(message.chat.id,"🛒 Cart empty")
        return

    text = "🛒 *Your cart:*\n\n"
    total = 0

    for item in user_cart[user_id]:
        p = PRODUCT_MAP.get(item)
        if p:
            text += f"📦 {p['name']} - ${p['price']}\n"
            total += float(p['price'])

    text += f"\n📦 {len(user_cart[user_id])} products\n💰 *Total: ${int(total)}*"

    bot.send_message(message.chat.id, text, parse_mode="Markdown")

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Make an order", callback_data="order"))
    bot.send_message(message.chat.id, "Shall we order?", reply_markup=markup)

@bot.message_handler(commands=["clear"])
def clear_cart(message:Message):
    user_id = message.chat.id
    user_cart[user_id]=[]
    bot.send_message(message.chat.id,"🧹 Cart cleared")



@bot.message_handler(commands=['order'])
def make_order(message:Message):
    bot.send_chat_action(message.chat.id,"typing")
    time.sleep(1)
    user_id = message.chat.id
    if user_id not in user_cart or not user_cart[user_id]:
        bot.send_message(message.chat.id, "🛒 Cart empty")
        return
    total = 0
    text = "📑 *Order summary:*\n\n"
    counts = {}
    for item in user_cart[user_id]:
        counts[item] = counts.get(item,0)+1
    for product_id, qty in counts.items():
        p = PRODUCT_MAP.get(product_id)
        if p:
            text += f"📦 {p['name']} x{qty}\n"
            total += float(p['price'])*qty
    text += f"\n💰 *Total : ${int(total)}*\n\n"
    text += "💳 *Payment:*\nStripe\n"
    text += "After payment:\n Click /paid"

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Confirm",callback_data="confirm_order"),
               InlineKeyboardButton("❌ Cancel",callback_data="cancel_order"))

    bot.send_message(message.chat.id,text,parse_mode="Markdown",reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "order")
def order_button(call):
    make_order(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_order")
def confirm_order(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id,"💳 Please complete payment and click /paid")

@bot.callback_query_handler(func=lambda call:call.data == "cancel_order")
def cancel_order(call):
    bot.answer_callback_query(call.id,"❌ Order cancelled")
    bot.send_message(call.message.chat.id,"❌ Your order has been cancelled, but you can continue shopping!")

@bot.message_handler(commands=['paid'])
def confirm_payment(message):
    bot.send_chat_action(message.chat.id,"typing")
    time.sleep(1)
    user_id = message.chat.id
    if user_id not in user_cart or not user_cart[user_id]:
        bot.send_message(message.chat.id, "❌ No order found")
        return
    data ={
        "user_id":user_id,
        "products":user_cart[user_id]
    }
    try:
        res = requests.post("http://127.0.0.1:8000/api/orders/create/", json=data)
        result = res.json()
        bot.send_message(message.chat.id,f"✅ *Payment confirmed!*\n📦 Order created\n💰 *Total : ${int(result['total_price'])}*",parse_mode="Markdown")
        user_cart[user_id] = []
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id,"❌ Order failed")

# if __name__ == "__main__":
#     print("Bot ishga tushdi")
#     bot.infinity_polling()


