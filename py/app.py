from openai import OpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessage

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "tell me a new joke"}
  ]
)

result: ChatCompletionMessage = completion.choices[0].message
print(result.content)