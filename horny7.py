import os
import threading
import asyncio
import random
import json
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- CONFIG ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))  # Set your Telegram user ID as environment variable
SECRET_CODE = "FDJGSLGSGSFJS"  # Admin code to access panel
CHANNEL_1 = "@K3NHA_EMPIRE"
CHANNEL_2 = "@K4NHA_EMPIRE"
CHANNEL_1_LINK = "https://t.me/K3NHA_EMPIRE"
CHANNEL_2_LINK = "https://t.me/K4NHA_EMPIRE"
STORAGE_CHANNEL_ID = -1003945923396

# --- VIDEO MAPPING ---
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

# --- STYLISH MESSAGES ---
JOIN_MESSAGES = [
    "⚠️ 𝙊𝙝 𝙣𝙤 𝙗𝙖𝙗𝙮! 𝙔𝙤𝙪'𝙧𝙚 𝙢𝙞𝙨𝙨𝙞𝙣𝙜 𝙤𝙪𝙩 𝙤𝙣 𝙖𝙡𝙡 𝙩𝙝𝙚 𝙬𝙚𝙩 𝙖𝙘𝙩𝙞𝙤𝙣. 𝙅𝙤𝙞𝙣 𝙩𝙝𝙚 𝙘𝙝𝙖𝙣𝙣𝙚𝙡𝙨 𝙩𝙤 𝙨𝙖𝙩𝙞𝙨𝙛𝙮 𝙮𝙤𝙪𝙧 𝙝𝙪𝙣𝙜𝙚𝙧! 💦👅",
    "🔥 𝘿𝙤𝙣'𝙩 𝙡𝙚𝙖𝙫𝙚 𝙢𝙚 𝙝𝙖𝙣𝙜𝙞𝙣𝙜! 𝙏𝙝𝙚 𝙧𝙚𝙖𝙡 𝙝𝙚𝙖𝙩 𝙞𝙨 𝙞𝙣𝙨𝙞𝙙𝙚 𝙩𝙝𝙚 𝙘𝙝𝙖𝙣𝙣𝙚𝙡𝙨. 𝙅𝙤𝙞𝙣 𝙣𝙤𝙬, 𝙙𝙤𝙣'𝙩 𝙗𝙚 𝙨𝙝𝙮! 😈",
    "✨ 𝙔𝙤𝙪 𝙬𝙖𝙣𝙩 𝙢𝙤𝙧𝙚? 𝙄 𝙝𝙖𝙫𝙚 𝙨𝙤 𝙢𝙪𝙘𝙝 𝙢𝙤𝙧𝙚 𝙬𝙖𝙞𝙩𝙞𝙣𝙜 𝙛𝙤𝙧 𝙮𝙤𝙪 𝙞𝙣𝙨𝙞𝙙𝙚. 𝙅𝙪𝙨𝙩 𝙟𝙤𝙞𝙣 𝙖𝙣𝙙 𝙨𝙚𝙚! 🫦"
]

# --- USER DATA PERSISTENCE ---
USER_DATA_FILE = "users.json"

def load_users():
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

users_db = load_users()  # {user_id: {"username": str, "first_name": str, "last_seen": timestamp}}

def add_user(user_id, username, first_name):
    user_id_str = str(user_id)
    if user_id_str not in users_db:
        users_db[user_id_str] = {
            "username": username or "None",
            "first_name": first_name or "None",
            "last_seen": asyncio.get_event_loop().time()
        }
        save_users(users_db)
    else:
        users_db[user_id_str]["last_seen"] = asyncio.get_event_loop().time()
        save_users(users_db)

