from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# We instantiate a fast model for the execution node.
model = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0)

def researcher_node(state: AgentState):
    print("--- NODE: RESEARCHER IS PROCESSING ---")
    last_input = state["messages"][-1]
    response = model.invoke([HumanMessage(content=last_input)])
    
    return {
        "messages": [response.content],
        "is_finished": True
    }
