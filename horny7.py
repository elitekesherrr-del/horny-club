import os
import threading
import asyncio
import random
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- CONFIG ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_1 = "@K3NHA_EMPIRE"
CHANNEL_2 = "@K4NHA_EMPIRE"
CHANNEL_1_LINK = "https://t.me/K3NHA_EMPIRE"
CHANNEL_2_LINK = "https://t.me/K4NHA_EMPIRE"
STORAGE_CHANNEL_ID = -1003945923396

# --- CORRECT VIDEO MAPPING (from working script) ---
VIDEOS = {
    "class1": 2,
    "class2": 3,
    "class3": 4,
    "class4": 5,
    "class5": 6,
    "class6": 7,
    "class7": 8,
    "class8": 9,
    "class9": 10,
    "class10": 11,
    "class11": 12,
    "class12": 13,
    "class13": 14,
    "class14": 33,
    "class15": 34,
    "class16": 35,
    "class17": 36,
    "class18": 37,
    "class19": 38,
    "class20": 39,
    "class21": 40,
    "class22": 41,
    "class23": 42,
    "class24": 43,
    "class25": 44,
    "class26": 45,
    "class27": 46,
    "class28": 47,
    "class29": 48,
    "class30": 49,
    "class31": 50,
    "class32": 51,
    "class33": 52,
    "class34": 53,
    "class35": 54,
    "class36": 55,
    "class37": 56,
    "class38": 57,
    "class39": 58,
    "class40": 59
}

# --- STYLISH MESSAGES ---
JOIN_MESSAGES = [
    "⚠️ 𝙊𝙝 𝙣𝙤 𝙗𝙖𝙗𝙮! 𝙔𝙤𝙪'𝙧𝙚 𝙢𝙞𝙨𝙨𝙞𝙣𝙜 𝙤𝙪𝙩 𝙤𝙣 𝙖𝙡𝙡 𝙩𝙝𝙚 𝙬𝙚𝙩 𝙖𝙘𝙩𝙞𝙤𝙣. 𝙅𝙤𝙞𝙣 𝙩𝙝𝙚 𝙘𝙝𝙖𝙣𝙣𝙚𝙡𝙨 𝙩𝙤 𝙨𝙖𝙩𝙞𝙨𝙛𝙮 𝙮𝙤𝙪𝙧 𝙝𝙪𝙣𝙜𝙚𝙧! 💦👅",
    "🔥 𝘿𝙤𝙣'𝙩 𝙡𝙚𝙖𝙫𝙚 𝙢𝙚 𝙝𝙖𝙣𝙜𝙞𝙣𝙜! 𝙏𝙝𝙚 𝙧𝙚𝙖𝙡 𝙝𝙚𝙖𝙩 𝙞𝙨 𝙞𝙣𝙨𝙞𝙙𝙚 𝙩𝙝𝙚 𝙘𝙝𝙖𝙣𝙣𝙚𝙡𝙨. 𝙅𝙤𝙞𝙣 𝙣𝙤𝙬, 𝙙𝙤𝙣'𝙩 𝙗𝙚 𝙨𝙝𝙮! 😈",
    "✨ 𝙔𝙤𝙪 𝙬𝙖𝙣𝙩 𝙢𝙤𝙧𝙚? 𝙄 𝙝𝙖𝙫𝙚 𝙨𝙤 𝙢𝙪𝙘𝙝 𝙢𝙤𝙧𝙚 𝙬𝙖𝙞𝙩𝙞𝙣𝙜 𝙛𝙤𝙧 𝙮𝙤𝙪 𝙞𝙣𝙨𝙞𝙙𝙚. 𝙅𝙪𝙨𝙩 𝙟𝙤𝙞𝙣 𝙖𝙣𝙙 𝙨𝙚𝙚! 🫦"
]

