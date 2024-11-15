from openai import OpenAI
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Message, Run
import time
import logging
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()
USER_ROLE = "user"
ASSISTANT_ROLE = "engineer"

model = os.environ.get("OPENAI_MODEL")
assistant_id = os.environ.get("OPENAI_ASSISTANT_ID")

def load_requirements() -> str:
    try:
        with open("software_requirements.md", "r") as file:
            req = file.read()
        return req
    except FileNotFoundError:
        print("The requirements file does not exist.")

def write_response(response): 
    # Open the file in write mode ('w')
    with open("response.md", "w") as file:
        file.write(response)

use_case = ""
requirement = load_requirements()
message_content = f"Define testing scinarios using Cucumber and Gherkin and create some C++ tests using google test framework for the follwoing requirements: \n{requirement}"
print (message_content)

# Create an OpenAI assistant
def create_openai_assistant(name, instructions) -> Assistant:
    assistant = client.beta.assistants.create(
        name=name, 
        instructions=instructions, 
        model=model
    )
    return assistant

# Create an OpenAI Thread
def create_openai_thread(message_content) -> Thread:
    thread = client.beta.threads.create(messages=[
        {
            "role": USER_ROLE, 
            "content": message_content
        }
    ])
    return thread


# Create an OpenAI Message for the specified thread
def create_openai_message(thread_id) -> Message:
    message = client.beta.threads.messages.create(
        role= USER_ROLE, 
        thread_id=thread_id, 
        message_content = message_content
    )
    return message

# Create an OpenAI thread Run
def create_openai_run(assistant_id, thread_id, instructions) -> Run:
    run = client.beta.threads.runs.create(
        thread_id=thread_id, 
        assistant_id=assistant_id, 
        instructions= instructions
    )
    return run

def wait_for_run_completion(thread_id, run_id, sleep_interval=5):
    """
    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                write_response(response)
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

'''
assistant = create_openai_assistant(
    client, 
    "Software Automation Test Engineer", 
    """You are a professional Software Test Automation  Engineer that can do the following tasks:
        - Analyse  requirement and list the main points that need testing.
        - Break down this requirement into key testing elements (inputs, actions, expected outcomes).
        - Generate high-level test scenarios based on this requirement.
        - List positive and negative test scenarios for this functionality.
        - Create a detailed test case for [requirement] that includes steps, inputs, and expected outcomes.
        - Generate test cases for boundary conditions and edge cases.
        - Write simple system instructions for executing this test case.
        - Translate these technical steps into instructions suitable for end-users
        - create requirements from a given source code functions for C or C++ programming language """
    )
thread = create_openai_thread(
    client, 
    message_content
    )
'''

thread_id = create_openai_thread(message_content=message_content).id
run = create_openai_run(
   assistant_id,
   thread_id,
   "Please address the user as Developer")

# === Run ===
wait_for_run_completion(thread_id, run.id)

# ==== Steps --- Logs ==
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
print(f"Steps---> {run_steps.data[0]}")