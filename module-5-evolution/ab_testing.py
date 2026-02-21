import random
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. THE PROMPT REGISTRY
# In a production environment, this lives in a database or JSON file.
# We store the prompts with strict version numbers to track changes.
prompt_registry = {
    "v1.0": "You are a polite assistant. Answer questions directly.",
    "v1.1": "You are a polite assistant. Always ask for an account ID first."
}

# 2. THE ENGINE
# We initialize the model using our evergreen placeholder.
# A temperature of 0.0 keeps the text generation highly predictable.
agent_llm = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0.0)

def execute_ab_test(user_input: str) -> str:
    print("Routing incoming request...")

    # 3. THE TRAFFIC SPLIT
    # We generate a random number between 1 and 100.
    # 80% of requests go to the stable v1.0 prompt.
    # 20% of requests go to the experimental v1.1 prompt.
    roll = random.randint(1, 100)
    
    if roll <= 80:
        active_version = "v1.0"
    else:
        active_version = "v1.1"
        
    print(f"Traffic bucket assigned. Injecting prompt {active_version}.")

    # 4. THE INJECTION
    # We fetch the exact text from the registry using the selected version.
    system_text = prompt_registry[active_version]

    messages = [
        SystemMessage(content=system_text),
        HumanMessage(content=user_input)
    ]

    # 5. THE EXECUTION
    # The agent reads the injected memory and runs the logic.
    response = agent_llm.invoke(messages)
    return response.content

# Simulating a customer requesting a password reset.
print(execute_ab_test("I need to reset my password."))
