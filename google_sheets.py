def save_to_sheet(channels_with_keywords_in_name, channels_with_keywords_in_description):
    print("📄 Подключаемся к Google Sheets...")

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    base64_creds = os.getenv("GOOGLE_CREDS_BASE64")
    if not base64_creds:
        raise Exception("❌ GOOGLE_CREDS_BASE64 переменная не найдена")

    creds_json = base64.b64decode(base64_creds).decode("utf-8")
    parsed = json.loads(creds_json)
    print(f"📧 Авторизуемся как: {parsed['client_email']}")

    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as tmp:
        tmp.write(creds_json)
        tmp.flush()

        creds = ServiceAccountCredentials.from_json_keyfile_name(tmp.name, scope)
        client = gspread.authorize(creds)

        try:
            sheet_id = os.getenv("SPREADSHEET_ID")
            sheet_name = os.getenv("SHEET_NAME")
            print(f"📊 Открываем таблицу: {sheet_id}, лист: {sheet_name}")

            sheet = client.open_by_key(sheet_id).worksheet(sheet_name)

            # Сохраняем каналы с ключевыми словами в названии
            sheet.append_row(["Каналы с ключевыми словами в названии"])
            for channel in channels_with_keywords_in_name:
                sheet.append_row([
                    channel["channel"],
                    channel["title"],
                    channel["description"],
                    channel["subscribers"]
                ])

            # Сохраняем каналы с ключевыми словами в описании
            sheet.append_row(["Каналы с ключевыми словами в описании"])
            for channel in channels_with_keywords_in_description:
                sheet.append_row([
                    channel["channel"],
                    channel["title"],
                    channel["description"],
                    channel["subscribers"]
                ])

    except APIError as e:
        print(f"❌ Ошибка Google Sheets: {e}")
        raise
