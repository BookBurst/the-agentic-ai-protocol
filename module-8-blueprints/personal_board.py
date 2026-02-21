from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# ==========================================
# PHASE 1: DEFINING THE BOARDROOM STATE
# ==========================================

# We structure the shared memory to hold the conflicting viewpoints separately.
class BoardroomState(TypedDict):
    core_idea: str
    optimist_review: str
    pessimist_review: str
    final_verdict: str

# We assign flagship models to these roles to guarantee deep logical reasoning.
board_member_llm = ChatOpenAI(model="latest-flagship-tier", temperature=0.8)
executive_llm = ChatOpenAI(model="latest-flagship-tier", temperature=0.1)


# ==========================================
# PHASE 2: THE POLARIZED NODES
# ==========================================

def optimist_node(state: BoardroomState):
    idea = state["core_idea"]
    
    # We force the model into a highly aggressive, growth-focused mindset.
    system_prompt = f"You are a visionary Chief Marketing Officer. Read this idea: {idea}. Explain why this will be a billion-dollar success. Focus on market expansion and user adoption. Ignore all risks."
    
    response = board_member_llm.invoke(system_prompt)
    print("Optimist: Market expansion analysis complete.")
    
    # The agent drops its hyper-positive review into its dedicated memory slot.
    return {"optimist_review": response.content}

def pessimist_node(state: BoardroomState):
    idea = state["core_idea"]
    
    # We force the model into a paranoid, risk-averse mindset.
    system_prompt = f"You are a strict Chief Risk Officer. Read this idea: {idea}. Explain why this will fail miserably. Focus on budget collapse, technical flaws, and market rejection. Ignore all upside."
    
    response = board_member_llm.invoke(system_prompt)
    print("Pessimist: Catastrophic risk analysis complete.")
    
    # The agent drops its hyper-negative review into its dedicated memory slot.
    return {"pessimist_review": response.content}


# ==========================================
# PHASE 3: THE SYNTHESIS NODE (THE REALIST)
# ==========================================

def realist_node(state: BoardroomState):
    idea = state["core_idea"]
    optimist_text = state["optimist_review"]
    pessimist_text = state["pessimist_review"]
    
    # The Realist reviews the entire chaotic desk and finds the truth in the middle.
    system_prompt = f"""
    You are the pragmatic CEO. 
    Original Idea: {idea}
    Optimist Argument: {optimist_text}
    Pessimist Argument: {pessimist_text}
    
    Write a final executive summary. Extract 3 actionable pros and 3 fatal risks. 
    Provide a final Go/No-Go decision based purely on logic.
    """
    
    response = executive_llm.invoke(system_prompt)
    print("Realist: Synthesis complete. Final verdict drafted.")
    
    return {"final_verdict": response.content}


# ==========================================
# PHASE 4: PARALLEL GRAPH ASSEMBLY
# ==========================================

workflow = StateGraph(BoardroomState)

# We seat the three personalities at the digital table.
workflow.add_node("optimist", optimist_node)
workflow.add_node("pessimist", pessimist_node)
workflow.add_node("realist", realist_node)

# We split the initial request into two parallel paths.
# Both the Optimist and the Pessimist start reading at the exact same time.
workflow.set_entry_point("optimist")
workflow.add_edge("optimist", "realist")

# We manually add a second entry point to force the parallel split.
workflow.add_edge("pessimist", "realist")

# The Realist writes the final report, and the graph shuts down entirely.
workflow.add_edge("realist", END)

boardroom_app = workflow.compile()
