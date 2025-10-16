import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get bot token from environment variable (DO NOT hardcode token)
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise SystemExit("ERROR: BOT_TOKEN environment variable not set")

# Birdeye public price endpoint for Solana tokens
def get_price_by_address(address):
    url = f"https://public-api.birdeye.so/public/price?address={address}"
    headers = {"x-chain": "solana"}
    try:
        r = requests.get(url, headers=headers, timeout=8)
        r.raise_for_status()
        data = r.json()
        return data.get("data", {}).get("value")
    except Exception as e:
        print("Price fetch error:", e)
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 Welcome to Solana Pulse Bot!\n"
        "Track Solana token prices in real-time.\n\n"
        "📊 /price <contract_address>\n"
        "Example: /price So11111111111111111111111111111111111111112 (SOL)\n\n"
        "🔔 /help for commands."
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/price <contract_address> - get current price\n"
        "/start - welcome message\n"
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /price <contract_address>")
        return

    address = context.args[0].strip()
    value = get_price_by_address(address)
    if value is None:
        await update.message.reply_text("❌ Could not fetch price. Try again later.")
    else:
        await update.message.reply_text(f"💰 Current Price: ${float(value):.6f}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("price", price))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()