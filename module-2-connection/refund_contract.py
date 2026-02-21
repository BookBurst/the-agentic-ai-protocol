# We import BaseModel to build our strict data contract.
from pydantic import BaseModel
# We import the OpenAI client to talk to our model.
from openai import OpenAI

# We set up our client with our private key.
client = OpenAI(api_key="your_api_key_here")

# This class is the contract. 
# The AI must provide exactly these fields in these exact formats.
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
        # It physically blocks the AI from outputting regular conversational text.
        response_format=RefundCommand,
    )
    
    # We pull the clean, verified data object out of the response.
    return response.choices[0].message.parsed

# We simulate a messy request from a customer.
messy_ticket = "I bought the blue shirt yesterday for $20 but it has a hole in it! My ID is 9982."

# We run the command through our contract.
safe_data = generate_refund_data(messy_ticket)

# We print the isolated integer. 
# This proves the AI stripped out the dollar sign and converted $20 to 2000 cents.
print(safe_data.amount_cents)
