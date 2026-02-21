# We define the shared memory structure first. 
class AgentState(dict):
    def __init__(self):
        super().__init__()
        self["input_query"] = ""
        self["retrieved_facts"] = ""
        self["final_answer"] = ""
        self["error_flag"] = False

# Node 1: The Retriever
def node_search(state: AgentState) -> AgentState:
    print("Executing Search Node...")
    try:
        state["retrieved_facts"] = "The system requires a minimum of 4GB RAM."
    except Exception:
        state["error_flag"] = True
    return state

# Node 2: The Generator
def node_generate(state: AgentState) -> AgentState:
    print("Executing Generation Node...")
    if state["error_flag"]:
        state["final_answer"] = "System failure: Cannot retrieve facts."
        return state
    
    facts = state["retrieved_facts"]
    state["final_answer"] = f"Based on the documents: {facts}"
    return state
