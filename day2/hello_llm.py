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
prompt = "i am planning to start a instagram/youtube page for content creation around travelling, photography, moto vlogging, lifestyle, psychology, suggest 5 unqiue yet easily rememberable names"

message_system = {
    "role": "system",
    "content": "You are a professional in summarizing long articles into crsipt and short descriptions"
}
message = {
    "role": role,
    "content": prompt
}

messages = [message, message_system]

# request a response
# temperature reanges between 0 and 2
response = client.chat.completions.create(model=model, messages=messages, temperature=2)

print(response.choices[0].message.content)
