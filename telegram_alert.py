import requests

TELEGRAM_BOT_TOKEN = '8595368042:AAFYIXmueIH5HtxnIEdj_FkUI0us5BnGGdU'
TELEGRAM_CHAT_ID = '772210684'

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print("Alerta do Telegram enviado com sucesso!")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar alerta do Telegram: {e}")
