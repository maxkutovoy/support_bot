import logging
import os

from environs import Env


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot):
        super().__init__()
        self.tg_bot = tg_bot

    def emit(self, record):
        env = Env()
        env.read_env()

        log_entry = self.format(record)
        self.tg_bot.send_message(
            chat_id=env.str('TG_CHAT_ID'),
            text=log_entry
        )
