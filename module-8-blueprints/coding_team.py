from typing import TypedDict
from langchain_openai import ChatOpenAI
from e2b_code_interpreter import Sandbox
from langgraph.graph import StateGraph, END

# ==========================================
# PHASE 1: DEFINING THE STATE & MODELS
# ==========================================

# We define the shared digital desk for our two agents.
# This structure tracks the original prompt, the code version, and the ongoing argument.
class CodingTeamState(TypedDict):
    original_request: str
    current_code: str
    reviewer_feedback: str
    execution_passed: bool

# We assign the specific intelligence tiers to the respective roles.
# The builder is cheap and creative. The reviewer is expensive and strict.
junior_coder = ChatOpenAI(model="latest-economy-tier", temperature=0.7)
senior_reviewer = ChatOpenAI(model="latest-flagship-tier", temperature=0)


# ==========================================
# PHASE 2: THE BUILDER AGENT (THE WORKER)
# ==========================================

def builder_agent(state: CodingTeamState):
    request = state["original_request"]
    past_feedback = state.get("reviewer_feedback", "")
    
    # The Builder receives the original task, plus any harsh critiques from the Architect.
    # On the first run, the 'past_feedback' variable remains completely empty.
    prompt = f"Write a Python script for: {request}. Fix these errors if they exist: {past_feedback}. Output ONLY pure code."
    
    response = junior_coder.invoke(prompt)
    
    # The Builder places its new draft onto the shared digital desk.
    print("Builder: Uploading new code draft.")
    return {"current_code": response.content}


# ==========================================
# PHASE 3: THE ARCHITECT AGENT (THE TESTER)
# ==========================================

def architect_agent(state: CodingTeamState):
    drafted_code = state["current_code"]
    
    # We open a secure, disposable environment to test the unverified logic safely.
    with Sandbox() as sandbox:
        print("Architect: Testing code in the sandbox...")
        execution_result = sandbox.run_code(drafted_code)
        
        # We check if the execution caused a fatal crash.
        if execution_result.error:
            error_message = f"CRITICAL FAILURE: {execution_result.error}"
            print(f"Architect: Code rejected. Sending feedback to Builder.")
            
            # We flag the failure and pass the exact error log back for a complete rewrite.
            return {"reviewer_feedback": error_message, "execution_passed": False}
            
    # If the sandbox survives without throwing an error, the code works perfectly.
    print("Architect: Execution successful. Code approved for production.")
    return {"reviewer_feedback": "Passed.", "execution_passed": True}


# ==========================================
# PHASE 4: CONDITIONAL ROUTING LOGIC
# ==========================================

# We define the routing rule that keeps the loop alive until perfection is reached.
def conditional_routing(state: CodingTeamState):
    if state["execution_passed"]:
        # The code passed the physical test. We break the loop and end the job.
        return "end_process"
    
    # The code failed the physical test. We force the Builder to try again.
    return "send_back_to_builder"


# ==========================================
# PHASE 5: ASSEMBLING THE CODING STUDIO
# ==========================================

# ======== ASSEMBLING THE CODING STUDIO ========

# We initialize the graph using the state schema defined in Phase 1.
workflow = StateGraph(CodingTeamState)

# We register the workers (nodes) into the environment.
workflow.add_node("builder", builder_agent)
workflow.add_node("architect", architect_agent)

# We define the fixed entry point for the request.
workflow.set_entry_point("builder")

# We draw the primary path from the developer to the reviewer.
workflow.add_edge("builder", "architect")

# We implement the conditional routing based on the sandbox test result.
# This is the "Bouncer" that prevents broken code from escaping.
workflow.add_conditional_edges(
    "architect",
    conditional_routing,
    {
        "send_back_to_builder": "builder",
        "end_process": END
    }
)

# We compile the graph into a production-ready application.
coding_studio = workflow.compile()
