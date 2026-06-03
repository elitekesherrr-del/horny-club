import os
import threading
import asyncio
import random
import json
from flask import Flask
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, BotCommand
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

# ==================== CONFIG ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    BOT_TOKEN = "8896492850:AAG429hyCEgWWSJuAH05inAhVxoPYdjlTRE"  # fallback (remove in production)

SECRET_CODE = "FDJGSLGSGSFJS"

CHANNEL_1 = "@K3NHA_EMPIRE"
CHANNEL_2 = "@K4NHA_EMPIRE"
CHANNEL_1_LINK = "https://t.me/K3NHA_EMPIRE"
CHANNEL_2_LINK = "https://t.me/K4NHA_EMPIRE"
STORAGE_CHANNEL_ID = -1003945923396

# ==================== VIDEO IDS (EXACTLY FROM YOUR WORKING SCRIPT) ====================
VIDEOS = {
    "class1": 2, "class2": 3, "class3": 4, "class4": 5, "class5": 6,
    "class6": 7, "class7": 8, "class8": 9, "class9": 10, "class10": 11,
    "class11": 12, "class12": 13, "class13": 14,
    "class14": 33, "class15": 34, "class16": 35, "class17": 36, "class18": 37,
    "class19": 38, "class20": 39, "class21": 40, "class22": 41, "class23": 42,
    "class24": 43, "class25": 44, "class26": 45, "class27": 46, "class28": 47,
    "class29": 48, "class30": 49, "class31": 50,
    "class32": 51, "class33": 52, "class34": 53, "class35": 54, "class36": 55,
    "class37": 56, "class38": 57, "class39": 58, "class40": 59
}

# ==================== USER DATA ====================
USER_FILE = "users.json"

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

users_db = load_users()

def add_user(user_id, username, first_name):
    uid = str(user_id)
    if uid not in users_db:
        users_db[uid] = {
            "username": username or "None",
            "first_name": first_name or "None",
            "last_seen": asyncio.get_event_loop().time()
        }
        save_users(users_db)
    else:
        users_db[uid]["last_seen"] = asyncio.get_event_loop().time()
        save_users(users_db)

# ==================== FLASK WEB SERVER ====================
app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# ==================== CHECK JOIN (YOUR EXACT CODE) ====================
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

