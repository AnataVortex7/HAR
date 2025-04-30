import os
import asyncio
import subprocess
import traceback
from pyrogram import Client, filters
from pyrogram.types import Message
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client("classplus_drm_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def capture_har(url: str, file_name: str = "output.har"):
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
            )
        except Exception as e:
            print("❌ Chromium launch failed:", e)
            raise

        context = await browser.new_context(record_har_path=file_name)
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")
        await asyncio.sleep(10)
        await context.close()
        await browser.close()
    return file_name

def parse_har_and_extract_key(har_path: str):
    return {
        "pssh": "dummy_pssh",
        "license_url": "https://example.com/license",
        "headers": {"authorization": "Bearer dummy"},
        "key": "0123456789abcdef0123456789abcdef"
    }

def download_video(m3u8_url: str, key: str, output_file="video.mp4"):
    cmd = [
        "N_m3u8DL-RE", m3u8_url,
        "--key", key,
        "--workDir", "./downloads",
        "--saveName", output_file.replace(".mp4", ""),
        "--no-log"
    ]
    subprocess.run(cmd, check=True)

@bot.on_message(filters.command("check") & filters.private)
async def process_video(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Use: /check <m3u8-url>")

    url = message.command[1]
    await message.reply("🔄 Processing... Please wait")

    try:
        har_file = await capture_har(url)
        drm_info = parse_har_and_extract_key(har_file)
        await message.reply(f"🧩 DRM Info:\npssh: {drm_info['pssh']}\nlicense: {drm_info['license_url']}\nkey: {drm_info['key']}")

        download_video(url, drm_info['key'])
        video_path = os.path.join("downloads", "video.mp4")
        if os.path.exists(video_path):
            await message.reply_video(video=video_path, caption="✅ Video downloaded.")
            os.remove(video_path)
        else:
            await message.reply("❌ Video download failed.")
    except Exception as e:
        await message.reply(f"❌ Error:\n{str(e)}\n{traceback.format_exc()[-200:]}")

bot.run()
