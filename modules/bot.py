import urllib.parse
import urllib.request
import os
import json
from time import sleep

# Decorator para atrasar chamadas em 3 segundos
def rate_limit(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        sleep(5)
        return result
    return wrapper

class BotTelegram():
    def __init__(self, token, chatId):
        self._token = token
        self._chatId = chatId
        self._base = f'https://api.telegram.org/bot{self._token}'

    @rate_limit
    def sendMessage(self, message, markdown: bool = True):
        """
        Envia uma mensagem de texto. Se markdown=True, habilita parse_mode Markdown.
        """
        params = {
            'chat_id': self._chatId,
            'text': message
        }
        if markdown:
            params['parse_mode'] = 'Markdown'
        url = f"{self._base}/sendMessage?" + urllib.parse.urlencode(params)
        try:
            urllib.request.urlopen(url)
            print('[telegram] Mensagem enviada com sucesso')
            return {
                    "response": True,
                    "message": "Mensagem c/ foto enviada com sucesso (urllib.request.urlopen)" 
                }
        except Exception:
            print('[telegram] Erro ao enviar sendMessage, tentando fallback curl…')
            payload = json.dumps(params)
            cmd = (
                f"curl -s -X POST {self._base}/sendMessage "
                f"-H 'Content-Type: application/json' "
                f"-d '{payload}'"
            )
            if os.system(cmd) == 0:
                print('[telegram] Mensagem enviada com sucesso (curl)')
                return {
                    "response": True,
                    "message": "Mensagem c/ foto enviada com sucesso (curl)" 
                }
            print('[telegram] Erro ao tentar enviar mensagem')
            return {
                    "response": True,
                    "message": "Erro ao enviar mensagem c/ foto (curl)" 
                }

    @rate_limit
    def sendPhoto(self, photo_url: str, caption: str = ''):
        """Anexa uma foto via URL e opcionalmente envia legenda em Markdown."""
        params = {
            'chat_id': self._chatId,
            'photo': photo_url,
            'caption': caption,
            'parse_mode': 'Markdown'
        }
        url = f'{self._base}/sendPhoto?' + urllib.parse.urlencode(params)
        try:
            urllib.request.urlopen(url)
            print('[telegram] Foto enviada com sucesso')
            return {
                    "response": True,
                    "message": "Mensagem c/ foto enviada com sucesso (urllib.request.urlopen)" 
                }
        except Exception:
            print('[telegram] Erro ao enviar sendPhoto, tentando fallback curl…')
            payload = json.dumps(params)
            cmd = (
                f"curl -s -X POST {self._base}/sendPhoto "
                f"-H 'Content-Type: application/json' "
                f"-d '{payload}'"
            )
            if os.system(cmd) == 0:
                print('[telegram] Foto enviada com sucesso (curl)')
                return {
                    "response": True,
                    "message": "Mensagem c/ foto enviada com sucesso (curl)" 
                }
            print('[telegram] Erro ao enviar foto')
            return {
                    "response": True,
                    "message": "Erro ao enviar mensagem c/ FOTO (curl)" 
            }