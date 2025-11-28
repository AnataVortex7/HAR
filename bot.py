import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))  # Owner Telegram ID

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    first_name = user.first_name or user.username or "Unknown"

    # 1️⃣ Send user ID to owner
    if OWNER_ID:
        try:
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=f"🔔 New User Started Bot\n\n👤 Name: {first_name}\n🆔 User ID: {user_id}"
            )
        except Exception as e:
            print("Failed to notify owner:", e)

    # 2️⃣ Send message to user
    await update.message.reply_text(
        f"Hello {first_name}! 👋\nStay connected ⭐"
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is starting…")
    app.run_polling()


if __name__ == "__main__":
    main()
