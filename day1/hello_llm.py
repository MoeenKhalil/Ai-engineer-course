import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# load the env file
load_dotenv()



# groq api key
my_api_key = os.getenv("GROQ_API_KEY")


if not my_api_key:
    raise ValueError("missing groq api key")
else:
    # creating the groq client
    client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"
role = "user"
prompt = "do you know moeen ul islam"

message = {
    "role": role,
    "content": prompt
}

messages = [message]

# request a response
response = client.chat.completions.create(model=model, messages=messages)

print(response.choices[0].message.content)
