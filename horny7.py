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

# --- CONVINCING MESSAGES (FOR JOINING ONLY) ---
JOIN_MESSAGES = [
    "**⚠️ OH NO BABY! YOU ARE MISSING OUT ON ALL THE WET ACTION. JOIN THE CHANNELS TO SATISFY YOUR HUNGER! 💦👅**",
    "**🔥 DON'T LEAVE ME HANGING! THE REAL HEAT IS INSIDE THE CHANNELS. JOIN NOW, DON'T BE SHY! 😈**",
    "**✨ YOU WANT MORE? I HAVE SO MUCH MORE WAITING FOR YOU INSIDE. JUST JOIN AND SEE! 🫦**"
]

app_web = Flask(__name__)
@app_web.route('/')
def home(): return "Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# --- CORE LOGIC ---
async def check_join(bot, user_id):
    not_joined = []
    for chan, link in [(CHANNEL_1, CHANNEL_1_LINK), (CHANNEL_2, CHANNEL_2_LINK)]:
        try:
            m = await bot.get_chat_member(chan, user_id)
            if m.status not in ["member", "administrator", "creator"]:
                not_joined.append((chan, link))
        except: not_joined.append((chan, link))
    return not_joined

def get_join_keyboard(not_joined):
    keyboard = [[InlineKeyboardButton(f"📢 JOIN {name.replace('@', '')}", url=link)] for name, link in not_joined]
    keyboard.append([InlineKeyboardButton("🔄 VERIFY AGAIN", callback_data="verify")])
    return InlineKeyboardMarkup(keyboard)

def reply_menu():
    keyboard = [["✅ VERIFY ACCESS"]]
    for i in range(1, 32, 2):
        row = [f"💝 HORNY EDITS {i} 💖"]
        if i + 1 <= 31: row.append(f"💝 HORNY EDITS {i+1} 💖")
        keyboard.append(row)
    for i in range(32, 41, 2):
        row = [f"💘 BADDIE {i-31}💝"]
        if i + 1 <= 40: row.append(f"💘 BADDIE {i-30}💝")
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("**💖 PREMIUM EDITS BOT 💖**", reply_markup=reply_menu(), parse_mode=constants.ParseMode.MARKDOWN)
    not_joined = await check_join(context.bot, update.effective_user.id)
    if not_joined:
        await update.message.reply_text(random.choice(JOIN_MESSAGES), reply_markup=get_join_keyboard(not_joined), parse_mode=constants.ParseMode.MARKDOWN)

async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    not_joined = await check_join(context.bot, query.from_user.id)
    if not not_joined:
        await query.message.edit_text("**✅ VERIFICATION SUCCESSFUL! NOW YOU CAN ACCESS ALL CONTENT! 💦**", parse_mode=constants.ParseMode.MARKDOWN)
    else:
        await query.message.edit_text(random.choice(JOIN_MESSAGES), reply_markup=get_join_keyboard(not_joined), parse_mode=constants.ParseMode.MARKDOWN)

async def text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    not_joined = await check_join(context.bot, update.effective_user.id)
    
    # AGAR JOIN NAHI HAI -> HORNY CONVINCING MESSAGE + LINK
    if not_joined:
        await update.message.reply_text(random.choice(JOIN_MESSAGES), reply_markup=get_join_keyboard(not_joined), parse_mode=constants.ParseMode.MARKDOWN)
        return
    
    # AGAR JOIN HAI -> SIRF VIDEO (NO TEXT MESSAGE)
    button_map = {f"💝 HORNY EDITS {i} 💖": f"class{i}" for i in range(1, 32)}
    button_map.update({f"💘 BADDIE {i-31}💝": f"class{i}" for i in range(32, 41)})
    
    if text in button_map:
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
    
