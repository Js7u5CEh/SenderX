import os

CONFIG_PATH = "config.txt"

def load_config_from_txt():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError("❌ Файл config.txt не найден.")

    accounts = []
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Пропускаем пустые строки и комментарии
            try:
                parts = line.split(";")
                account = {}
                for part in parts:
                    key, value = part.split("=")
                    account[key.strip()] = value.strip()
                # Проверка обязательных полей
                if all(k in account for k in ("session_name", "api_id", "api_hash", "my_name")):
                    account["api_id"] = int(account["api_id"])  # Преобразуем api_id в число
                    accounts.append(account)
                else:
                    print(f"⚠️ Пропущена строка: {line} — отсутствуют обязательные поля.")
            except Exception as e:
                print(f"⚠️ Ошибка обработки строки: {line}\n{e}")
    return accounts
