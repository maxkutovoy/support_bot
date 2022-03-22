#!/usr/bin/env python

import os
import random

import vk_api as vk
from environs import Env
from google.cloud import storage
from telegram import Update, ForceReply
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)
from pathlib import Path
from vk_api.longpoll import VkLongPoll, VkEventType

from create_intent import create_intent

env = Env()
env.read_env()


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Давай начнем')


def vk_echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


def tg_bot(update: Update, context: CallbackContext):

    text = update.message.text
    answer = detect_intent_texts(text)
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id,
                             text=answer)


def detect_intent_texts(text):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow
    project_id = 'speech-recognition-lyfe'
    session_id = '479351324'
    language_code = 'ru'

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


def main():
    # tg_token = env.str('TG_TOKEN')
    # updater = Updater(tg_token)
    # dispatcher = updater.dispatcher
    #
    # dispatcher.add_handler(CommandHandler('start', start))
    # dispatcher.add_handler(MessageHandler(
    #     Filters.text & ~Filters.command,
    #     tg_bot
    #     )
    # )
    #
    # updater.start_polling()
    # updater.idle()

    vk_token = env.str('VK_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            vk_echo(event, vk_api)


if __name__ == '__main__':
    main()
