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

# We simulate a worker going completely off track.
macro_goal = "Find the monthly price of Competitor X's basic plan."
bad_research = "Competitor X was founded in 2012 by John Doe. They have 500 employees. Their office is in Seattle."

# We run the manager check before letting the agent continue its expensive research.
decision = evaluate_worker_output(macro_goal, bad_research)
print(f"Manager Decision: {decision}")
# Expected output: Manager Decision: FAIL
