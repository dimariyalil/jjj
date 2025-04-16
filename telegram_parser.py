import os
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors import FloodWaitError

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
session_name = os.getenv("TG_SESSION_NAME", "lilbet")
target_channels = os.getenv("TG_TARGETS", "").split(",")
keywords = os.getenv("TG_KEYWORDS", "вакансия,ищем,трафик,гемблинг,cpa,арбитраж,менеджер").lower().split(",")

def parse_telegram_channels():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_posts())

async def fetch_posts():
    posts = []

    print("🔐 Авторизация в Telegram...")
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()
    print("✅ Успешно авторизовались.")

    try:
        for username in target_channels:
            username = username.strip()
            if not username:
                continue
            print(f"📡 Парсим: {username}")
            try:
                entity = await client.get_entity(username)
                history = await client(GetHistoryRequest(
                    peer=entity,
                    limit=30,
                    offset_date=None,
                    offset_id=0,
                    max_id=0,
                    min_id=0,
                    add_offset=0,
                    hash=0
                ))

                filtered_messages = []
                for msg in history.messages:
                    if msg.message and any(kw in msg.message.lower() for kw in keywords):
                        filtered_messages.append({
                            "channel": username,
                            "text": msg.message,
                            "url": f"https://t.me/{username}/{msg.id}",
                            "date": msg.date.strftime("%Y-%m-%d %H:%M"),
                            "source": "telegram",
                            "positive": ""
                        })

                print(f"✅ Найдено релевантных постов: {len(filtered_messages)}")
                posts.extend(sorted(filtered_messages, key=lambda x: x['date'], reverse=True))

            except FloodWaitError as e:
                print(f"⏳ FloodWait: ждём {e.seconds} сек.")
                await asyncio.sleep(e.seconds + 1)
            except Exception as e:
                print(f"⚠️ Ошибка канала {username}: {e}")

            await asyncio.sleep(1)

    finally:
        await client.disconnect()

    return posts