# ==================== REPLY KEYBOARD (YOUR EXACT CODE + ADMIN BUTTON) ====================
def reply_menu():
    keyboard = [["✅ VERIFY ACCESS"]]
    # Horny edits 1-31
    for i in range(1, 32, 2):
        row = []
        row.append(f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖")
        if i + 1 <= 31:
            row.append(f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i+1} 💖")
        keyboard.append(row)
    # Baddie 32-40
    for i in range(32, 41, 2):
        row = []
        row.append(f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31}💝")
        if i + 1 <= 40:
            row.append(f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-30}💝")
        keyboard.append(row)
    # Admin button (visible to all, but code protected)
    keyboard.append(["👑 ADMIN PANEL 👑"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ==================== SEND JOIN MESSAGE (YOUR EXACT CODE) ====================
async def send_join_message(message):
    keyboard = [
        [InlineKeyboardButton("📢 JOIN CHANNEL 1", url=CHANNEL_1_LINK)],
        [InlineKeyboardButton("📢 JOIN CHANNEL 2", url=CHANNEL_2_LINK)],
        [InlineKeyboardButton("✅ VERIFY", callback_data="verify")]
    ]
    await message.reply_text(
        "⚠️ First join both channels to unlock the bot.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ==================== AUTO DELETE VIDEO ====================
async def auto_delete_message(context, chat_id, message_id, delay=1800):
    await asyncio.sleep(delay)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass

# ==================== ADMIN PANEL (CODE PROTECTED) ====================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 *Admin Panel*\n\nSend the secret code to continue.",
        parse_mode="Markdown"
    )
    context.user_data["awaiting_code"] = True

async def handle_admin_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_code"):
        return
    if update.message.text == SECRET_CODE:
        context.user_data["awaiting_code"] = False
        keyboard = [
            [InlineKeyboardButton("📊 View Users", callback_data="admin_users")],
            [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
            [InlineKeyboardButton("🔧 Test Storage", callback_data="admin_test")],
            [InlineKeyboardButton("❌ Close", callback_data="admin_close")]
        ]
        await update.message.reply_text(
            "✅ Access granted!\nChoose option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("❌ Wrong code. Access denied.")
        context.user_data["awaiting_code"] = False

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "admin_users":
        if not users_db:
            await query.edit_message_text("No users yet.")
            return
        msg = "📊 *Users:*\n\n"
        for uid, info in users_db.items():
            uname = info.get("username", "None")
            fname = info.get("first_name", "None")
            msg += f"👤 {fname}\n🆔 `{uid}`\n📛 @{uname}\n\n"
        if len(msg) > 4000:
            for i in range(0, len(msg), 4000):
                await query.message.reply_text(msg[i:i+4000], parse_mode="Markdown")
            await query.delete_message()
        else:
            await query.edit_message_text(msg, parse_mode="Markdown")
    elif query.data == "admin_broadcast":
        await query.edit_message_text(
            "📢 *Broadcast Mode*\nSend any message (text/photo/video).\nType /cancel to abort.",
            parse_mode="Markdown"
        )
        context.user_data["broadcast_mode"] = True
    elif query.data == "admin_test":
        await query.edit_message_text("Testing storage channel...")
        try:
            test = await context.bot.forward_message(
                chat_id=query.from_user.id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_id=2,
                protect_content=True
            )
            await context.bot.delete_message(query.from_user.id, test.message_id)
            await query.edit_message_text("✅ Storage channel works.")
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")
    elif query.data == "admin_close":
        await query.edit_message_text("Panel closed.")
        context.user_data.pop("broadcast_mode", None)

async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("broadcast_mode"):
        return
    if update.message.text == "/cancel":
        context.user_data.pop("broadcast_mode")
        await update.message.reply_text("Broadcast cancelled.")
        return
    if not users_db:
        await update.message.reply_text("No users.")
        context.user_data.pop("broadcast_mode")
        return
    total = len(users_db)
    success = 0
    fail = 0
    await update.message.reply_text(f"Broadcasting to {total} users...")
    for uid_str in users_db:
        try:
            uid = int(uid_str)
            if update.message.text:
                await context.bot.send_message(uid, update.message.text)
            elif update.message.photo:
                await context.bot.send_photo(uid, update.message.photo[-1].file_id, caption=update.message.caption)
            elif update.message.video:
                await context.bot.send_video(uid, update.message.video.file_id, caption=update.message.caption)
            else:
                await context.bot.copy_message(uid, update.message.chat_id, update.message.message_id)
            success += 1
        except:
            fail += 1
        await asyncio.sleep(0.05)
    await update.message.reply_text(f"✅ Done. Sent: {success}, Failed: {fail}")
    context.user_data.pop("broadcast_mode")

# ==================== YOUR ORIGINAL HANDLERS (UNCHANGED) ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.first_name)
    await update.message.reply_text(
        "💖 PREMIUM EDITS BOT 💖\n\nSelect your content below 👇",
        reply_markup=reply_menu()
    )
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
            keyboard = []
            text = "❌ You have not joined:\n\n"
            for name, link in not_joined:
                text += f"{name}\n{link}\n\n"
                keyboard.append([InlineKeyboardButton(f"📢 JOIN {name}", url=link)])
            keyboard.append([InlineKeyboardButton("🔄 VERIFY AGAIN", callback_data="verify")])
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    add_user(user_id, update.effective_user.username, update.effective_user.first_name)

    # Admin panel button
    if text == "👑 ADMIN PANEL 👑":
        await admin_panel(update, context)
        return

    # ========== YOUR EXACT VIDEO LOGIC STARTS HERE ==========
    if text == "✅ VERIFY ACCESS":
        not_joined = await check_join(context.bot, user_id)
        if not not_joined:
            await update.message.reply_text("✅ Verification Successful\n\nEnjoy premium edits 💖")
        else:
            keyboard = []
            for name, link in not_joined:
                keyboard.append([InlineKeyboardButton(f"📢 JOIN {name}", url=link)])
            keyboard.append([InlineKeyboardButton("🔄 VERIFY AGAIN", callback_data="verify")])
            await update.message.reply_text(
                "⚠️ First join both channels to unlock bot buttons.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        return

    not_joined = await check_join(context.bot, user_id)
    if not_joined:
        keyboard = []
        for name, link in not_joined:
            keyboard.append([InlineKeyboardButton(f"📢 JOIN {name}", url=link)])
        keyboard.append([InlineKeyboardButton("🔄 VERIFY AGAIN", callback_data="verify")])
        await update.message.reply_text(
            "⚠️ First join both the channels to use the bot.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    button_map = {}
    for i in range(1, 32):
        button_map[f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖"] = f"class{i}"
    for i in range(32, 41):
        button_map[f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31}💝"] = f"class{i}"

    if text in button_map:
        key = button_map[text]
        try:
            sent_msg = await context.bot.copy_message(
                chat_id=update.message.chat_id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_id=VIDEOS[key],
                protect_content=True
            )
            # Auto-delete after 30 minutes
            asyncio.create_task(auto_delete_message(context, sent_msg.chat_id, sent_msg.message_id, 1800))
        except Exception as e:
            await update.message.reply_text(f"❌ ERROR:\n{e}")

# ==================== SET COMMANDS ====================
async def set_menu(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Restart the bot 💖"),
        BotCommand("admin", "Admin panel (code required)")
    ])

# ==================== MAIN ====================
def main():
    print("✅ BOT STARTED")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(buttons))          # your original verify callback
    app.add_handler(CallbackQueryHandler(admin_callback, pattern="^admin_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_code))
    app.add_handler(MessageHandler(filters.ALL, handle_broadcast))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_buttons))  # your video handler
    app.post_init = set_menu
    threading.Thread(target=run_web, daemon=True).start()
    app.run_polling()

if __name__ == "__main__":
    main()
