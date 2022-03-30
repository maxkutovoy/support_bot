import logging
import random

import requests.exceptions
import telegram
import vk_api as vk
from environs import Env
from google.api_core.exceptions import InvalidArgument
from vk_api.longpoll import VkLongPoll, VkEventType

import log_handler
from dialogflow_detect_intent import detect_intent_texts

logger = logging.getLogger('VK logger')


def vk_send_answer(event, vk_api, df_project_id, language_code):
    vk_user_id = event.user_id

    df_response = detect_intent_texts(
        event.text,
        df_project_id=df_project_id,
        session_id=vk_user_id,
        language_code=language_code,
    )

    if not df_response.query_result.intent.is_fallback:
        answer = df_response.query_result.fulfillment_text
        vk_api.messages.send(
            user_id=vk_user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )


def main():
    env = Env()
    env.read_env()

    tg_chat_id = env.str('TG_CHAT_ID')
    tg_bot = telegram.Bot(token=env.str('TG_TOKEN'))
    logger.setLevel(logging.WARNING)
    logger.addHandler(log_handler.TelegramLogsHandler(tg_bot, tg_chat_id))

    df_project_id = env.str('PROJECT_ID')
    language_code = env.str('LANGUAGE_CODE', 'ru')
    vk_token = env.str('VK_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                vk_send_answer(event, vk_api, df_project_id, language_code)
            except requests.exceptions.HTTPError as error:
                logger.warning('Проблема с ботом Вконтакте')


if __name__ == '__main__':
    main()
