import os
import sqlite3
import asyncio
import nltk
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# ------------------ BOT TOKEN ------------------
TOKEN = "BOT_TOKEN"  # ← Add your Bot Token here

# ------------------ REQUEST CONFIG ------------------
request = HTTPXRequest(connect_timeout=30, read_timeout=30)

# ------------------ NLTK ------------------
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

# ------------------ DATABASE ------------------
conn = sqlite3.connect("shopmate.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product TEXT
)""")
conn.commit()

# ------------------ PRODUCTS ------------------
products = {
    "laptop": {"price": 55000, "image": "laptop.jpg"},
    "phone": {"price": 30000, "image": "android.jpeg"},
    "earbuds": {"price": 2000, "image": "earbuds.jpeg"},
    "keyboard": {"price": 1500, "image": "keyboard.jpeg"},
    "mouse": {"price": 700, "image": "mouse.jpeg"}
}

# ------------------ COMMAND HANDLERS ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to ShopMate!\n\n"
        "✨ Commands:\n"
        "/products - View items\n"
        "/cart - View shopping cart\n"
        "/clearcart - Empty cart\n"
        "/help - Guide\n"
        "/exit - End session"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Commands:\n\n"
        "/products → Show product list\n"
        "/cart → View cart\n"
        "/clearcart → Clear cart\n"
        "/exit → End session"
    )

async def products_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🛍 Available Products:\n\n"
    for item, details in products.items():
        text += f"➡ {item.title()} — ₹{details['price']}\n"
    text += "\nType: add <product name> to add to cart."
    await update.message.reply_text(text)

async def send_product_image(update, product_name):
    image_path = os.path.join("images", products[product_name]["image"])
    if os.path.exists(image_path):
        with open(image_path, "rb") as img:
            await update.message.reply_photo(
                img,
                caption=f"🛍 {product_name.title()}\n💰 ₹{products[product_name]['price']}"
            )
    else:
        await update.message.reply_text("⚠ Image not found.")

async def cart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    cursor.execute("SELECT product FROM cart WHERE user_id=?", (user_id,))
    items = cursor.fetchall()

    if not items:
        await update.message.reply_text("🛒 Your cart is empty.")
        return

    text = "🛍 Your Cart:\n\n"
    total = 0
    cart_count = {}

    for item in items:
        cart_count[item[0]] = cart_count.get(item[0], 0) + 1

    for item, qty in cart_count.items():
        price = products[item]["price"] * qty
        total += price
        text += f"• {item.title()} × {qty} — ₹{price}\n"

    text += "\n--------------------\n"
    text += f"💰 Total: ₹{total}"

    await update.message.reply_text(text)

async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("DELETE FROM cart WHERE user_id=?", (update.message.chat_id,))
    conn.commit()
    await update.message.reply_text("🧹 Cart cleared!")

async def exit_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Session ended. Type /start again anytime.")

# ------------------ MESSAGE HANDLER ------------------
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()
    user_id = update.message.chat_id

    greetings = ["hi", "hello", "hey", "hai", "hlo"]
    if msg in greetings:
        await update.message.reply_text("👋 Hello! How can I help?")
        return

    if msg == "who are you":
        await update.message.reply_text("🤖 I am ShopMate AI — your shopping assistant!")
        return

    if msg in products:
        await send_product_image(update, msg)
        return

    if msg.startswith("add "):
        item = msg.replace("add ", "").strip()
        if item in products:
            cursor.execute("INSERT INTO cart (user_id, product) VALUES (?, ?)", (user_id, item))
            conn.commit()
            await update.message.reply_text(f"✔ {item.title()} added to your cart!")
        else:
            await update.message.reply_text("❌ Item not found!")
        return

    await update.message.reply_text("❓ Type /help to see commands.")

# ------------------ MAIN ------------------
async def main():
    # Create bot instance
    app = ApplicationBuilder().token(TOKEN).request(request).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("products", products_command))
    app.add_handler(CommandHandler("cart", cart_command))
    app.add_handler(CommandHandler("clearcart", clear_cart))
    app.add_handler(CommandHandler("exit", exit_bot))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Start polling
    print("🚀 ShopMate Bot is now running...")
    await app.run_polling()

# ------------------ EXECUTION ------------------
if __name__ == "__main__":
    asyncio.run(main())

