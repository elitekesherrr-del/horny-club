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

VIDEOS = {f"class{i}": i+1 for i in range(1, 41)} # Maine range adjust ki hai

# --- FLASK SERVER (Render ke liye) ---
app_web = Flask(__name__)
@app_web.route('/')
def home(): return "Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# --- BOT FUNCTIONS ---
async def check_join(bot, user_id):
    not_joined = []
    for chan in [CHANNEL_1, CHANNEL_2]:
        try:
            m = await bot.get_chat_member(chan, user_id)
            if m.status not in ["member", "administrator", "creator"]:
                not_joined.append(chan)
        except: not_joined.append(chan)
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

async def text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    
    # Verification check
    if await check_join(context.bot, user_id):
        await update.message.reply_text("⚠️ Please join the channels first!")
        return

    # Button Map
    button_map = {f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖": f"class{i}" for i in range(1, 32)}
    button_map.update({f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31}💝": f"class{i}" for i in range(32, 41)})

    if text in button_map:
        try:
            await context.bot.copy_message(chat_id=update.message.chat_id, 
                                           from_chat_id=STORAGE_CHANNEL_ID, 
                                           message_id=VIDEOS[button_map[text]], 
                                           protect_content=True)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}\n(Bot ko Channel mein Admin banaya hai?)")

async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_buttons))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

def main():
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()
    
