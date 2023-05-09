import os

import requests
from celery import shared_task


# celery -A library_service worker -l INFO/
from django.conf import settings


@shared_task
def send_telegram(text: str):
    token = settings.TOKEN
    url = "https://api.telegram.org/bot"
    chat_id = settings.SHAT_ID
    url += token
    method = url + "/sendMessage"

    req = requests.post(method, data={
        "chat_id": chat_id,
        "text": text
    })

    if req.status_code != 200:
        raise ValueError
