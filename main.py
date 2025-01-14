import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
secret_key = os.getenv('OPENAI_KEY')

client = OpenAI(
  api_key=secret_key
)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system",
     "content": "You are a helpful assistant."},
      {
      'role': "user",
      'content': "Who won the NBA championship in 2005?",
      }
  ]
)

print(response.choices[0].message.content);
