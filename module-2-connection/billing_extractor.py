from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")

class CustomerData(BaseModel):
    first_name: str
    last_name: str
    amount_due: float

def extract_customer_info(email_text: str):
    response = client.beta.chat.completions.parse(
        model="<LATEST_REASONING_MODEL>",
        messages=[
            {"role": "system", "content": "Extract the data. No small talk."},
            {"role": "user", "content": email_text}
        ],
        response_format=CustomerData
    )

    clean_data = response.choices[0].message.parsed
    print(f"Billing {clean_data.first_name} exactly ${clean_data.amount_due}")
