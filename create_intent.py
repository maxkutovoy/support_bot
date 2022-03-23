import json

from environs import Env
from google.cloud import dialogflow


def create_intent(project_id):

    with open('questions.json') as file:
        intents = json.load(file)

    for intent_name, intent_description in intents.items():

        questions = intent_description['questions']
        answers = []
        answer = intent_description['answer']
        answers.append(answer)

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

    project_id = env.str('PROJECT_ID')
    create_intent(project_id)


if __name__ == '__main__':
    main()
