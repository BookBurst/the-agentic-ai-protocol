# We define the shared memory structure first. 
# This dictionary acts as the conveyor belt moving between our agent functions.
class AgentState(dict):
    def __init__(self):
        super().__init__()
        self["input_query"] = ""
        self["retrieved_facts"] = ""
        self["final_answer"] = ""
        self["error_flag"] = False

# Node 1: The Retriever
# This function only cares about finding facts. It ignores everything else.
def node_search(state: AgentState) -> AgentState:
    print("Executing Search Node...")
    try:
        # Simulated database lookup based on the input query.
        state["retrieved_facts"] = "The system requires a minimum of 4GB RAM."
    except Exception:
        state["error_flag"] = True
    return state

# Node 2: The Generator
# This function takes the facts and formats the final response.
def node_generate(state: AgentState) -> AgentState:
    print("Executing Generation Node...")
    if state["error_flag"]:
        state["final_answer"] = "System failure: Cannot retrieve facts."
        return state
    
    facts = state["retrieved_facts"]
    state["final_answer"] = f"Based on the documents: {facts}"
    return state

# The Agnostic Graph Execution
# We manually string the nodes together in a strict sequence.
# Data flows forward. It never loops back.
def run_pipeline(user_text: str):
    current_state = AgentState()
    current_state["input_query"] = user_text
    
    # The data moves through the graph step by step.
    current_state = node_search(current_state)
    current_state = node_generate(current_state)
    
    return current_state["final_answer"]

# Triggering the system.
result = run_pipeline("What are the hardware requirements?")
print(f"Final Output: {result}")
