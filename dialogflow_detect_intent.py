#!/usr/bin/env python

def detect_intent_texts(text, df_project_id, session_id, language_code):
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(df_project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )

    return response
