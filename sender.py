import asyncio
import random
from telethon import TelegramClient
from telethon.errors import FloodWaitError, PeerIdInvalidError, UserPrivacyRestrictedError

async def send_messages(client: TelegramClient, recipients: list[str], my_name: str, message_template: str, min_delay=20, max_delay=60):
    me = await client.get_me()
    for username in recipients:
        try:
            user = await client.get_entity(username)
            his_name = user.first_name or ""
            final_message = message_template.replace("<МоёИмя>", my_name).replace("<ЕгоИмя>", his_name)

            if user.id == me.id:
                print(f"⚠️ Пропущен сам себе: {username}")
                continue

            await client.send_message(user, final_message)
            print(f"✅ Отправлено {username}")
        except FloodWaitError as e:
            print(f"⏳ Flood wait: ждём {e.seconds} секунд...")
            await asyncio.sleep(e.seconds)
        except (PeerIdInvalidError, UserPrivacyRestrictedError):
            print(f"❌ Ошибка доступа к {username} — пропускаем")
        except Exception as e:
            print(f"⚠️ Не удалось отправить {username}: {e}")

        delay = random.randint(min_delay, max_delay)
        print(f"⏱ Пауза {delay} сек...")
        await asyncio.sleep(delay)
