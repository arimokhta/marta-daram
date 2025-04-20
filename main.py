import asyncio
import logging
import os
from telethon import TelegramClient, events
from telethon.errors import RPCError
import nest_asyncio

# ✅ دریافت تنظیمات از محیط
API_ID = int(os.getenv(""))
API_HASH = os.getenv("")
PHONE = os.getenv("")
SESSION_NAME = os.getenv("SESSION_NAME", "userbot_session")

# لاگ‌گذاری
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# تریگرها و پاسخ‌ها
TRIGGERS = {
    'marta': ["مارتا دارم", "سلام مارتا دارم"],
    'france': ["سلام فرانسویا دارم", "فرانسویا دارم", "فرانسوی ها دارم"],
}
RESPONSES = {
    'marta': 'سلام مارتا میخام',
    'france': 'سلام فرانسویا میخام',
}

# اجرای ربات
async def start_userbot():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    @client.on(events.NewMessage)
    async def handler(event):
        if not event.is_group:
            return

        text = (event.message.message or '').strip().lower()
        sender_id = event.message.sender_id

        for key, trigger_list in TRIGGERS.items():
            if any(trigger.lower() in text for trigger in trigger_list):
                resp = RESPONSES.get(key)
                try:
                    await client.send_message(sender_id, resp)
                    logger.info(f"✅ پیام ارسال شد به {sender_id}: {resp}")
                except RPCError as e:
                    logger.error(f"⚠️ خطا در ارسال پیام به {sender_id}: {e}")
                break

    logger.info("🤖 ربات تلگرام راه‌اندازی شد...")
    await client.start(phone=PHONE)
    await client.run_until_disconnected()

# اجرای اصلی
nest_asyncio.apply()
asyncio.run(start_userbot())
