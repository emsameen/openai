from openai import OpenAI
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Message, Run

class Constants:
    assistant_id = "asst_G0l99J1mt8FoKs3lOofv7Jok"
    assistant_name = "Software Automation Test Engineer"
    thread_id = "thread_rwQoDHU6tiTPLyU4Ruko6bsi"
    USER_ROLE = "developer"
    ASSISTANT_ROLE = "assistant"

class AssistantManager:
    model = "gpt-4o-mini"
    def __init__(self, model=model) -> None:
        self.client = OpenAI()
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None

        # Retrieve the existing assistant if exists
        if Constants.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id=Constants.assistant_id
            )
        
        # Retrieve the existing thread if exists
        if Constants.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id=Constants.thread_id
            )
        else:
            self.create_thread()

    def retrieve_assistant(self, name) -> bool:
        __assistants_list = self.client.beta.assistants.list(
            order="desc",
            limit="5",
        )
        
        # search for assistant with the given name
        for __assistant in __assistants_list.data:
            if __assistant.name == name:
                self.assistant = __assistant
                Constants.thread_id = __assistant.id
                return True
        return False
            

    def create_assistant(self, name, instrauctions, tools):
        if not self.assistant:
            __assistant: Assistant = self.client.beta.assistants.create(
                name=name, 
                instructions=instrauctions,
                tools=tools,
                model=self.model
        )
        self.assistant = __assistant
        Constants.assistant_id = __assistant.id

        print(f"A new Assistant is created with id: {self.assistant.id}")

    def create_thread(self):
        if not self.thread:
            __thread = self.client.beta.threads.create()
            self.thread = __thread
            Constants.thread_id = __thread.id
            print(f"A new Thread is created with id: {self.thread.id}")
        else:
            print(f"There is already a valid thread with ID {self.thread.id}")

        
    def add_messages(self,content):
        if self.thread:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role=Constants.USER_ROLE, 
                content=content
            )
        else:
            print("Invalid thread")

    def run_assistant(self, instructions):
        if self.thread and self.assistant:
            self.run = self.client.beta.threads.runs.create(
                assistant_id=self.assistant.id,
                thread_id=self.thread.id,
                instructions=instructions
            )
        else:
            print("Error:: either thread or assistant is invalid")
    
    def process_message(self):
        if self.thread:
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            last_message = messages.data[0]
            role = last_message.role.capitalize()
            response = last_message.content[0].text.value

            print (f"SUMMARY: {role}: {response}")
        else:
            print("Invalid thread")
        


if __name__ == "__main__":
    assistant = AssistantManager()
    print(f"Current Assistant: {assistant.assistant.id}")
    print(f"Current Thread: {assistant.thread.id}")
    assistant.retrieve_assistant(Constants.assistant_name)
    #assistant.process_message()