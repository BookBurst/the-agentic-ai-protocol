import time
from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")

def monitored_agent_call(prompt_text: str):
    # We record the exact millisecond the request starts.
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model="<LATEST_REASONING_MODEL>",
            messages=[{"role": "user", "content": prompt_text}]
        )
        
        # We calculate the total duration of the thought process.
        duration = time.time() - start_time
        
        # We set a hard limit. If the model takes over 15 seconds, something is wrong.
        if duration > 15.0:
            print(f"ALERT: High latency detected! Task took {duration:.2f} seconds.")
        
        return {
            "text": response.choices[0].message.content,
            "latency": duration
        }
        
    except Exception as error:
        print(f"System failure: {error}")
        return None

# We run a test to check the speed of our digital worker.
execution_data = monitored_agent_call("Draft a detailed project plan for a new app.")
if execution_data:
    print(f"Task completed in {execution_data['latency']:.2f}s.")
