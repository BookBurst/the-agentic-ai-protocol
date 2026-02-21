import json
from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")

def grade_agent_response(user_query: str, perfect_answer: str, agent_attempt: str) -> dict:
    # We define the strict persona and the binary grading rules for our judge.
    judge_instructions = """
    You are an expert Quality Assurance Judge.
    Compare the AGENT ATTEMPT to the PERFECT ANSWER for the given USER QUERY.
    Did the agent include all factual information without adding false details?
    Reply STRICTLY in JSON format with two keys: 
    'score' (either "PASS" or "FAIL") and 'reasoning' (a brief explanation).
    """
    
    # We format the data clearly so the judge model does not get confused.
    evaluation_data = f"""
    USER QUERY: {user_query}
    PERFECT ANSWER: {perfect_answer}
    AGENT ATTEMPT: {agent_attempt}
    """
    
    # We call our smartest, most expensive model to do the grading.
    response = client.chat.completions.create(
        model="<LATEST_REASONING_MODEL>",
        messages=[
            {"role": "system", "content": judge_instructions},
            {"role": "user", "content": evaluation_data}
        ],
        response_format={"type": "json_object"}
    )
    
    # The function returns the structured grading report.
    return json.loads(response.choices[0].message.content)

# We test the system with a scenario where the agent forgets a key detail.
query = "How long do I have to return a laptop?"
golden_rule = "You have 14 days to return electronics. A receipt is required."
flawed_agent = "You have 14 days to return electronics."

# The judge catches the missing receipt requirement and fails the attempt.
grade_report = grade_agent_response(query, golden_rule, flawed_agent)
print(f"QA Result: {grade_report}")
