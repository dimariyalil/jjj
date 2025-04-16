import os
import json
import gspread
import base64
import tempfile
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import APIError

def save_to_sheet(posts):
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

            for post in posts:
                try:
                    sheet.append_row([
                        post['channel'],
                        post['text'],
                        post['url'],
                        post['date'],
                        post['source'],
                        post['positive']
                    ])
                    print(f"✅ Добавлена строка из канала: {post['channel']}")
                except Exception as e:
                    print(f"⚠️ Не удалось записать строку: {e}")
        except APIError as e:
            print(f"❌ Ошибка Google Sheets: {e}")
            raise
