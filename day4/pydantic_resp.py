import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel
import json

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

# prepare schema
class Ticket(BaseModel):
    name: str
    email: str
    issue: str


schema = Ticket.model_json_schema()

resp_format = {
    "type": "json_object"
}

system_prompt = f"""
    Extract the personal info from the tiket and give me the same in json output following the schema {schema}
"""

message_system = {
    "role": "system",
    "content": system_prompt
}


customer_info = "hi my name is mark zukerberg, my email is abc@gmail.com and the issue i am facing is i am unable to loggin to your portal inorder to pay the fees"
prompt = f"""
    Take this customer info {customer_info} and extract the personal info from it
"""

message = {
    "role": role,
    "content": prompt
}



messages = [message_system, message]

# request a response
response = client.chat.completions.create(model=model, messages=messages, response_format=resp_format)


answer = response.choices[0].message.content



json_resp = json.loads(answer)
ticket = Ticket(**json_resp)

print(f"\nCustomer details from the ticket \n\nname:{ticket.name}\nemail:{ticket.email}\nissue:{ticket.issue}")

