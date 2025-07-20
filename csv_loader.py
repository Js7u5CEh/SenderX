import csv

def load_recipients(csv_path: str = "recipients.csv") -> list[str]:
    recipients = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            raw = row.get("recipient", "").strip()
            if raw.startswith("t.me/"):
                username = raw.replace("t.me/", "").strip().lstrip("@")
                recipients.append(username)
            elif raw:
                recipients.append(raw.lstrip("@"))
    return recipients
