from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

# ==========================================
# PHASE 1: DEFINING THE STATE & WORKERS
# ==========================================

# We define the strict data structure for our customer service ticket.
class TriageState(TypedDict):
    inbound_email: str
    sender_address: str
    categorized_intent: str
    extracted_budget: int
    drafted_reply: str
    human_approval: bool

def classify_and_draft(state: TriageState):
    # The agent reads the email, updates the CRM via API, and writes the reply.
    # (We simulate the API call logic here for brevity).
    print("Agent: Updating CRM and drafting response.")
    
    simulated_draft = "Hello, I saw your budget is $50k. Let's schedule a call."
    
    # We save the unapproved draft to the clipboard and flag approval as False.
    return {"drafted_reply": simulated_draft, "human_approval": False}

def send_to_client(state: TriageState):
    # This function actually fires the email over the open internet.
    # It must never run without human permission.
    final_message = state["drafted_reply"]
    print(f"System: Dispatching email -> {final_message}")
    return state


# ==========================================
# PHASE 2: ASSEMBLING WITH HUMAN-IN-THE-LOOP
# ==========================================

# We create the workflow using our exact ticket structure.
workflow = StateGraph(TriageState)

# We add our specific worker nodes.
workflow.add_node("process_email", classify_and_draft)
workflow.add_node("dispatch_email", send_to_client)

# We connect the nodes sequentially.
workflow.set_entry_point("process_email")
workflow.add_edge("process_email", "dispatch_email")
workflow.add_edge("dispatch_email", END)

# THE CRITICAL STEP: We compile the graph with a built-in pause.
# The system will stop completely before it reaches the "dispatch_email" node.
# It requires a database to hold the memory safely while pausing.
# Think of this as taking a photograph of the agent's brain before it sleeps.
memory_saver = SqliteSaver.from_conn_string("checkpoints.db")

triage_app = workflow.compile(
    checkpointer=memory_saver,
    interrupt_before=["dispatch_email"] 
)
