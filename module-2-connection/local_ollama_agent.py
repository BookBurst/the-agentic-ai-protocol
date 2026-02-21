from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# We initialize the local engine. Requires Ollama running.
local_llm = ChatOllama(model="llama3", temperature=0.1)

def query_local_agent(user_input: str) -> str:
    print("Routing request to local hardware...")
    messages = [
        SystemMessage(content="Act as a strict data analyst. Be brief."),
        HumanMessage(content=user_input)
    ]
    response = local_llm.invoke(messages)
    return response.content
