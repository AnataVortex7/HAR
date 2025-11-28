import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# -------------------------
#   SAFE HEARTBEAT
# -------------------------
async def heartbeat(app):
    while True:
        try:
            # silent ping to Telegram so the container stays "active"
            await app.bot.get_me()
        except Exception as e:
            # only notify owner on real errors
            try:
                if OWNER_ID:
                    await app.bot.send_message(chat_id=OWNER_ID, text=f"❌ Heartbeat Error: {e}")
            except Exception:
                # ignore notification errors
                pass
        await asyncio.sleep(4)   # every 4 seconds

# -------------------------
#   /start command
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = user.id
    name = user.first_name or user.username or "Unknown"

    await update.message.reply_text("Wait for CP Code...\nStay Connected ⭐")

    msg = f"🔔 New User Started Bot\n\n👤 Name: {name}\n🆔 User ID: {uid}"
    # send to owner (if set)
    if OWNER_ID:
        try:
            await context.bot.send_message(chat_id=OWNER_ID, text=msg)
        except Exception as e:
            print("Failed to send new-user message to owner:", e)

# -------------------------
#   MAIN BOT RUNNER
# -------------------------
async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set in environment variables")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Start silent heartbeat in background
    asyncio.create_task(heartbeat(app))

    print("Bot is running with safe heartbeat…")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
