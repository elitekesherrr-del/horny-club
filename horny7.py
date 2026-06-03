import os
import threading
import asyncio
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, BotCommand
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
)

# --- CONFIG ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_1 = "@K3NHA_EMPIRE"
CHANNEL_2 = "@K4NHA_EMPIRE"
CHANNEL_1_LINK = "https://t.me/K3NHA_EMPIRE"
CHANNEL_2_LINK = "https://t.me/K4NHA_EMPIRE"
STORAGE_CHANNEL_ID = -1003945923396
VIDEOS = {f"class{i}": i+1 for i in range(1, 41)}  # class1 → 2, class40 → 41

# Flask web server for keeping the bot alive
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "🍆💦 𝙃𝙊𝙍𝙉𝙔 𝘽𝙊𝙏 𝙄𝙎 𝘼𝙇𝙄𝙑𝙀 & 𝙎𝙊𝘼𝙆𝙄𝙉𝙂 💦🍆"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# --- Helper: check both channels ---
async def check_join(bot, user_id):
    """
    Returns a list of tuples (channel_name, channel_link) for channels the user has NOT joined.
    """
    not_joined = []
    # Channel 1
    try:
        m1 = await bot.get_chat_member(CHANNEL_1, user_id)
        if m1.status not in ["member", "administrator", "creator"]:
            not_joined.append(("🍆💦 𝐊𝟑𝐍𝐇𝐀 𝐄𝐌𝐏𝐈𝐑𝐄 🔥", CHANNEL_1_LINK))
    except:
        not_joined.append(("🍆💦 𝐊𝟑𝐍𝐇𝐀 𝐄𝐌𝐏𝐈𝐑𝐄 🔥", CHANNEL_1_LINK))
    # Channel 2
    try:
        m2 = await bot.get_chat_member(CHANNEL_2, user_id)
        if m2.status not in ["member", "administrator", "creator"]:
            not_joined.append(("💦🍑 𝐊𝟒𝐍𝐇𝐀 𝐄𝐌𝐏𝐈𝐑𝐄 🍆", CHANNEL_2_LINK))
    except:
        not_joined.append(("💦🍑 𝐊𝟒𝐍𝐇𝐀 𝐄𝐌𝐏𝐈𝐑𝐄 🍆", CHANNEL_2_LINK))
    return not_joined

