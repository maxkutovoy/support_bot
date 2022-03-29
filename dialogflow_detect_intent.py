#!/usr/bin/env python

from environs import Env


def detect_intent_texts(text):
    from google.cloud import dialogflow

    env = Env()
    env.read_env()

    project_id = env.str('PROJECT_ID')
    session_id = env.str('TG_CHAT_ID')
    language_code = env.str('LANGUAGE_CODE', 'ru')

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text
