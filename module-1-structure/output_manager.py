import json
from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")

def evaluate_worker_output(original_goal: str, worker_output: str) -> str:
    # We assign a strict, non-creative role to our fast model.
    system_prompt = """
    You are a ruthless project manager.
    Read the original goal. Read the worker's output.
    If the output directly answers the goal, reply strictly with {"status": "PASS"}.
    If the worker added useless information or missed the point, reply strictly with {"status": "FAIL"}.
    """
    
    # We send the context to the model and force a clean data structure back.
    evaluation = client.chat.completions.create(
        model="<LATEST_FAST_MODEL>",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"GOAL: {original_goal}\nOUTPUT: {worker_output}"}
        ],
        response_format={"type": "json_object"}
    )
    
    # We parse the result so our main script knows whether to proceed or loop back.
    result = json.loads(evaluation.choices[0].message.content)
    return result["status"]
