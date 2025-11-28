import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))


# /start → user ID मिळतो
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n"
        f"Your Telegram ID: `{user.id}`\n\n"
        f"Stay connected!"
    )


# /id command → कोणत्याही user ची ID पाहायला
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Your ID: `{user.id}`")


# Bot मध्ये err आला तर फक्त owner ला DM
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    error_text = f"⚠ ERROR:\n{context.error}"

    try:
        await context.bot.send_message(chat_id=OWNER_ID, text=error_text)
    except:
        pass

    logger.error("Exception while handling:", exc_info=context.error)


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", myid))

    # Error handler
    app.add_error_handler(error_handler)

    # Start bot
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
