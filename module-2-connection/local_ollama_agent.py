from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# We initialize the local engine.
# This requires the Ollama application running in the background.
# The temperature stays low to force factual, predictable answers.
local_llm = ChatOllama(model="llama3", temperature=0.1)

def query_local_agent(user_input: str) -> str:
    print("Routing request to local hardware...")
    
    # The agent receives instructions exactly like a cloud model.
    # The message array structure remains identical.
    messages = [
        SystemMessage(content="Act as a strict data analyst. Be brief."),
        HumanMessage(content=user_input)
    ]

    # The invocation sends data to the local port (usually localhost:11434).
    # Zero data travels across the open internet.
    response = local_llm.invoke(messages)
    
    return response.content

# Executing a zero-cost local request.
output = query_local_agent("Calculate the risk of infinite loops.")
print(f"Agent Output:\n{output}")
