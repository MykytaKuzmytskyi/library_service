import requests


def send_telegram(text: str):
    token = "5810198718:AAEi5i1P74rjEo05zphnWQyAvv9C0xCNTdo"
    url = "https://api.telegram.org/bot"
    chat_id = "482631115"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": chat_id,
         "text": text
          })

    if r.status_code != 200:
        raise ValueError
