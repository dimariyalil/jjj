
from telegram_parser import parse_telegram_channels
from google_sheets import save_to_sheet

def main():
    print("🚀 Стартуем! Парсим Telegram каналы...")
    posts = parse_telegram_channels()
    print(f"📬 Найдено постов: {len(posts)}")

    for post in posts:
        if not post:
            print("⚠️ Пропущен пустой пост (None).")
            continue
        try:
            print(f"- {post['channel']} | {post['text'][:40]}...")
        except Exception as e:
            print(f"❌ Ошибка при выводе поста: {e}")

    valid_posts = [p for p in posts if p]
    if valid_posts:
        print("📤 Отправляем данные в Google Sheets...")
        save_to_sheet(valid_posts)
        print("✅ Успешно сохранено!")
    else:
        print("⚠️ Нет валидных постов для сохранения.")

if __name__ == "__main__":
    main()
