# We import the json library to read the agent's output.
import json
# We import the OpenAI client.
from openai import OpenAI

# We set up our client with our private key.
client = OpenAI(api_key="your_api_key_here")

# We define our toolbox. We give the AI a list of tools it can use.
# We describe what each tool does so the AI understands when to pick it.
available_tools = [
    {
        "type": "function",
        "function": {
            # The exact name of our local Python function.
            "name": "update_billing",
            # The description the AI reads to understand the tool's purpose.
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
    # We send the prompt and the toolbox to the model.
    response = client.chat.completions.create(
        model="<LATEST_FAST_MODEL>",
        messages=[{"role": "user", "content": user_prompt}],
        # We hand the toolbox to the agent here.
        tools=available_tools,
        # We tell the agent to pick a tool automatically if it needs one.
        tool_choice="auto"
    )

    # We check if the agent decided to use a tool.
    response_message = response.choices[0].message
    
    # If tool_calls exists, the agent wants to use our local functions.
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            # The agent tells us which tool it picked and what data to pass.
            print(f"Agent chose to use: {tool_call.function.name}")
            print(f"With these arguments: {tool_call.function.arguments}")
    else:
        # If the user just said "Hello", the agent will ignore the tools.
        print("Agent decided no tools were needed.")

# We test the agent with a complex double request.
complex_prompt = "Change the address for user 992 to 123 Main St and email them a confirmation."

# We run the command.
route_request(complex_prompt)
