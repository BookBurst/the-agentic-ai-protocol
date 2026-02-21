# We import BaseModel to create our strict data mold.
from pydantic import BaseModel
# We import the OpenAI client.
from openai import OpenAI

# We initialize our client with our private key.
client = OpenAI(api_key="your_api_key_here")

# This class is the rigid box. The AI cannot deviate from these exact fields.
class TicketData(BaseModel):
    account_number: str
    issue_category: str
    # We force the AI to summarize the problem in under 10 words.
    short_summary: str

def process_support_email(email_text: str) -> TicketData:
    # We call the model to read the unstructured email.
    response = client.beta.chat.completions.parse(
        model="<LATEST_FAST_MODEL>",
        messages=[
            # We give the model a highly restrictive command.
            {"role": "system", "content": "Extract the account number and issue. Do not add conversational text."},
            {"role": "user", "content": email_text}
        ],
        # We enforce the strict Pydantic mold to block unwanted text.
        response_format=TicketData,
    )
    
    # We pull the perfectly formatted data out of the response object.
    return response.choices[0].message.parsed

# We simulate a messy customer email.
messy_email = "Hi, my account is ACCT-9923 and my dashboard keeps freezing. Please help ASAP!"

# We run the pipeline.
clean_data = process_support_email(messy_email)

# The output is now safe to use in standard Python code.
print(clean_data.account_number) 
print(clean_data.short_summary)
