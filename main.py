import os
import random
from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# Token Railway environment variable se aayega
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Error: BOT_TOKEN environment variable nahi mila! Kripya Railway me add karein.")

MOTIVATIONAL_QUOTES = [
    "✨ *\"Success doesn't come to you, you go to it!\"*",
    "💡 *\"Roz thoda thoda padho, NEET/Boards me top karo!\"*",
    "🎯 *\"Consistency is the key to cracking any exam!\"*",
    "🔥 *\"Padhai aisi karo ki sapne sach ho jayein!\"*",
    "🌱 *\"Hard work beats talent when talent doesn't work hard.\"*",
]

FILE_IDS = {
    # --- Class 11 ---
    "11_intro": "BQACAgUAAxkBAAMDasJewxdD2ZHf6OHC6gfFiaYCb0IAAzMAArw6EVaA5XbNM_XI-j0E",
    "11_1": "BQACAgUAAxkBAAMEasJew_6Lvj1D0AEKjNOkFSl1QLYAAgEzAAK8OhFWme9F75l4vwM9BA",
    "11_2": "BQACAgUAAxkBAAMFasJew-FeQd6WxUYaMkSmB06s7V0AAgIzAAK8OhFWN46Bc0F-e749BA",
    "11_3": "BQACAgUAAxkBAAMGasJewwvvMOA6NjSGAAH_ZCGI27YjAAIDMwACvDoRVgiVKGziv89APQQ",
    "11_4": "BQACAgUAAxkBAAMHasJew9u17wNYFEnrBgWn7Gt1WtIAAgQzAAK8OhFW7py1fyYx2Uo9BA",
    "11_5": "BQACAgUAAxkBAAMIasJewz5jsGlKQw-xGsGtWmKdZCMAAgUzAAK8OhFWnbU7ub7n0pc9BA",
    "11_6": "BQACAgUAAxkBAAMJasJew1ytFQM2Qjkbow2YRnp8hUEAAgYzAAK8OhFW2C0L5cy9Nog9BA",
    "11_7": "BQACAgUAAxkBAAMKasJew-SSwan5ATRf3QXNZyabgFkAAgczAAK8OhFWh61FMEO7nXk9BA",
    "11_8": "BQACAgUAAxkBAAMLasJewwKbk_2Oo_h07OeiPVUJ2mkAAggzAAK8OhFWUoXDudfHOTU9BA",
    "11_9": "BQACAgUAAxkBAAMMasJew1NubDVX5kkEkKKIETV0LAUAAgkzAAK8OhFWMFi7qegG8fA9BA",
    "11_10": "BQACAgUAAxkBAAMNasJew_tTlNyOq0RHNtxypC9_LeAAAgozAAK8OhFWtqdR69sq2FY9BA",
    "11_11": "BQACAgUAAxkBAAMOasJewwdqFoG_uOR4QxYjJsMMz2EAAgszAAK8OhFWBB43kTZSp209BA",
    "11_12": "BQACAgUAAxkBAAMPasJew2Ty37vCmA09hV-3NCf3pIkAAgwzAAK8OhFWxPTn8EtP_3Y9BA",
    "11_13": "BQACAgUAAxkBAAMQasJewwgG_p700tHbUhldGfmjK98AAg0zAAK8OhFWfxJPwDm60089BA",
    "11_14": "BQACAgUAAxkBAAMRasJewyljuuTPECRv3cFhvvFp1UIAAg4zAAK8OhFW5DZjlyQnFxc9BA",
    "11_15": "BQACAgUAAxkBAAMSasJewzqFl9AMyaFuXDaQb_5q8-EAAg8zAAK8OhFWZAABAYRSB-rvPQQ",
    "11_16": "BQACAgUAAxkBAAMTasJew4564OGjP3lb8-_VA_dkwH8AAhAzAAK8OhFWzKMIEfbvz709BA",
    "11_17": "BQACAgUAAxkBAAMUasJew7HTMWFUVv6ta1M8OeIiVoEAAhEzAAK8OhFWWMHM5XhQGG89BA",
    "11_18": "BQACAgUAAxkBAAMVasJew7iLSpHQ3d5wWPFfl9obXnkAAhIzAAK8OhFWCh4ZnPaLmVA9BA",
    "11_19": "BQACAgUAAxkBAAMWasJew9jY1WqL-sKLrf0E8n53yAADEzMAArw6EVZjK-PR5RLU2j0E",

    # --- Class 12 ---
    "12_intro": "BQACAgUAAxkBAAMXasJew0Nkg7_3XQv2WASIYoxueTIAAhQzAAK8OhFWaoKNYSMQaT09BA",
    "12_1": "BQACAgUAAxkBAAMYasJew_sdoKEZbsI6Wgiuzp_2W9kAAhUzAAK8OhFW7bFXSaG8GCs9BA",
    "12_2": "BQACAgUAAxkBAAMZasJew3fgtavUq1SzD_29vDvKsNMAAhczAAK8OhFWgLO9YNUJ8oI9BA",
    "12_3": "BQACAgUAAxkBAAMaasJew216E5Y0bYAI7FzD58HTXdcAAhgzAAK8OhFWAT3E4564Ggo9BA",
    "12_4": "BQACAgUAAxkBAAMbasJew8pFlz1MOach1wABWAfI2qKPAAIZMwACvDoRVnYuMhPDMKMdPQQ",
    "12_5": "BQACAgUAAxkBAAMcasJew4WbFoCgKlMhH3uyE1Xao1cAAhozAAK8OhFWuEN1CLt5HRc9BA",
    "12_6": "BQACAgUAAxkBAAMdasJew25oCqGmT29ESxJOGkkJHdoAAhszAAK8OhFW3YcYRaaLQr89BA",
    "12_7": "BQACAgUAAxkBAAMeasJew9RCUTizFfQfCSgwd-w8IdIAAhwzAAK8OhFWNY5xnRGcNjY9BA",
    "12_8": "BQACAgUAAxkBAAMfasJew0HeZ5tmQWcXsTaI44pdeMsAAh0zAAK8OhFWlXAAAQN_MQVePQQ",
    "12_9": "BQACAgUAAxkBAAMgasJew3NjFzg_SrE0VcgwO-ijwtEAAh4zAAK8OhFWxkzANTd82fo9BA",
    "12_10": "BQACAgUAAxkBAAMhasJew4mVgHMqZjIHqUPoxEd7IVAAAh8zAAK8OhFWTuZQznQY49U9BA",
    "12_11": "BQACAgUAAxkBAAMiasJew4mL7m42D67A7E24OBI7wa4AAiAzAAK8OhFWtTDpru7kca09BA",
    "12_12": "BQACAgUAAxkBAAMjasJew274shkKLe8cCS2VRG2s1zIAAiEzAAK8OhFWD-E-KWRu6aA9BA",
    "12_13": "BQACAgUAAxkBAAMkasJewyREhPra007yUeAn6RCl9HwAAiIzAAK8OhFWL8MUo_v75Fs9BA",
}

