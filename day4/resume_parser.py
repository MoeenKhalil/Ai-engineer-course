import os
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel
import json
from pypdf import PdfReader
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

# HR schema
class Ticket(BaseModel):
    name: str
    email: str
    skills: str
    designation:  list
    experience: str
    projects: list


schema = Ticket.model_json_schema()

resp_format = {
    "type": "json_object"
}


# Hr info list
hr_expectations = {
    "experience": "2.5+",
    "skills": ['python', 'java', 'docker', 'kubernetes']
}
system_prompt = f"""
    Extract the personal info from the resume and give me the same in json output following the schema {schema}
"""

message_system = {
    "role": "system",
    "content": system_prompt
}


with open("/Users/moeenkhalil/Downloads/Moeenul_Islam.pdf", "rb") as file:
    reader = PdfReader(file)

    raw_text = ""

    for page in reader.pages:
        text=page.extract_text()
        if text:
            raw_text += text + "\n"




prompt = f"""
    Take this candiates resume {raw_text} and extract the personal and professional info from it
"""

message = {
    "role": role,
    "content": prompt
}



messages = [message_system, message]

# # request a response
response = client.chat.completions.create(model=model, messages=messages, response_format=resp_format)


answer = response.choices[0].message.content



json_resp = json.loads(answer)
ticket = Ticket(**json_resp)

print(f"=========Candidate Details=============")
print(f"""
    Name:         :{ticket.name}\n
    Email         :{ticket.email}
    Skills        :{ticket.skills}
    Projects      :{ticket.projects}
    Experience    :{ticket.experience}
""")
# print(f"\nCustomer details from the ticket \n\nname:{ticket.name}\nemail:{ticket.email}\nissue:{ticket.issue}")


# calculate the match scrore
hr_message = {
    "role": role,
    "content": f"act as an hr for recruiment and calculate the match score for the attached information {ticket}"
}
hr_system = {
    "role": "system",
    "content": "you are an professional recruiter, provide a overall match score depdending on various parametres like skills, experience etc, give ouput in a json format in the form {'name':'match_score'}, match score should be on the scale of 1 to 10"
}

hr_messages = [hr_system, hr_message]
match_score = client.chat.completions.create(model=model, messages=hr_messages, response_format=resp_format)

match_score = response.choices[0].message.content

print(f"MATCH SCORE {match_score}")