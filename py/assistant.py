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

def load_requirements(req_file: str) -> str:
    try:
        with open(req_file, "r") as file:
            req = file.read()
        return req
    except FileNotFoundError:
        print("The requirements file does not exist.")

def load_sourcecode(src_file:str) -> str:
    try:
        with open(src_file, "r") as file:
            code = file.read()
        return code
    except FileNotFoundError:
        print("The source code file does not exist.")

client = OpenAI()
USER_ROLE = "user"
ASSISTANT_ROLE = "engineer"
DUMP_PROMPT = True
DUMP_RESPONSE = True

model = os.environ.get("OPENAI_MODEL")
assistant_id = os.environ.get("OPENAI_ASSISTANT_ID")
requirement_file = "software_requirements.rst"
sourcecode_file = "code.cpp"
requirement = load_requirements(requirement_file)
sourcecode = load_sourcecode(sourcecode_file)
test_framework = "GoogleTest"

def write_prompt(prompt): 
    if DUMP_PROMPT:
        print("==================================================================")
        print("=========================== PROMPT ===============================")
        print("==================================================================")
        print(prompt)
        print("==================================================================")

    # Open the file in write mode ('w')
    with open("prompt.md", "w") as file:
        file.write(prompt)

def write_response(response): 
    if DUMP_RESPONSE:
        print("==================================================================")
        print("====================== ASSISTANT RESPONSE ========================")
        print("==================================================================")
        print(response)
        print("==================================================================")

    # Open the file in write mode ('w')
    with open("response.md", "w") as file:
        file.write(response)

#prompt = f"What can be improved in the requirements ?\nRequirements: \n{requirement}"
prompt = f"Improve the quality of the requirements, and provide the result in the same data format (Sphinx-Needs)\n {requirement}"
#prompt = f"What are potintial mistakes in the requirements below:\n {requirement}"

# prompt = f"""Define feature scenarios using Cucumber and Gherkin and create C++ tests for each case 
#         using the {test_framework} Framework for the following requirements: 
#         \n{requirement}\nfor the 
#         source code:\n{sourcecode}"""

write_prompt(prompt)

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
        message_content = prompt
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
    print("Assistant request started !")
    """
    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        print("Processing ...")
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

# assistant = create_openai_assistant(
#     client, 
#     "Software Automation Test Engineer", 
#     """You are a professional Software Automation Test Engineer that can do the following tasks:
#         - Analyze requirements and list the main points that need testing.
#         - Break down this requirement into key testing elements (inputs, actions, expected outcomes).
#         - Generate high-level test scenarios based on this requirement.
#         - List positive and negative test scenarios for this functionality.
#         - Create a detailed test case for [requirement] that includes steps, inputs, and expected outcomes.
#         - Generate test cases for boundary conditions and edge cases.
#         - Write simple system instructions for executing this test case.
#         - Translate these technical steps into instructions suitable for end-users
#         - create requirements from a given source code functions for C or C++ programming language """
#     )
# thread = create_openai_thread(
#     client, 
#     message_content
#     )

thread_id = create_openai_thread(message_content=prompt).id
run = create_openai_run(
   assistant_id,
   thread_id,
   "Please address the user as Developer")

# === Run ===
wait_for_run_completion(thread_id, run.id)

# ==== Steps --- Logs ==
# run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
# print(f"Steps---> {run_steps.data[0]}")