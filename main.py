#!/usr/bin/env python

import os

from environs import Env
from telegram import Update, ForceReply
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)
from pathlib import Path

env = Env()
env.read_env()


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Давай начнем')


def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)


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
