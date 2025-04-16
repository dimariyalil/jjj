from telegram_parser import search_telegram_channels
from google_sheets import save_to_sheet

def main():
    print("🚀 Стартуем! Ищем Telegram каналы...")
    channels_with_keywords_in_name, channels_with_keywords_in_description = search_telegram_channels()
    
    print(f"📬 Найдено каналов с ключевыми словами в названии: {len(channels_with_keywords_in_name)}")
    print(f"📬 Найдено каналов с ключевыми словами в описании: {len(channels_with_keywords_in_description)}")

    if channels_with_keywords_in_name or channels_with_keywords_in_description:
        print("📤 Отправляем данные в Google Sheets...")
        save_to_sheet(channels_with_keywords_in_name, channels_with_keywords_in_description)
        print("✅ Успешно сохранено!")
    else:
        print("⚠️ Нет подходящих каналов для сохранения.")

if __name__ == "__main__":
    main()