# --- FLASK WEB SERVER (for Render/Railway) ---
app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# --- HELPER FUNCTIONS ---
async def check_join(bot, user_id):
    not_joined = []
    for chan, link in [(CHANNEL_1, CHANNEL_1_LINK), (CHANNEL_2, CHANNEL_2_LINK)]:
        try:
            m = await bot.get_chat_member(chan, user_id)
            if m.status not in ["member", "administrator", "creator"]:
                not_joined.append((chan, link))
        except:
            not_joined.append((chan, link))
    return not_joined

def get_join_keyboard(not_joined):
    keyboard = [[InlineKeyboardButton(f"📢 𝙅𝙊𝙄𝙉 {name.replace('@', '')}", url=link)] for name, link in not_joined]
    keyboard.append([InlineKeyboardButton("🔄 𝙑𝙀𝙍𝙄𝙁𝙔 𝘼𝙂𝘼𝙄𝙉", callback_data="verify")])
    return InlineKeyboardMarkup(keyboard)

def reply_menu():
    keyboard = [["✅ 𝙑𝙀𝙍𝙄𝙁𝙔 𝘼𝘾𝘾𝙀𝙎𝙎"]]
    # Horny edits 1 to 31
    for i in range(1, 32, 2):
        row = [f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖"]
        if i + 1 <= 31:
            row.append(f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i+1} 💖")
        keyboard.append(row)
    # Baddie edits 32 to 40
    for i in range(32, 41, 2):
        row = [f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31}💝"]
        if i + 1 <= 40:
            row.append(f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-30}💝")
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# --- BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💖 𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙀𝘿𝙄𝙏𝙎 𝘽𝙊𝙏 💖\n\nSelect your content below 👇",
        reply_markup=reply_menu()
    )
    not_joined = await check_join(context.bot, update.effective_user.id)
    if not_joined:
        await update.message.reply_text(random.choice(JOIN_MESSAGES), reply_markup=get_join_keyboard(not_joined))

async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    not_joined = await check_join(context.bot, query.from_user.id)
    if not not_joined:
        await query.message.edit_text("✅ 𝙑𝙚𝙧𝙞𝙛𝙞𝙘𝙖𝙩𝙞𝙤𝙣 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡! 𝙉𝙤𝙬 𝙚𝙣𝙟𝙤𝙮 𝙩𝙝𝙚 𝙫𝙞𝙙𝙚𝙤𝙨!")
    else:
        await query.message.edit_text(random.choice(JOIN_MESSAGES), reply_markup=get_join_keyboard(not_joined))

async def text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    # Handle "VERIFY ACCESS" button
    if text == "✅ 𝙑𝙀𝙍𝙄𝙁𝙔 𝘼𝘾𝘾𝙀𝙎𝙎":
        not_joined = await check_join(context.bot, user_id)
        if not not_joined:
            await update.message.reply_text("✅ Verification Successful!\n\nNow you can use all buttons 💖")
        else:
            await update.message.reply_text(
                random.choice(JOIN_MESSAGES),
                reply_markup=get_join_keyboard(not_joined)
            )
        return

    # For other buttons, check join status first
    not_joined = await check_join(context.bot, user_id)
    if not_joined:
        await update.message.reply_text(
            random.choice(JOIN_MESSAGES),
            reply_markup=get_join_keyboard(not_joined)
        )
        return

    # Map button text to class key
    button_map = {}
    for i in range(1, 32):
        button_map[f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖"] = f"class{i}"
    for i in range(32, 41):
        button_map[f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31}💝"] = f"class{i}"

    if text in button_map:
        key = button_map[text]
        if key in VIDEOS:
            try:
                await context.bot.copy_message(
                    chat_id=update.message.chat_id,
                    from_chat_id=STORAGE_CHANNEL_ID,
                    message_id=VIDEOS[key],
                    protect_content=True
                )
            except Exception as e:
                await update.message.reply_text(f"❌ Error: {e}")
        else:
            await update.message.reply_text("❌ Video not found.")

async def set_commands(app):
    await app.bot.set_my_commands([BotCommand("start", "Restart the bot 💖")])

async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_buttons))
    app.post_init = set_commands
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()  # Keep running

def main():
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()
