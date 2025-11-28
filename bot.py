import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from aiohttp import web

# -------------------------
# Environment variables
# -------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))  # replace with your Telegram ID or use env

# -------------------------
# /start command
# -------------------------
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

# -------------------------
# Minimal HTTP server for health check
# -------------------------
async def handle(request):
    return web.Response(text="OK")

async def run_web():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("Web server running on port 8080")

# -------------------------
# Main bot function
# -------------------------
async def main():
    # Start Telegram bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Start minimal web server for health check
    asyncio.create_task(run_web())

    print("Bot and web server starting…")
    await app.run_polling()

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    asyncio.run(main())
