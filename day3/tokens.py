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

prompt1 = "hi!"
prompt2 = "give a brief description for my travellling instagram page under 100 words"
prompt3 = "give a detailed review of kawasaki versys 300"


prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
    message_system = {
        "role": "system",
        "content": "You are a professional in summarizing long articles into crsip and short descriptions"
    }
    message = {
        "role": role,
        "content": prompt
    }

    messages = [message]

    # request a response
    response = client.chat.completions.create(model=model, messages=messages, max_tokens=500)

    # token usage
    usage = response.usage

    print(f"Prompt: {prompt} --> my tokens {usage.prompt_tokens} completion_tokens: {usage.completion_tokens} total_tokens: {usage.total_tokens} Finish_reason {response.choices[0].finish_reason} ")

    print(response.choices[0].message.content)
