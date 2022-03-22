#!/usr/bin/env python

import os

from environs import Env
from telegram import Update, ForceReply
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)
from pathlib import Path
from google.cloud import storage

env = Env()
env.read_env()


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Давай начнем')


def echo(update: Update, context: CallbackContext):

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
    tg_token = env.str('TG_TOKEN')
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        echo
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
