import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8677583656:AAHKRBtog2egYTbJxzP9mt9tHcH-VqUrPaI"

# -------- BTC PRICE --------
def get_btc():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        r = requests.get(url).json()
        price = float(r["price"])

        return f"📊 Bitcoin (BTC)\n\n💰 Precio: ${price:,.2f}"

    except:
        return "⚠️ No pude obtener el precio."

# -------- PRICE ANY CRYPTO --------
def get_price(symbol):

    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}USDT"
        r = requests.get(url).json()

        price = float(r["price"])

        return f"💰 {symbol.upper()}\n\nPrecio: ${price:,.4f}"

    except:
        return "⚠️ Crypto no encontrada."

# -------- FEAR & GREED --------
def get_fg():

    try:
        url = "https://api.alternative.me/fng/"
        r = requests.get(url).json()

        value = r["data"][0]["value"]
        status = r["data"][0]["value_classification"]

        return f"""
😱 Fear & Greed Index

Valor: {value}/100
Estado: {status}
"""

    except:
        return "⚠️ No pude obtener Fear & Greed."

# -------- NEWS --------
def get_news():
    try:
        url = "https://news.google.com/rss/search?q=crypto+bitcoin&hl=en-US&gl=US&ceid=US:en"

        r = requests.get(url)

        import xml.etree.ElementTree as ET

        root = ET.fromstring(r.content)

        news = "📰 Noticias Crypto\n\n"

        items = root.findall(".//item")[:3]

        for item in items:
            title = item.find("title").text
            link = item.find("link").text

            news += f"• {title}\n{link}\n\n"

        return news

    except:
        return "⚠️ No pude obtener noticias."
# -------- TOP 10 CRYPTO --------
def get_top():

    try:

        coins = [
            "BTCUSDT",
            "ETHUSDT",
            "BNBUSDT",
            "SOLUSDT",
            "XRPUSDT",
            "ADAUSDT",
            "DOGEUSDT",
            "AVAXUSDT",
            "DOTUSDT",
            "LINKUSDT"
        ]

        text = "📊 Top Cryptos\n\n"

        for coin in coins:

            url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin}"
            r = requests.get(url).json()

            price = float(r["price"])

            symbol = coin.replace("USDT","")

            text += f"{symbol} — ${price:,.2f}\n"

        return text

    except:
        return "⚠️ No pude obtener el top."
# -------- MAYER MULTIPLE --------
def get_mayer():

    try:

        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=200"
        r = requests.get(url).json()

        closes = [float(x[4]) for x in r]

        ma200 = sum(closes) / len(closes)

        price = closes[-1]

        mayer = price / ma200

        if mayer < 1:
            status = "🟢 BTC barato"
        elif mayer < 2.4:
            status = "🟡 Mercado normal"
        else:
            status = "🔴 Mercado sobrecalentado"

        return f"""
📉 Mayer Multiple

BTC Price: ${price:,.2f}
MA200: ${ma200:,.2f}

Mayer Multiple: {mayer:.2f}

Estado: {status}
"""

    except:
        return "⚠️ No pude calcular el Mayer Multiple."
# -------- COMMANDS --------

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_btc())

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text("Uso: /price btc")
        return

    symbol = context.args[0]
    await update.message.reply_text(get_price(symbol))

async def fg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_fg())

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_news())

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_top())

async def mayer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_mayer())

# -------- MAIN --------

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("fg", fg))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(CommandHandler("mayer", mayer))

    print("Bot funcionando...")

    app.run_polling()

if __name__ == "__main__":
    main()