# --- Horny button menu (ReplyKeyboardMarkup) ---
def horny_menu():
    keyboard = [["✅ 𝐕𝐄𝐑𝐈𝐅𝐘 𝐌𝐘 𝐇𝐎𝐑𝐍𝐘 𝐀𝐒𝐒"]]
    # First 31 buttons: Horny Edits 1 to 31
    for i in range(1, 32, 2):
        row = [f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖"]
        if i + 1 <= 31:
            row.append(f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i+1} 💖")
        keyboard.append(row)
    # Next 9 buttons: Baddie 1 to 9
    for i in range(32, 41, 2):
        row = [f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31} 💝"]
        if i + 1 <= 40:
            row.append(f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-30} 💝")
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# --- /start command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    not_joined = await check_join(context.bot, user.id)

    if not not_joined:
        # Already a good boy/girl – give the full horny menu
        await update.message.reply_text(
            f"💦🍆 **𝗢𝗵 𝗯𝗮𝗯𝘆 {user.first_name}**, 𝘆𝗼𝘂'𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗼𝗻𝗲 𝗼𝗳 𝘂𝘀! 😈💋\n"
            f"𝗡𝗼𝘄 𝘁𝗼𝘂𝗰𝗵 𝘆𝗼𝘂𝗿𝘀𝗲𝗹𝗳 𝘁𝗼 𝘁𝗵𝗲𝘀𝗲 𝗽𝗿𝗲𝗺𝗶𝘂𝗺 𝗲𝗱𝗶𝘁𝘀... 💦🍑\n"
            f"𝗝𝘂𝘀𝘁 𝘁𝗮𝗽 𝗮𝗻𝘆 𝗯𝘂𝘁𝘁𝗼𝗻 𝗯𝗲𝗹𝗼𝘄 𝗮𝗻𝗱 𝗲𝗻𝗷𝗼𝘆 𝘁𝗵𝗲 𝘀𝗵𝗼𝘄! 🔥🥵",
            reply_markup=horny_menu()
        )
    else:
        # Not fully joined – ask to join with naughty convincing
        msg = (
            f"🥵💦 𝗛𝗲𝘆 {user.first_name}, 𝘆𝗼𝘂 𝘄𝗮𝗻𝗻𝗮 𝘀𝗲𝗲 𝘀𝗼𝗺𝗲 *𝗛𝗢𝗧 & 𝗦𝗣𝗜𝗖𝗬* 𝗲𝗱𝗶𝘁𝘀, 𝗱𝗼𝗻'𝘁 𝘆𝗼𝘂? 🍆🔥\n\n"
            f"𝗕𝘂𝘁 𝗳𝗶𝗿𝘀𝘁… 𝘆𝗼𝘂 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗷𝗼𝗶𝗻 𝗺𝘆 *𝘀𝗲𝗰𝗿𝗲𝘁 𝗽𝗹𝗲𝗮𝘀𝘂𝗿𝗲 𝗰𝗵𝗮𝗺𝗯𝗲𝗿𝘀*:\n"
            f"➡️ {CHANNEL_1}\n"
            f"➡️ {CHANNEL_2}\n\n"
            f"👉 *𝗝𝗼𝗶𝗻 𝗯𝗼𝘁𝗵* 𝗮𝗻𝗱 𝘁𝗵𝗲𝗻 𝗵𝗶𝘁 𝗩𝗘𝗥𝗜𝗙𝗬. 𝗢𝗻𝗹𝘆 𝘁𝗵𝗲 𝗵𝗼𝗿𝗻𝗶𝗲𝘀𝘁 𝘀𝗼𝘂𝗹𝘀 𝗴𝗲𝘁 𝗮𝗰𝗰𝗲𝘀𝘀! 💦😈"
        )
        keyboard = []
        for name, link in not_joined:
            keyboard.append([InlineKeyboardButton(f"📢 𝗝𝗢𝗜𝗡 {name} (𝗰𝘂𝗺 𝗶𝗻𝘀𝗶𝗱𝗲)", url=link)])
        keyboard.append([InlineKeyboardButton("✅ 𝗩𝗘𝗥𝗜𝗙𝗬 𝗠𝗬 𝗛𝗢𝗥𝗡𝗬 𝗔𝗦𝗦", callback_data="verify")])
        await update.message.reply_text(
            msg,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# --- Verify callback ---
async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    not_joined = await check_join(context.bot, user.id)

    if not not_joined:
        # Verification success – give access
        await query.message.edit_text(
            f"✅ *𝗩𝗘𝗥𝗜𝗙𝗜𝗘𝗗!* 𝗚𝗼𝗼𝗱 𝗹𝗶𝘁𝘁𝗹𝗲 𝘀𝗹𝘂𝘁 😈💦\n"
            f"𝗡𝗼𝘄 {user.first_name}, 𝗵𝗲𝗿𝗲'𝘀 𝘆𝗼𝘂𝗿 𝘄𝗲𝘁 𝗱𝗿𝗲𝗮𝗺 𝗺𝗲𝗻𝘂... 💋🍆\n"
            f"𝗧𝗮𝗽 𝗮𝗻𝘆 𝗯𝘂𝘁𝘁𝗼𝗻 𝗮𝗻𝗱 𝗜'𝗹𝗹 𝘀𝗹𝗶𝗱𝗲 𝗶𝗻𝘁𝗼 𝘆𝗼𝘂𝗿 𝗗𝗠𝘀 𝘄𝗶𝘁𝗵 𝘁𝗵𝗲 𝗳𝗶𝗹𝘁𝗵𝗶𝗲𝘀𝘁 𝗲𝗱𝗶𝘁𝘀! 🔥🥵",
            parse_mode="Markdown"
        )
        await query.message.reply_text(
            "👇 *𝗖𝗵𝗼𝗼𝘀𝗲 𝘆𝗼𝘂𝗿 𝗽𝗼𝗶𝘀𝗼𝗻:* 👇\n🍑💦🍆🥵",
            parse_mode="Markdown",
            reply_markup=horny_menu()
        )
    else:
        # Still missing some channels
        msg = (
            f"❌ *{user.first_name}*, 𝘆𝗼𝘂 𝗱𝗶𝗱𝗻'𝘁 𝗷𝗼𝗶𝗻 𝗮𝗹𝗹 𝗺𝘆 𝗻𝗮𝘂𝗴𝗵𝘁𝘆 𝗰𝗵𝗮𝗻𝗻𝗲𝗹𝘀 𝘆𝗲𝘁.\n"
            f"𝗜 𝗰𝗮𝗻'𝘁 𝘀𝗽𝗿𝗲𝗮𝗱 𝗺𝘆 𝗹𝗲𝗴𝘀 𝗳𝗼𝗿 𝘆𝗼𝘂 𝗶𝗳 𝘆𝗼𝘂'𝗿𝗲 𝗻𝗼𝘁 𝗮 𝗺𝗲𝗺𝗯𝗲𝗿... 😩💦\n\n"
            f"👉 𝗝𝗼𝗶𝗻 𝘁𝗵𝗲 𝗺𝗶𝘀𝘀𝗶𝗻𝗴 𝗼𝗻𝗲𝘀 𝗯𝗲𝗹𝗼𝘄 𝗮𝗻𝗱 𝗩𝗘𝗥𝗜𝗙𝗬 𝗮𝗴𝗮𝗶𝗻, 𝗯𝗮𝗯𝘆. 🍆🔥"
        )
        keyboard = []
        for name, link in not_joined:
            keyboard.append([InlineKeyboardButton(f"📢 𝗝𝗢𝗜𝗡 {name} (𝗜'𝗺 𝘄𝗲𝘁 𝗮𝗹𝗿𝗲𝗮𝗱𝘆)", url=link)])
        keyboard.append([InlineKeyboardButton("🔄 𝗩𝗘𝗥𝗜𝗙𝗬 𝗔𝗚𝗔𝗜𝗡 (𝗽𝗹𝘀 𝗰𝘂𝗺 𝗶𝗻𝘀𝗶𝗱𝗲)", callback_data="verify")])
        await query.message.edit_text(
            msg,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# --- Handle the horny button presses ---
async def text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    not_joined = await check_join(context.bot, user.id)

    # If any channel is missing, deny access with a juicy warning
    if not_joined:
        msg = (
            f"😭💦 𝗢𝗵 𝗻𝗼 {user.first_name}, 𝘆𝗼𝘂 𝗹𝗲𝗳𝘁 𝗺𝘆 𝘀𝘄𝗲𝗲𝘁 𝗰𝘂𝗻𝘁… 𝗜 𝗺𝗲𝗮𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹!\n"
            f"𝗜 𝗰𝗮𝗻'𝘁 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂 𝘁𝗵𝗲 𝗵𝗼𝘁 𝘀𝘁𝘂𝗳𝗳 𝘂𝗻𝗹𝗲𝘀𝘀 𝘆𝗼𝘂'𝗿𝗲 *𝘀𝘁𝗶𝗹𝗹* 𝗶𝗻𝘀𝗶𝗱𝗲 𝗺𝗲.\n\n"
            f"👉 𝗥𝗲-𝗷𝗼𝗶𝗻 𝘁𝗵𝗲 𝗺𝗶𝘀𝘀𝗶𝗻𝗴 𝗰𝗵𝗮𝗻𝗻𝗲𝗹(𝘀) 𝗮𝗻𝗱 𝗵𝗶𝘁 𝗩𝗘𝗥𝗜𝗙𝗬 𝗮𝗴𝗮𝗶𝗻, 𝗱𝗮𝗱𝗱𝘆/𝗺𝗼𝗺𝗺𝘆! 🍆💦"
        )
        keyboard = []
        for name, link in not_joined:
            keyboard.append([InlineKeyboardButton(f"📢 𝗝𝗢𝗜𝗡 {name} (𝗜'𝗺 𝗯𝗲𝗴𝗴𝗶𝗻𝗴 💦)", url=link)])
        keyboard.append([InlineKeyboardButton("✅ 𝗩𝗘𝗥𝗜𝗙𝗬 𝗠𝗬 𝗥𝗘𝗧𝗨𝗥𝗡", callback_data="verify")])
        await update.message.reply_text(
            msg,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Map button texts to internal class keys
    button_map = {f"💝 𝙃𝙊𝙍𝙉𝙔 𝙀𝘿𝙄𝙏𝙎 {i} 💖": f"class{i}" for i in range(1, 32)}
    button_map.update({f"💘 𝘽𝘼𝘿𝘿𝙄𝙀 {i-31} 💝": f"class{i}" for i in range(32, 41)})

    if text in button_map:
        class_key = button_map[text]
        video_msg_id = VIDEOS[class_key]
        try:
            await context.bot.copy_message(
                chat_id=update.message.chat_id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_id=video_msg_id,
                protect_content=True
            )
            # Spicy follow-up
            await update.message.reply_text(
                f"💦🍑 *𝗘𝗻𝗷𝗼𝘆 𝘁𝗵𝗲 𝘃𝗶𝗲𝘄, 𝗻𝗮𝘂𝗴𝗵𝘁𝘆 {user.first_name}...* 💦🍆\n"
                f"𝗗𝗼𝗻'𝘁 𝗳𝗼𝗿𝗴𝗲𝘁 𝘁𝗼 𝗰𝗼𝗺𝗲 𝗯𝗮𝗰𝗸 𝗳𝗼𝗿 𝗺𝗼𝗿𝗲! 😘🔥",
                parse_mode="Markdown"
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ 𝗢𝗼𝗽𝘀, 𝘁𝗵𝗲 𝘃𝗶𝗱𝗲𝗼 𝗶𝘀 𝘀𝗵𝘆 𝗿𝗶𝗴𝗵𝘁 𝗻𝗼𝘄. 𝗧𝗲𝗹𝗹 𝗺𝘆 𝗼𝘄𝗻𝗲𝗿 𝘁𝗼 𝗰𝗵𝗲𝗰𝗸 𝘀𝘁𝗼𝗿𝗮𝗴𝗲 𝗰𝗵𝗮𝗻𝗻𝗲𝗹!\n𝗘𝗿𝗿𝗼𝗿: {e}"
            )
    else:
        # If user types something else, tease them
        await update.message.reply_text(
            f"😈💦 {user.first_name}, 𝗱𝗼𝗻'𝘁 𝘁𝘆𝗽𝗲 𝗻𝗼𝗻𝘀𝗲𝗻𝘀𝗲… 𝗷𝘂𝘀𝘁 *𝘁𝗮𝗽 𝘁𝗵𝗲 𝗵𝗼𝗿𝗻𝘆 𝗯𝘂𝘁𝘁𝗼𝗻𝘀* 𝗯𝗲𝗹𝗼𝘄! 💋🍆",
            parse_mode="Markdown"
        )

# --- Bot runner ---
async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_buttons))

    # Set bot commands for nice UI
    await app.bot.set_my_commands([
        BotCommand("start", "🍆💦 Get access to horny premium edits 🔥🥵")
    ])

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

# --- Main: run Flask web server in background + bot ---
def main():
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()
