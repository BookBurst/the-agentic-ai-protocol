import json
from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")

def check_prompt_completeness(user_input: str) -> dict:
    # We define exactly what the agent needs to know to send an email.
    system_instruction = """
    Read the user request. To send an email, we absolutely need two things:
    1. 'recipient_name'
    2. 'document_topic'
    If both are present, output: {"status": "COMPLETE", "missing": "none"}.
    If anything is missing, output: {"status": "INCOMPLETE", "missing": "Name the missing piece"}.
    """
    
    # We force the fast model to evaluate the human's clarity.
    response = client.chat.completions.create(
        model="<LATEST_FAST_MODEL>",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        response_format={"type": "json_object"}
    )
    
    # We parse the ruling to decide our next routing step.
    return json.loads(response.choices[0].message.content)
