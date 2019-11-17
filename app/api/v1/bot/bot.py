import logging
import urllib.parse as urlparser

import requests

from teleautobot import settings


class Bot:

    logger = logging.getLogger(__name__)

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def send_tg_msg(self, msgtxt):
        url = urlparser.urljoin(self._bot_url(), 'sendMessage')
        headers = {
            'Content-Type': 'application/json',
        }
        params = {
            'chat_id': self.chat_id,
            'text': msgtxt,
        }
        resp = requests.post(url, params=params, headers=headers)

    def _bot_url(self):
        return 'https://api.telegram.org/bot/%s' % str(settings.BOT_TOKEN)