# Sirf Class 11 aur Class 12 ka Clean Keyboard
def get_main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📗 Class 11th Biology", callback_data="menu_11"),
            InlineKeyboardButton("📘 Class 12th Biology", callback_data="menu_12"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_chapters_keyboard(class_num: int, total_chapters: int):
    keyboard = [
        [InlineKeyboardButton("📑 00. Introduction Notes", callback_data=f"send_{class_num}_intro")]
    ]
    row = []
    for ch in range(1, total_chapters + 1):
        row.append(
            InlineKeyboardButton(f"📁 Ch {ch:02d}", callback_data=f"send_{class_num}_{ch}")
        )
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_main")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "Student"
    welcome_text = (
        f"👋 *Hello {user_name}!*\n\n"
        f"🔬 *Welcome to Biology Study Portal* 🧬\n"
        f"Yahan aapko Class 11th aur 12th ke saare NCERT chapters ki complete notes aur PDFs milengi bilkul free.\n\n"
        f"👇 *Neeche se apni class select karein:*"
    )
    await update.message.reply_text(
        welcome_text, 
        reply_markup=get_main_menu_keyboard(), 
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "back_main":
        await query.answer()
        user_name = update.effective_user.first_name or "Student"
        await query.edit_message_text(
            f"👋 *Hello {user_name}!*\n\n"
            f"🔬 *Welcome to Biology Study Portal* 🧬\n\n"
            f"👇 *Neeche se apni class select karein:*",
            reply_markup=get_main_menu_keyboard(),
            parse_mode="Markdown"
        )

    elif data == "menu_11":
        await query.answer()
        await query.edit_message_text(
            "📗 *Class 11th Biology - All Chapters*\n\n"
            "📌 *Select the chapter you want to download:*",
            parse_mode="Markdown",
            reply_markup=get_chapters_keyboard(class_num=11, total_chapters=19),
        )

    elif data == "menu_12":
        await query.answer()
        await query.edit_message_text(
            "📘 *Class 12th Biology - All Chapters*\n\n"
            "📌 *Select the chapter you want to download:*",
            parse_mode="Markdown",
            reply_markup=get_chapters_keyboard(class_num=12, total_chapters=13),
        )

    elif data.startswith("send_"):
        key = data.replace("send_", "")
        file_id = FILE_IDS.get(key)

        parts = key.split("_")
        cls_num = parts[0]
        ch_name = "Introduction" if parts[1] == "intro" else f"Chapter {parts[1]}"
        
        await query.answer(text=f"🚀 Sending Class {cls_num} - {ch_name}...", show_alert=False)

        if file_id:
            quote = random.choice(MOTIVATIONAL_QUOTES)
            caption_text = (
                f"📚 *Class {cls_num} Biology*\n"
                f"📑 *Topic:* {ch_name}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"{quote}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"✅ *Downloaded via Biology Portal Bot*"
            )
            await query.message.reply_document(
                document=file_id,
                caption=caption_text,
                parse_mode="Markdown"
            )
        else:
            await query.message.reply_text("⚠️ File not found.")

async def post_init(application):
    commands = [
        BotCommand("start", "🏠 Main Menu / Open Classes")
    ]
    await application.bot.set_my_commands(commands)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot ready hai...")
    app.run_polling()

if __name__ == "__main__":
    main()
