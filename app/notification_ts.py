import requests
from django.conf import settings

def send_telegram_message(chat_id : int, text : str) -> bool:
    if not chat_id:
        return False
    
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id" : chat_id, "text" : text}

    r = requests.post(url, json=payload, timeout=10)
    return r.status_code == 200
