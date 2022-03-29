import json
import logging

import requests
import telegram
from environs import Env
from google.cloud import dialogflow

import log_handler

logger = logging.getLogger('New intent logger')


def get_json_from_file(file_path):
    with open(file_path) as file:
        json_raw = json.load(file)
    return json_raw


def create_intent(project_id):

    intents = get_json_from_file('questions.json')
    for intent_name, intent_description in intents.items():

        questions = intent_description['questions']
        answers = [intent_description['answer']]

        intents_client = dialogflow.IntentsClient()

        parent = dialogflow.AgentsClient.agent_path(project_id)
        training_phrases = []

        for question in questions:
            part = dialogflow.Intent.TrainingPhrase.Part(text=question)
            training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)

        messages = [{'text': {'text': [answer]}} for answer in answers]

        intent_for_dialogflow = dialogflow.Intent(
            display_name=intent_name,
            training_phrases=training_phrases,
            messages=messages,
        )

        response = intents_client.create_intent(
            request={"parent": parent, "intent": intent_for_dialogflow}
        )


def main():

    env = Env()
    env.read_env()

    tg_chat_id = env.str('TG_CHAT_ID')
    tg_bot = telegram.Bot(token=env.str('TG_TOKEN'))
    logger.setLevel(logging.WARNING)
    logger.addHandler(log_handler.TelegramLogsHandler(tg_bot, tg_chat_id))

    project_id = env.str('PROJECT_ID')
    try:
        create_intent(project_id)
    except requests.exceptions.HTTPError as error:
        logging.warning('Не удалось добавить новые вопросы')


if __name__ == '__main__':
    main()
