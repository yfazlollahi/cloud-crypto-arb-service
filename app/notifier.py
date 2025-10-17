import os
import httpx
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

async def send_telegram_message(text: str):
    """
    Send a text message to the Telegram chat.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[ERROR] Telegram bot token or chat ID is not set.")
        return

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown"
            }
            r = await client.post(TELEGRAM_URL, data=payload)
            r.raise_for_status()
        except Exception as e:
            print(f"[ERROR] Failed to send Telegram message: {e}")
