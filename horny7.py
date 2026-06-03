import os
import threading
import asyncio
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, BotCommand
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
)

# --- BOT CONFIG ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_1 = "@K3NHA_EMPIRE"
CHANNEL_2 = "@K4NHA_EMPIRE"
CHANNEL_1_LINK = "https://t.me/K3NHA_EMPIRE"
CHANNEL_2_LINK = "https://t.me/K4NHA_EMPIRE"
STORAGE_CHANNEL_ID = -1003945923396

# --- FLASK SERVER ---
app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# --- YOUR FUNCTIONS ---
async def check_join(bot, user_id):
    not_joined = []
    for name, link in [("CHANNEL 1", CHANNEL_1), ("CHANNEL 2", CHANNEL_2)]:
        try:
            member = await bot.get_chat_member(link, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append((name, CHANNEL_1_LINK if "1" in name else CHANNEL_2_LINK))
        except:
            not_joined.append((name, CHANNEL_1_LINK if "1" in name else CHANNEL_2_LINK))
    return not_joined

def reply_menu():
    keyboard = [["✅ VERIFY ACCESS"]]
    for i in range(1, 32, 2):
        row = [f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖"]
        if i + 1 <= 31: row.append(f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i+1} 💖")
        keyboard.append(row)
    for i in range(32, 41, 2):
        row = [f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31}💝"]
        if i + 1 <= 40: row.append(f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-30}💝")
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💖 PREMIUM EDITS BOT 💖\n\nSelect your content below 👇", reply_markup=reply_menu())

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "verify":
        await query.message.reply_text("✅ Verification logic triggered!")

async def text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Simple logic to match your buttons
    if "𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎" in text or "𝘽𝘼𝘿𝘿𝙄𝙀" in text:
        await update.message.reply_text("Button clicked: " + text)

async def set_menu(app):
    await app.bot.set_my_commands([BotCommand("start", "Restart The Bot 💖")])

# --- MAIN LOOP ---
async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_buttons))
    app.post_init = set_menu
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

def main():
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()
    
