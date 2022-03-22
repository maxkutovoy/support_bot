import json

from environs import Env
from google.cloud import storage

env = Env()
env.read_env()


def create_intent():
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

    project_id = 'speech-recognition-lyfe'
    session_id = '479351324'
    language_code = 'ru'

    with open('questions.json') as file:
        questions = json.load(file)

    getting_job_intent = questions['Устройство на работу']
    getting_job_questions = getting_job_intent['questions']
    answers = []
    getting_job_answers = getting_job_intent['answer']
    answers.append(getting_job_answers)


    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []

    for question in getting_job_questions:
        print(question)
        part = dialogflow.Intent.TrainingPhrase.Part(text=question)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    # text = dialogflow.Intent.Message.Text(text=answers)
    # messages = dialogflow.Intent.Message(text=text)

    display_name = 'Как устроиться к вам на работу'
    messages = [{'text': {'text': [answer]}} for answer in answers]

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=messages
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    # print("Intent created: {}".format(response))


def main():
    create_intent()


if __name__ == '__main__':
    main()
