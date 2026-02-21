from typing import TypedDict, List
from langgraph.graph import StateGraph, END

# We define the "Medical Chart" for our team.
# This structure acts as the shared clipboard between agents.
class TeamState(TypedDict):
    # The Researcher writes here.
    raw_research: str
    # A list of specific prices found.
    extracted_prices: List[float]
    # The Writer checks this before starting.
    is_data_valid: bool
    # Final output key.
    final_email: str

def researcher_node(state: TeamState):
    print("--- RESEARCHER: Scraping Data ---")
    # The agent performs its scrape and finds a price.
    found_price = 299.99
    
    # We update the state. This is the "Baton" being prepared.
    return {
        "raw_research": "Competitor X is selling Product Y at 299.99.",
        "extracted_prices": [found_price],
        "is_data_valid": True
    }

def writer_agent_node(state: TeamState):
    print("--- WRITER: Receiving the Baton ---")
    # The Writer does not guess. It pulls the data directly from the state keys.
    price_to_mention = state["extracted_prices"][0]
    
    if not state["is_data_valid"]:
        return {"final_email": "Error: Research was incomplete."}
        
    # The agent uses the structured data to build the final response.
    draft = f"Our competitor is at {price_to_mention}. We should match it."
    return {"final_email": draft}

# We wire the factory line together.
workflow = StateGraph(TeamState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_agent_node)

# We set the sequence of the handoff.
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", END)

app = workflow.compile()
