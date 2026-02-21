from pydantic import BaseModel # We bring in the strict bouncer to verify the output.
from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")

# We define the exact shape of the data we want.
# The AI must follow this blueprint perfectly.
class CustomerData(BaseModel):
    first_name: str
    last_name: str
    amount_due: float

def extract_customer_info(email_text: str):
    # We send the email to the model and force it to use our blueprint.
    response = client.beta.chat.completions.parse(
        model="<LATEST_REASONING_MODEL>",
        messages=[
            {"role": "system", "content": "Extract the data. No small talk."},
            {"role": "user", "content": email_text}
        ],
        # This line tells the AI to format its answer exactly like our CustomerData class.
        response_format=CustomerData
    )

    # We pull the clean, verified data object out of the response.
    clean_data = response.choices[0].message.parsed
    
    # Now we can use the data confidently without breaking our software.
    print(f"Billing {clean_data.first_name} exactly ${clean_data.amount_due}")

# We test the agent with a casual message.
extract_customer_info("Hey, it's Mark Smith. I owe 45.50 for the monthly plan.")
