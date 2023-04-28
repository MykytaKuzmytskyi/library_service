import os

import requests


def send_telegram(text: str):
    token = os.getenv("TELEGRAM_TOKEN")
    url = "https://api.telegram.org/bot"
    chat_id = os.getenv("CHAT_ID")
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": chat_id,
        "text": text
    })

    if r.status_code != 200:
        raise ValueError
