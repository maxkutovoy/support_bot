import logging

import requests
import telegram
from environs import Env
from google.api_core.exceptions import InvalidArgument
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)

import log_handler
from dialogflow_detect_intent import detect_intent_texts


logger = logging.getLogger('TG logger')


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Давай начнем')


def tg_send_answer(update: Update, context: CallbackContext):
    df_project_id = context.bot_data['df_project_id']
    language_code = context.bot_data['language_code']

    text = update.message.text
    chat_id = update.message.chat_id

    try:
        answer = detect_intent_texts(
            text,
            df_project_id=df_project_id,
            session_id=chat_id,
            language_code=language_code,
        )
    except InvalidArgument:
        answer = 'Неверный запрос. Бот понимает только текст.'
        return answer

    context.bot.send_message(
        chat_id=chat_id,
        text=answer,
    )


def main():
    env = Env()
    env.read_env()

    tg_token = env.str('TG_TOKEN')
    tg_chat_id = env.str('TG_CHAT_ID')
    tg_bot = telegram.Bot(token=tg_token)
    logger.setLevel(logging.WARNING)
    logger.addHandler(log_handler.TelegramLogsHandler(tg_bot, tg_chat_id))

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    dispatcher.bot_data['df_project_id'] = env.str('PROJECT_ID')
    dispatcher.bot_data['language_code'] = env.str('LANGUAGE_CODE', 'ru')

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        tg_send_answer
        )
    )

    try:
        updater.start_polling()
        updater.idle()
    except requests.exceptions.HTTPError as error:
        logger.warning('Проблема с телеграм ботом ')


if __name__ == '__main__':
    main()
