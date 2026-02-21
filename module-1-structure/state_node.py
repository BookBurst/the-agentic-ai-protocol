from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# We instantiate a fast model for the execution node.
# Temperature zero keeps the output predictable and grounded.
model = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0)

def researcher_node(state: AgentState):
    print("--- NODE: RESEARCHER IS PROCESSING ---")
    
    # We pull the last message from our shared pad.
    last_input = state["messages"][-1]
    
    # The model processes the input and generates a response.
    response = model.invoke([HumanMessage(content=last_input)])
    
    # We return the update to the state.
    return {
        "messages": [response.content],
        "is_finished": True
    }
