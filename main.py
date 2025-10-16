import requests  
from telegram import Update  
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes  
  
BOT_TOKEN = "8471846428:AAF1f0wfZN1RykD_ILvxzyozUEtBAvrhAXg"  

def get_price(address):  
    url = f"https://public-api.birdeye.so/public/price?address={address}"  
    headers = {"x-chain": "solana"}  
    try:  
        response = requests.get(url, headers=headers).json()  
        return response["data"]["value"]  
    except:  
        return None  
  
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    await update.message.reply_text(  
        "🌟 Welcome to Solana Pulse Bot!\n"  
        "Track Solana token prices in real-time.\n\n"  
        "📊 /price <contract_address>\n"  
        "Example: /price So11111111111111111111111111111111111111112 (SOL)\n\n"  
        "Let's get started 🚀"  
    )  
  
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    if not context.args:  
        await update.message.reply_text("Usage: /price <contract_address>")  
        return  
  
    address = context.args[0]  
    value = get_price(address)  
    if value:  
        await update.message.reply_text(f"💰 Current Price: ${value:.4f}")  
    else:  
        await update.message.reply_text("❌ Could not fetch price. Try again.")  
  
app = ApplicationBuilder().token(BOT_TOKEN).build()  
app.add_handler(CommandHandler("start", start))  
app.add_handler(CommandHandler("price", price))  
  
print("🤖 Bot is running...")  
app.run_polling()
