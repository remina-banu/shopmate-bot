# ShopMate Telegram Bot 🤖🛍

ShopMate is a Telegram-based shopping assistant chatbot that allows users to browse products, view prices, and interact with a simple conversational interface.
The bot is built using **Python** and the **Telegram Bot API** and stores product information using an **SQLite database**.

This project demonstrates chatbot development, database integration, and Telegram bot automation.

## 🚀 Features

* Browse products by category
* View product prices
* Receive product images
* Simple chatbot responses for user queries
* Product data stored using SQLite database
* Natural language response support using NLTK

## 🛠 Tech Stack

* Python 3
* python-telegram-bot
* SQLite
* NLTK (Natural Language Toolkit)


## 📂 Project Structure

```
shopmate/
│
├── images/                           # Product images
├── Shopping-Assistant-Chatbot.py     # Main Telegram bot script
├── download_nltk.py                  # Script to download required NLTK data
├── shopmate.db                       # SQLite database
└── README.md                         # Project documentation
```

## ⚙️ Installation

### 1️⃣ Clone the Repository

```
git clone https://github.com/yourusername/shopmate-bot.git
cd shopmate-bot
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Create a Telegram Bot

Create a bot using **BotFather** in Telegram and get the **Bot Token**.

Replace the token in the Python file:

```
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

---

### 4️⃣ Run the Bot

```
python Shopping-Assistant-Chatbot.py
```

Your bot will start running and respond to users on Telegram.

---

## 💬 Example Commands

```
/start
/help
/products
/categories
```

---

## 🔮 Future Improvements

* Product search functionality
* Payment gateway integration
* AI-based product recommendations
* Admin panel for managing products

---

## 👩‍💻 Author

**Remina Banu S**
B.Tech Information Technology

---

## 📌 Project Purpose

This project was developed as a learning project to demonstrate:

* Telegram bot development
* Python backend programming
* Database integration
* Basic chatbot interaction
