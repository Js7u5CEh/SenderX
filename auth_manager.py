import os
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

async def ensure_authorized(account: dict):
    session_path = f"{account['session_name']}.session"
    client = TelegramClient(
        account['session_name'],
        account['api_id'],
        account['api_hash']
    )

    await client.connect()

    if not await client.is_user_authorized():
        print(f"\n🔐 Авторизация аккаунта: {account['my_name']}")

        phone = input("Введите номер телефона (в формате +1234567890): ")
        await client.send_code_request(phone)
        code = input("Введите код из Telegram: ")
        try:
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input("⚠️ Установлен пароль 2FA. Введите его: ")
            await client.sign_in(password=password)

        print("✅ Авторизация прошла успешно!")

    await client.disconnect()
