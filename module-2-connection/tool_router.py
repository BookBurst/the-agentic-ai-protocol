# We import the json library to read the agent's output.
import json
# We import the OpenAI client.
from openai import OpenAI

# We set up our client with our private key.
client = OpenAI(api_key="your_api_key_here")

# We define our toolbox.
available_tools = [
    {
        "type": "function",
        "function": {
            "name": "update_billing",
            "description": "Updates a customer billing address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                    "new_address": {"type": "string"}
                },
                "required": ["customer_id", "new_address"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Sends an email to a customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                    "message": {"type": "string"}
                },
                "required": ["customer_id", "message"]
            }
        }
    }
]

def route_request(user_prompt: str):
    response = client.chat.completions.create(
        model="<LATEST_FAST_MODEL>",
        messages=[{"role": "user", "content": user_prompt}],
        tools=available_tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            print(f"Agent chose to use: {tool_call.function.name}")
            print(f"With these arguments: {tool_call.function.arguments}")
    else:
        print("Agent decided no tools were needed.")
