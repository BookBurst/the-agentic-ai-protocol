import json
from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")

def route_with_cascade(user_prompt: str):
    # We define our cheap and expensive workers at the start to control costs.
    cheap_model = "<LATEST_FAST_MODEL>"
    expert_model = "<LATEST_REASONING_MODEL>"
    
    try:
        # Step 1: The system hands the task to the economical model first.
        response = client.chat.completions.create(
            model=cheap_model,
            messages=[{"role": "user", "content": user_prompt}],
            response_format={"type": "json_object"}
        )
        
        # We attempt to load the response as a clean data dictionary.
        result = json.loads(response.choices[0].message.content)
        print("Task completed successfully by the economical model.")
        return result
        
    except Exception as error:
        # Step 2: The cheap model failed to format the data correctly.
        # We catch the error and escalate the task to the expensive expert.
        print(f"Cheap model failed. Escalating to expert model. Error: {error}")
        
        expert_response = client.chat.completions.create(
            model=expert_model,
            messages=[
                {"role": "system", "content": "You are a fallback expert. Fix this task and output valid JSON."},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # The expert resolves the complex issue and returns the correct format.
        return json.loads(expert_response.choices[0].message.content)
