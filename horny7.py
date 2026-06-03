import os
import asyncio
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

# ==========================================
# CONFIG
# ==========================================

BOT_TOKEN = os.environ.get("BOT_TOKEN")

CHANNEL_1 = "@K3NHA_EMPIRE"
CHANNEL_2 = "@K4NHA_EMPIRE"

CHANNEL_1_LINK = "https://t.me/K3NHA_EMPIRE"
CHANNEL_2_LINK = "https://t.me/K4NHA_EMPIRE"

STORAGE_CHANNEL_ID = -1003945923396


# ==========================================
# VIDEOS
# ==========================================

VIDEOS = {
    "class1": 2, "class2": 3, "class3": 4, "class4": 5, "class5": 6,
    "class6": 7, "class7": 8, "class8": 9, "class9": 10, "class10": 11,
    "class11": 12, "class12": 13, "class13": 14,

    "class14": 33, "class15": 34, "class16": 35, "class17": 36,
    "class18": 37, "class19": 38, "class20": 39, "class21": 40,
    "class22": 41, "class23": 42, "class24": 43, "class25": 44,
    "class26": 45, "class27": 46, "class28": 47, "class29": 48,
    "class30": 49, "class31": 50,

    "class32": 51, "class33": 52, "class34": 53, "class35": 54,
    "class36": 55, "class37": 56, "class38": 57, "class39": 58,
    "class40": 59
}


# ==========================================
# CHANNEL CHECK
# ==========================================

async def check_join(bot, user_id):
    not_joined = []

    for name, link in [
        ("CHANNEL 1", CHANNEL_1),
        ("CHANNEL 2", CHANNEL_2)
    ]:
        try:
            member = await bot.get_chat_member(link, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append((name, link))
        except:
            not_joined.append((name, link))

    return not_joined


def is_verified(not_joined):
    return len(not_joined) == 0


# ==========================================
# KEYBOARDS
# ==========================================

def join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 JOIN CHANNEL 1", url=CHANNEL_1_LINK)],
        [InlineKeyboardButton("📢 JOIN CHANNEL 2", url=CHANNEL_2_LINK)],
        [InlineKeyboardButton("🔄 VERIFY", callback_data="verify")]
    ])


def reply_menu():
    keyboard = [["🔄 VERIFY ACCESS"]]

    for i in range(1, 32, 2):
        row = [f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖"]
        if i + 1 <= 31:
            row.append(f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i+1} 💖")
        keyboard.append(row)

    for i in range(32, 41, 2):
        row = [f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31} 💝"]
        if i + 1 <= 40:
            row.append(f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-30} 💝")
        keyboard.append(row)

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ==========================================
# START
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    not_joined = await check_join(context.bot, update.effective_user.id)

    if not is_verified(not_joined):
        await update.message.reply_text(
            "⚠️ First join both channels to unlock bot 👇",
            reply_markup=join_keyboard()
        )
        return

    await update.message.reply_text(
        "💖 PREMIUM EDITS BOT 💖\nAccess Granted ✅",
        reply_markup=reply_menu()
    )


# ==========================================
# VERIFY CALLBACK
# ==========================================

async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    not_joined = await check_join(context.bot, user_id)

    if is_verified(not_joined):

        await query.message.edit_text(
            "✅ Verified Successfully!\nNow you can use bot 💖"
        )

        await query.message.reply_text(
            "👇 Main Menu Unlocked",
            reply_markup=reply_menu()
        )

    else:

        text = "❌ Not joined channels:\n\n"
        buttons = []

        for name, link in not_joined:
            text += f"{name}\n"
            buttons.append([InlineKeyboardButton(f"📢 JOIN {name}", url=link)])

        buttons.append([InlineKeyboardButton("🔄 VERIFY AGAIN", callback_data="verify")])

        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )


# ==========================================
# TEXT HANDLER (MAIN SECURITY LOGIC)
# ==========================================

async def text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text

    # 🔥 ALWAYS CHECK LIVE STATUS (LEAVE DETECTION FIX)
    not_joined = await check_join(context.bot, user_id)

    if not is_verified(not_joined):
        await update.message.reply_text(
            "⚠️ You left the channel!\nJoin again to continue 👇",
            reply_markup=join_keyboard()
        )
        return

    # ======================================
    # VERIFY BUTTON
    # ======================================

    if text == "🔄 VERIFY ACCESS":

        if is_verified(not_joined):
            await update.message.reply_text("✅ Already Verified 💖")
        else:
            await update.message.reply_text(
                "⚠️ Not verified yet!",
                reply_markup=join_keyboard()
            )
        return

    # ======================================
    # BUTTON MAP
    # ======================================

    button_map = {}

    for i in range(1, 32):
        button_map[f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖"] = f"class{i}"

    for i in range(32, 41):
        button_map[f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31} 💝"] = f"class{i}"

    # ======================================
    # SEND VIDEO
    # ======================================

    if text in button_map:

        key = button_map[text]

        try:
            await context.bot.copy_message(
                chat_id=update.message.chat_id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_id=VIDEOS[key],
                protect_content=True
            )

        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")


# ==========================================
# MENU SETUP
# ==========================================

async def set_menu(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start Bot 💖")
    ])


# ==========================================
# MAIN
# ==========================================

def main():

    print("🚀 BOT RUNNING ON RENDER")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_buttons))

    app.post_init = set_menu

    app.run_polling()


if __name__ == "__main__":
    main()
