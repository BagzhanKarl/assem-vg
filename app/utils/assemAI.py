import time
from openai import OpenAI


class AssemAI:
    def __init__(self, api_key, assistant=None):
        self.api = api_key
        self.client = OpenAI(api_key=self.api)
        self.run = None
        self.temp = 1.0
        self.assistant = assistant if assistant else 'asst_sr0IcR2W3q5mzhJO0m8o54fT'

    def update_assist_data(self, name, instruction, temp):
        assistant_update = self.client.beta.assistants.update(
            assistant_id=self.assistant,
            name=name,
            instructions=instruction,
            model='gpt-4o-mini-2024-07-18',
            temperature=temp,
        )

    def generate_answer(self, context):
        thread = self.client.beta.threads.create(
            messages=context,
        )
        run = self.client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=self.assistant)
        while run.status != 'completed':
            run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            time.sleep(1)
            print('Waiting')

        else:
            print('Done')

        message = self.client.beta.threads.messages.list(thread_id=thread.id)
        messages = message.data
        latest = messages[0]
        return latest.content[0].text.value