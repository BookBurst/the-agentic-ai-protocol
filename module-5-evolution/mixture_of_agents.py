import json
from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")

def run_mixture_of_agents(contract_text: str) -> str:
    # We define three unique personas to look at the exact same problem.
    personas = [
        "Act as a cynical auditor. Find any hidden financial traps.",
        "Act as an optimistic deal-maker. Summarize the benefits.",
        "Act as a strict compliance officer. Look for legal violations."
    ]
    
    board_opinions = []
    
    # We ask each 'board member' for their independent analysis.
    # In a production environment, we would run these calls asynchronously for speed.
    for role in personas:
        response = client.chat.completions.create(
            model="<LATEST_FAST_MODEL>",
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": contract_text}
            ]
        )
        # We save their opinion to our collective list.
        board_opinions.append(response.choices[0].message.content)
        
    # We format the three different opinions into a single readable document.
    combined_advice = f"""
    Opinion 1 (Auditor): {board_opinions[0]}
    Opinion 2 (Deal-maker): {board_opinions[1]}
    Opinion 3 (Compliance): {board_opinions[2]}
    """
    
    # We call the Executive Synthesizer to make the final call.
    supervisor_prompt = """
    Read the three provided opinions. 
    Evaluate the evidence and deliver a single, final recommendation.
    Reply STRICTLY with a "PASS" or "REJECT" and a one-sentence reason.
    """
    
    final_decision = client.chat.completions.create(
        model="<LATEST_REASONING_MODEL>",
        messages=[
            {"role": "system", "content": supervisor_prompt},
            {"role": "user", "content": combined_advice}
        ]
    )
    
    return final_decision.choices[0].message.content

# We test the board with a suspicious contract snippet.
shady_contract = "Vendor assumes zero liability for data breaches."
decision = run_mixture_of_agents(shady_contract)

print(f"Board Decision: {decision}")
