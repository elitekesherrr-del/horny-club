import os
import threading
import asyncio
import random
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, constants
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- CONFIG ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_1 = "@K3NHA_EMPIRE"
CHANNEL_2 = "@K4NHA_EMPIRE"
CHANNEL_1_LINK = "https://t.me/K3NHA_EMPIRE"
CHANNEL_2_LINK = "https://t.me/K4NHA_EMPIRE"
STORAGE_CHANNEL_ID = -1003945923396
VIDEOS = {f"class{i}": i+1 for i in range(1, 41)}

# --- SPICY MESSAGES (FOR VIDEO) ---
SPICY_MESSAGES = [
    "**Uff, here is your favorite video! Getting hot in here, right? 🥵💦**",
    "**It is hard to control yourself after watching this... enjoy baby! 😈🔥**",
    "**I stole the hottest and spiciest edit just for you. Don't forget to enjoy! 🍆💦**",
    "**Forget the stress, here is the spicy video you were waiting for! 👅✨**",
    "**This is a super sexy video, watch it fully and feel the heat! 😉🔥**"
]

# --- SPICY JOIN MESSAGE ---
JOIN_TEXT = "**⚠️ Attention Baby! To unlock all the spicy content and satisfy your desires, you MUST join these channels first. Don't be shy, join now! 💦🔥**"

app_web = Flask(__name__)
@app_web.route('/')
def home(): return "Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# --- LOGIC ---
async def check_join(bot, user_id):
    not_joined = []
    for chan, link in [(CHANNEL_1, CHANNEL_1_LINK), (CHANNEL_2, CHANNEL_2_LINK)]:
        try:
            m = await bot.get_chat_member(chan, user_id)
            if m.status not in ["member", "administrator", "creator"]:
                not_joined.append((chan, link))
        except: not_joined.append((chan, link))
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
    await update.message.reply_text("💖 PREMIUM EDITS BOT 💖", reply_markup=reply_menu())
    keyboard = [[InlineKeyboardButton("📢 JOIN CHANNEL 1", url=CHANNEL_1_LINK)], 
                [InlineKeyboardButton("📢 JOIN CHANNEL 2", url=CHANNEL_2_LINK)], 
                [InlineKeyboardButton("✅ VERIFY ACCESS", callback_data="verify")]]
    await update.message.reply_text(JOIN_TEXT, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=constants.ParseMode.MARKDOWN)

async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    not_joined = await check_join(context.bot, query.from_user.id)
    if not_joined:
        keyboard = [[InlineKeyboardButton(f"📢 JOIN {name.replace('@', '')}", url=link)] for name, link in not_joined]
        keyboard.append([InlineKeyboardButton("🔄 VERIFY AGAIN", callback_data="verify")])
        await query.message.edit_text("**❌ Still not joined? You are missing out on the heat! Join now to unlock:**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=constants.ParseMode.MARKDOWN)
    else:
        await query.message.edit_text("✅ **Verification Successful! Now go and enjoy your spicy content! 💦**", parse_mode=constants.ParseMode.MARKDOWN)

async def text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    not_joined = await check_join(context.bot, update.effective_user.id)
    if not_joined:
        keyboard = [[InlineKeyboardButton(f"📢 JOIN {name.replace('@', '')}", url=link)] for name, link in not_joined]
        keyboard.append([InlineKeyboardButton("🔄 VERIFY AGAIN", callback_data="verify")])
        await update.message.reply_text(f"**⚠️ Hey baby! You left the channel. Join again to keep the heat alive:**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=constants.ParseMode.MARKDOWN)
        return
    
    button_map = {f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖": f"class{i}" for i in range(1, 32)}
    button_map.update({f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31}💝": f"class{i}" for i in range(32, 41)})
    
    if text in button_map:
        await update.message.reply_text(random.choice(SPICY_MESSAGES), parse_mode=constants.ParseMode.MARKDOWN)
        await context.bot.copy_message(update.message.chat_id, STORAGE_CHANNEL_ID, VIDEOS[button_map[text]], protect_content=True)

async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))
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
    
