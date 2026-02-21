# We import BaseModel to build our strict data contract.
from pydantic import BaseModel
# We import the OpenAI client to talk to our model.
from openai import OpenAI

# We set up our client with our private key.
client = OpenAI(api_key="your_api_key_here")

# This class is the contract. 
class RefundCommand(BaseModel):
    # We force the amount to be a whole number, preventing dollar signs.
    amount_cents: int
    # We force the customer ID to be a text string.
    customer_id: str
    # We ask for a short reason to log in our database.
    reason_for_refund: str

def generate_refund_data(customer_request: str) -> RefundCommand:
    # We send the raw user request to the model.
    response = client.beta.chat.completions.parse(
        model="<LATEST_FAST_MODEL>",
        messages=[
            {"role": "system", "content": "You process refunds. Convert dollar amounts to cents. Follow the exact data structure."},
            {"role": "user", "content": customer_request}
        ],
        # This single line forces the AI to obey our strict contract.
        response_format=RefundCommand,
    )
    
    # We pull the clean, verified data object out of the response.
    return response.choices[0].message.parsed
