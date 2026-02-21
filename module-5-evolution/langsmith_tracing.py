import os
from openai import OpenAI
# We import a tracing library to wrap our standard API calls.
from langsmith.wrappers import wrap_openai
from langsmith import traceable

# We tell the system to send all diagnostic data to our secure dashboard.
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your_langsmith_key"

# We wrap our standard OpenAI client. 
# Now, every single interaction records automatically in the background.
client = wrap_openai(OpenAI(api_key="your_openai_key"))

# The @traceable tag acts as our flight recorder for this specific function.
@traceable(name="Process_Refund_Logic")
def decide_refund_action(customer_message: str):
    # The system logs the exact prompt, the model version, and the latency.
    response = client.chat.completions.create(
        model="<LATEST_FAST_MODEL>",
        messages=[
            {"role": "system", "content": "Analyze the refund request."},
            {"role": "user", "content": customer_message}
        ]
    )
    return response.choices[0].message.content

# When this runs, a full visual breakdown appears in the LangSmith platform.
decision = decide_refund_action("My coffee maker arrived broken.")
print("Action recorded and traced successfully.")
