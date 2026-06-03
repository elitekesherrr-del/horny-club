import os
import threading
from flask import Flask
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    BotCommand
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# --- BOT CONFIG ---
# Token ab Render ke Environment Variables se aayega
BOT_TOKEN = os.environ.get("BOT_TOKEN")

CHANNEL_1 = "@K3NHA_EMPIRE"
CHANNEL_2 = "@K4NHA_EMPIRE"
CHANNEL_1_LINK = "https://t.me/K3NHA_EMPIRE"
CHANNEL_2_LINK = "https://t.me/K4NHA_EMPIRE"
STORAGE_CHANNEL_ID = -1003945923396

# --- FLASK SERVER (Render ke liye zaroori) ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- VIDEO IDS ---
VIDEOS = {
    "class1": 2, "class2": 3, "class3": 4, "class4": 5, "class5": 6,
    "class6": 7, "class7": 8, "class8": 9, "class9": 10, "class10": 11,
    "class11": 12, "class12": 13, "class13": 14, "class14": 33, "class15": 34,
    "class16": 35, "class17": 36, "class18": 37, "class19": 38, "class20": 39,
    "class21": 40, "class22": 41, "class23": 42, "class24": 43, "class25": 44,
    "class26": 45, "class27": 46, "class28": 47, "class29": 48, "class30": 49,
    "class31": 50, "class32": 51, "class33": 52, "class34": 53, "class35": 54,
    "class36": 55, "class37": 56, "class38": 57, "class39": 58, "class40": 59
}

# --- YOUR EXISTING LOGIC ---
async def check_join(bot, user_id):
    not_joined = []
    try:
        member1 = await bot.get_chat_member(CHANNEL_1, user_id)
        if member1.status not in ["member", "administrator", "creator"]:
            not_joined.append(("CHANNEL 1", CHANNEL_1_LINK))
    except:
        not_joined.append(("CHANNEL 1", CHANNEL_1_LINK))
    try:
        member2 = await bot.get_chat_member(CHANNEL_2, user_id)
        if member2.status not in ["member", "administrator", "creator"]:
            not_joined.append(("CHANNEL 2", CHANNEL_2_LINK))
    except:
        not_joined.append(("CHANNEL 2", CHANNEL_2_LINK))
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
    
