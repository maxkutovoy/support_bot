import logging
import random

import requests.exceptions
import telegram
import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

import log_handler
from service import detect_intent_texts

logger = logging.getLogger('VK logger')


def vk_send_answer(event, vk_api):
    answer = detect_intent_texts(event.text)
    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1, 1000)
    )


def main():
    env = Env()
    env.read_env()

    tg_bot = telegram.Bot(token=env.str('TG_TOKEN'))
    logger.setLevel(logging.WARNING)
    logger.addHandler(log_handler.TelegramLogsHandler(tg_bot))

    vk_token = env.str('VK_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                vk_send_answer(event, vk_api)
            except requests.exceptions.HTTPError as error:
                logger.warning('Проблема с ботом Вконтакте')


if __name__ == '__main__':
    main()
