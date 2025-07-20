import asyncio
import random
from collections import deque
from telethon import TelegramClient
from telethon.errors import FloodWaitError, ChatWriteForbiddenError

from config_loader import load_config_from_txt
from csv_loader import load_recipients
from auth_manager import ensure_authorized
from sender import send_messages

async def main():
    print("📨 TeleSender — запуск рассылки с ротацией аккаунтов\n")

    accounts = load_config_from_txt()
    recipients = deque(load_recipients())

    if not accounts:
        print("❌ Не найдено ни одного отправителя в config.txt")
        return
    if not recipients:
        print("❌ Не найдено получателей в recipients.csv")
        return

    # Авторизация аккаунтов
    for acc in accounts:
        await ensure_authorized(acc)
    print("✅ Все аккаунты авторизованы или уже готовы к использованию.\n")

    # Запрашиваем сообщение
    print("Введите текст сообщения. Можно использовать <МоёИмя> и <ЕгоИмя>")
    message_template = input("Сообщение: ").strip()

    account_index = 0
    while recipients and account_index < len(accounts):
        acc = accounts[account_index]
        print(f"🚀 Пытаемся отправлять через: {acc['my_name']} ({acc['session_name']})")
        client = TelegramClient(acc["session_name"], acc["api_id"], acc["api_hash"])
        await client.start()

        try:
            while recipients:
                username = recipients[0]  # Смотрим на первого в очереди
                try:
                    await send_messages(
                        client=client,
                        recipients=[username],
                        my_name=acc["my_name"],
                        message_template=message_template,
                        min_delay=20,
                        max_delay=60
                    )
                    recipients.popleft()  # Удаляем, если успешно
                except (FloodWaitError, ChatWriteForbiddenError) as e:
                    print(f"⛔ Аккаунт {acc['my_name']} заблокирован: {e}")
                    raise e
        except (FloodWaitError, ChatWriteForbiddenError):
            account_index += 1  # Переходим к следующему аккаунту
        finally:
            await client.disconnect()
            print(f"🔌 Завершена работа аккаунта: {acc['my_name']}\n")

    if recipients:
        print("❌ Остались неполученные адресаты — не хватило рабочих аккаунтов:")
        for r in recipients:
            print(" -", r)
    else:
        print("✅ Рассылка завершена полностью.")

if __name__ == "__main__":
    asyncio.run(main())