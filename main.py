import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client("drm_har_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def capture_har(url: str, file_name: str = "output.har"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(record_har_path=file_name)
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")
        await asyncio.sleep(10)
        await context.close()
        await browser.close()
    return file_name

@bot.on_message(filters.command("check") & filters.private)
async def check_video(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ कृपया एक वीडियो लिंक दें: `/check <url>`", quote=True)
    
    url = message.command[1]
    await message.reply("🔄 Processing... Please wait", quote=True)

    try:
        file = await capture_har(url)
        await message.reply_document(document=file, caption="✅ HAR file extracted.")
        os.remove(file)
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

bot.run()