# --- FLASK WEB SERVER ---
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
    # Horny edits 1-31
    for i in range(1, 32, 2):
        row = [f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖"]
        if i + 1 <= 31:
            row.append(f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i+1} 💖")
        keyboard.append(row)
    # Baddie 32-40
    for i in range(32, 41, 2):
        row = [f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31}💝"]
        if i + 1 <= 40:
            row.append(f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-30}💝")
        keyboard.append(row)
    # Admin button (only visible to admin)
    if ADMIN_ID:
        keyboard.append(["👑 𝘼𝘿𝙈𝙄𝙉 𝙋𝘼𝙉𝙀𝙇 👑"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def auto_delete_message(context, chat_id, message_id, delay=1800):
    """Delete message after delay (seconds)"""
    await asyncio.sleep(delay)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass  # Message already deleted or permission issue

# --- ADMIN HANDLERS ---
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /admin - only for admin"""
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    await update.message.reply_text(
        "👑 *Admin Panel*\n\nPlease enter the secret code to access.",
        parse_mode="Markdown"
    )
    # Wait for admin to send code
    context.user_data["awaiting_code"] = True

async def handle_admin_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_code"):
        return
    if update.message.text == SECRET_CODE:
        context.user_data["awaiting_code"] = False
        keyboard = [
            [InlineKeyboardButton("📊 View Users", callback_data="admin_users")],
            [InlineKeyboardButton("📢 Broadcast Message", callback_data="admin_broadcast")],
            [InlineKeyboardButton("❌ Close Panel", callback_data="admin_close")]
        ]
        await update.message.reply_text(
            "✅ Access Granted!\n\nChoose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("❌ Wrong code. Access denied.")
        context.user_data["awaiting_code"] = False

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id != ADMIN_ID:
        await query.edit_message_text("❌ Unauthorized.")
        return

    if query.data == "admin_users":
        if not users_db:
            await query.edit_message_text("No users have used the bot yet.")
            return
        # Build user list
        user_list = []
        for uid, info in users_db.items():
            username = info.get("username", "None")
            first_name = info.get("first_name", "None")
            user_list.append(f"👤 {first_name}\n🆔 `{uid}`\n📛 @{username}\n")
        # Split into multiple messages if too long
        msg = "📊 *User List:*\n\n" + "\n".join(user_list)
        if len(msg) > 4000:
            parts = [msg[i:i+4000] for i in range(0, len(msg), 4000)]
            for part in parts:
                await query.message.reply_text(part, parse_mode="Markdown")
            await query.delete_message()
        else:
            await query.edit_message_text(msg, parse_mode="Markdown")

    elif query.data == "admin_broadcast":
        await query.edit_message_text(
            "📢 *Broadcast Mode*\n\nSend me the message you want to broadcast to all users.\n"
            "You can send: text, photo, video, document, or any media.\n"
            "Type /cancel to abort.",
            parse_mode="Markdown"
        )
        context.user_data["broadcast_mode"] = True

    elif query.data == "admin_close":
        await query.edit_message_text("Admin panel closed.")
        context.user_data.pop("broadcast_mode", None)

async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("broadcast_mode"):
        return
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    # Cancel broadcast
    if update.message.text == "/cancel":
        context.user_data.pop("broadcast_mode")
        await update.message.reply_text("Broadcast cancelled.")
        return

    # Get all users
    if not users_db:
        await update.message.reply_text("No users to broadcast to.")
        context.user_data.pop("broadcast_mode")
        return

    total = len(users_db)
    success = 0
    fail = 0
    await update.message.reply_text(f"Broadcasting to {total} users... This may take a while.")

    # For each user, forward the admin's message
    for uid_str, info in users_db.items():
        try:
            uid = int(uid_str)
            # Forward the message from admin to user
            if update.message.text:
                await context.bot.send_message(chat_id=uid, text=update.message.text)
            elif update.message.photo:
                await context.bot.send_photo(chat_id=uid, photo=update.message.photo[-1].file_id, caption=update.message.caption)
            elif update.message.video:
                await context.bot.send_video(chat_id=uid, video=update.message.video.file_id, caption=update.message.caption)
            elif update.message.document:
                await context.bot.send_document(chat_id=uid, document=update.message.document.file_id, caption=update.message.caption)
            else:
                await context.bot.copy_message(chat_id=uid, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
            success += 1
        except Exception as e:
            fail += 1
        await asyncio.sleep(0.05)  # Avoid flood wait

    await update.message.reply_text(f"✅ Broadcast completed!\nSent: {success}\nFailed: {fail}")
    context.user_data.pop("broadcast_mode")

# --- MAIN BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.first_name)
    await update.message.reply_text(
        "💖 𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙀𝘿𝙄𝙏𝙎 𝘽𝙊𝙏 💖\n\nSelect your content below 👇",
        reply_markup=reply_menu()
    )
    not_joined = await check_join(context.bot, user.id)
    if not_joined:
        await update.message.reply_text(random.choice(JOIN_MESSAGES), reply_markup=get_join_keyboard(not_joined))

async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    add_user(user_id, query.from_user.username, query.from_user.first_name)
    not_joined = await check_join(context.bot, user_id)
    if not not_joined:
        await query.message.edit_text("✅ 𝙑𝙚𝙧𝙞𝙛𝙞𝙘𝙖𝙩𝙞𝙤𝙣 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡! 𝙉𝙤𝙬 𝙚𝙣𝙟𝙤𝙮 𝙩𝙝𝙚 𝙫𝙞𝙙𝙚𝙤𝙨!")
    else:
        await query.message.edit_text(random.choice(JOIN_MESSAGES), reply_markup=get_join_keyboard(not_joined))

async def text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    add_user(user_id, update.effective_user.username, update.effective_user.first_name)

    # Handle admin panel button (only visible to admin)
    if text == "👑 𝘼𝘿𝙈𝙄𝙉 𝙋𝘼𝙉𝙀𝙇 👑" and user_id == ADMIN_ID:
        await admin_panel(update, context)
        return

    # Handle verify access
    if text == "✅ 𝙑𝙀𝙍𝙄𝙁𝙔 𝘼𝘾𝘾𝙀𝙎𝙎":
        not_joined = await check_join(context.bot, user_id)
        if not not_joined:
            await update.message.reply_text("✅ Verification Successful!\n\nNow you can use all buttons 💖")
        else:
            await update.message.reply_text(random.choice(JOIN_MESSAGES), reply_markup=get_join_keyboard(not_joined))
        return

    # For other buttons, check join status
    not_joined = await check_join(context.bot, user_id)
    if not_joined:
        await update.message.reply_text(random.choice(JOIN_MESSAGES), reply_markup=get_join_keyboard(not_joined))
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
                # Send video
                sent_msg = await context.bot.copy_message(
                    chat_id=update.message.chat_id,
                    from_chat_id=STORAGE_CHANNEL_ID,
                    message_id=VIDEOS[key],
                    protect_content=True
                )
                # Schedule auto-delete after 30 minutes (1800 seconds)
                asyncio.create_task(auto_delete_message(context, sent_msg.chat_id, sent_msg.message_id, delay=1800))
            except Exception as e:
                await update.message.reply_text(f"❌ Error: {e}")
        else:
            await update.message.reply_text("❌ Video not found.")

async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Restart the bot 💖"),
        BotCommand("admin", "Admin panel (admin only)")
    ])

# --- MAIN ---
async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))
    app.add_handler(CallbackQueryHandler(admin_callback, pattern="^admin_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(r"^👑"), admin_panel))  # fallback for button
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_code))
    app.add_handler(MessageHandler(filters.ALL, handle_broadcast))  # handle broadcast messages (text, photo, video, etc.)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_buttons))
    app.post_init = set_commands
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

def main():
    if not ADMIN_ID:
        print("⚠️ WARNING: ADMIN_ID not set. Admin features disabled.")
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()
