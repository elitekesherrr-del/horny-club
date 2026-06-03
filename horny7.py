import os
import threading
import asyncio
from flask import Flask
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, BotCommand
)
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

# --- VIDEO IDS ---
VIDEOS = {f"class{i}": i+1 for i in range(1, 14)}
VIDEOS.update({f"class{i}": i+19 for i in range(14, 41)})

# --- YOUR LOGIC FUNCTIONS ---
async def check_join(bot, user_id):
    not_joined = []
    for name, link in [("CHANNEL 1", CHANNEL_1), ("CHANNEL 2", CHANNEL_2)]:
        try:
            member = await bot.get_chat_member(link, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append((name, CHANNEL_1_LINK if name=="CHANNEL 1" else CHANNEL_2_LINK))
        except:
            not_joined.append((name, CHANNEL_1_LINK if name=="CHANNEL 1" else CHANNEL_2_LINK))
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
        not_joined = await check_join(context.bot, query.from_user.id)
        if not not_joined:
            await query.message.reply_text("✅ Verification Successful!")
        else:
            await query.message.reply_text("❌ Join channels first!")

async def text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Yahan wahi button map logic hai jo aapke purane script mein tha
    button_map = {f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖": f"class{i}" for i in range(1, 32)}
    button_map.update({f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31}💝": f"class{i}" for i in range(32, 41)})
    
    if text in button_map:
        key = button_map[text]
        await context.bot.copy_message(chat_id=update.message.chat_id, from_chat_id=STORAGE_CHANNEL_ID, message_id=VIDEOS[key], protect_content=True)

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
import os
import threading
import asyncio
from flask import Flask
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, BotCommand
)
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

# --- VIDEO IDS ---
VIDEOS = {f"class{i}": i+1 for i in range(1, 14)}
VIDEOS.update({f"class{i}": i+19 for i in range(14, 41)})

# --- YOUR LOGIC FUNCTIONS ---
async def check_join(bot, user_id):
    not_joined = []
    for name, link in [("CHANNEL 1", CHANNEL_1), ("CHANNEL 2", CHANNEL_2)]:
        try:
            member = await bot.get_chat_member(link, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append((name, CHANNEL_1_LINK if name=="CHANNEL 1" else CHANNEL_2_LINK))
        except:
            not_joined.append((name, CHANNEL_1_LINK if name=="CHANNEL 1" else CHANNEL_2_LINK))
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
        not_joined = await check_join(context.bot, query.from_user.id)
        if not not_joined:
            await query.message.reply_text("✅ Verification Successful!")
        else:
            await query.message.reply_text("❌ Join channels first!")

async def text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Yahan wahi button map logic hai jo aapke purane script mein tha
    button_map = {f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖": f"class{i}" for i in range(1, 32)}
    button_map.update({f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31}💝": f"class{i}" for i in range(32, 41)})
    
    if text in button_map:
        key = button_map[text]
        await context.bot.copy_message(chat_id=update.message.chat_id, from_chat_id=STORAGE_CHANNEL_ID, message_id=VIDEOS[key], protect_content=True)

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
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def send_join_message(message):
    keyboard = [[InlineKeyboardButton("📢 JOIN CHANNEL 1", url=CHANNEL_1_LINK)],
                [InlineKeyboardButton("📢 JOIN CHANNEL 2", url=CHANNEL_2_LINK)],
                [InlineKeyboardButton("✅ VERIFY", callback_data="verify")]]
    await message.reply_text("⚠️ First join both channels to unlock the bot.", reply_markup=InlineKeyboardMarkup(keyboard))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💖 PREMIUM EDITS BOT 💖\n\nSelect your content below 👇", reply_markup=reply_menu())
    await send_join_message(update.message)

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if query.data == "verify":
        not_joined = await check_join(context.bot, user_id)
        if not not_joined:
            await query.message.reply_text("✅ Verification Successful\n\nNow you can use all bot buttons 💖")
        else:
            keyboard = [[InlineKeyboardButton(f"📢 JOIN {name}", url=link)] for name, link in not_joined]
            keyboard.append([InlineKeyboardButton("🔄 VERIFY AGAIN", callback_data="verify")])
            await query.message.reply_text("❌ You have not joined:", reply_markup=InlineKeyboardMarkup(keyboard))

async def text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    not_joined = await check_join(context.bot, user_id)
    if not_joined:
        keyboard = [[InlineKeyboardButton(f"📢 JOIN {name}", url=link)] for name, link in not_joined]
        keyboard.append([InlineKeyboardButton("🔄 VERIFY AGAIN", callback_data="verify")])
        await update.message.reply_text("⚠️ Join both channels to use the bot.", reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    # Button Map
    button_map = {f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖": f"class{i}" for i in range(1, 32)}
    button_map.update({f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31}💝": f"class{i}" for i in range(32, 41)})
    
    if text in button_map:
        try:
            await context.bot.copy_message(chat_id=update.message.chat_id, from_chat_id=STORAGE_CHANNEL_ID, message_id=VIDEOS[button_map[text]], protect_content=True)
        except Exception as e:
            await update.message.reply_text(f"❌ ERROR: {e}")

async def set_menu(app):
    await app.bot.set_my_commands([BotCommand("start", "Restart The Bot 💖")])

def main():
    if not BOT_TOKEN:
        print("CRITICAL ERROR: BOT_TOKEN is missing!")
        return
    
    threading.Thread(target=run_web, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_buttons))
    app.post_init = set_menu
    print("✅ BOT STARTED SUCCESSFULLY")
    app.run_polling()

if __name__ == "__main__":
    main()
    
