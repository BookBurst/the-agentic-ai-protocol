import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. THE CORRECTION LEDGER
# We use a simple dictionary to simulate a permanent database.
# In a production environment, this data lives in a vector database for semantic searching.
historical_corrections = {
    "sql_generation": "Always use the 'users_v2' table instead of 'users'. Do not use markdown formatting.",
    "email_drafting": "Never use greetings like 'Dear Sir'. Start directly with the first name."
}

# 2. THE INTELLIGENCE ENGINE
# We initialize our reasoning model with absolute zero temperature.
# We want deterministic obedience to our historical rules.
agent_llm = ChatOpenAI(model="<LATEST_REASONING_MODEL>", temperature=0.0)

def generate_with_historical_context(task_type: str, user_prompt: str) -> str:
    print(f"Initializing execution sequence for task type: {task_type}")
    
    # 3. THE KNOWLEDGE RETRIEVAL
    # The system checks the ledger to see if a human previously corrected this exact task type.
    # If a rule exists, we store it in a variable to inject later.
    retrieved_rule = historical_corrections.get(task_type, "")
    
    # We construct the baseline system instructions.
    base_instructions = "You are an expert autonomous assistant. Execute the request flawlessly."
    
    # 4. THE CONTEXT INJECTION
    # We append the retrieved human feedback directly into the system prompt.
    # This acts as the pinned ticket on the restaurant rail.
    if retrieved_rule:
        print("Historical correction found. Injecting constraints into the prompt context.")
        base_instructions += f"\n\nCRITICAL HUMAN FEEDBACK TO FOLLOW:\n{retrieved_rule}"
    else:
        print("No historical corrections found. Proceeding with baseline instructions.")
        
    # We build the final message array and send it to the model.
    messages = [
        SystemMessage(content=base_instructions),
        HumanMessage(content=user_prompt)
    ]
    
    response = agent_llm.invoke(messages)
    return response.content

# Execution Test 1: Triggering a task with known historical feedback.
print("\n--- Test 1: SQL Generation ---")
sql_result = generate_with_historical_context(
    task_type="sql_generation", 
    user_prompt="Write a query to count all active accounts."
)
print(f"Agent Output:\n{sql_result}")

# Execution Test 2: Triggering a brand new task with zero historical baggage.
print("\n--- Test 2: Python Scripting ---")
python_result = generate_with_historical_context(
    task_type="python_scripting", 
    user_prompt="Write a function to add two numbers."
)
print(f"Agent Output:\n{python_result}")
