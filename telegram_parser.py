import os
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.types import Channel, ChannelForbidden

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
session_name = os.getenv("TG_SESSION_NAME", "lilbet")
keywords = os.getenv("TG_KEYWORDS", "вакансия,ищем,трафик,гемблинг,cpa,арбитраж,менеджер").lower().split(",")
min_subscribers = int(os.getenv("TG_MIN_SUBSCRIBERS", 1000))
max_subscribers = int(os.getenv("TG_MAX_SUBSCRIBERS", 5000))

def search_telegram_channels():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_channels())

async def fetch_channels():
    print("🔐 Авторизация в Telegram...")
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()
    print("✅ Успешно авторизовались.")

    channels_with_keywords_in_name = []
    channels_with_keywords_in_description = []

    try:
        for keyword in keywords:
            print(f"🔎 Ищем каналы по ключевому слову: {keyword}")
            results = await client(SearchRequest(
                q=keyword,
                limit=50  # Максимальное количество результатов за один запрос
            ))

            for result in results.chats:
                if isinstance(result, Channel):
                    try:
                        if result.participants_count and min_subscribers <= result.participants_count <= max_subscribers:
                            # Проверка ключевых слов в названии
                            if keyword in (result.title or "").lower():
                                channels_with_keywords_in_name.append({
                                    "channel": result.username or "N/A",
                                    "title": result.title,
                                    "description": result.about or "",
                                    "subscribers": result.participants_count
                                })
                            # Проверка ключевых слов в описании
                            elif keyword in (result.about or "").lower():
                                channels_with_keywords_in_description.append({
                                    "channel": result.username or "N/A",
                                    "title": result.title,
                                    "description": result.about or "",
                                    "subscribers": result.participants_count
                                })
                    except ChannelForbidden:
                        print(f"⚠️ Доступ к каналу {result.title} запрещен.")
                    except Exception as e:
                        print(f"⚠️ Ошибка при обработке канала {result.title}: {e}")

    finally:
        await client.disconnect()

    return channels_with_keywords_in_name, channels_with_keywords_in_description
