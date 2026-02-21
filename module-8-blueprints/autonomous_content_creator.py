from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END

# ==========================================
# PHASE 1: DEFINING THE NEWSROOM STATE
# ==========================================

# 1. STATE: The shared clipboard for the newsroom.
class ContentState(TypedDict):
    topic: str
    facts: str
    post: str

# ==========================================
# PHASE 2: THE RESEARCHER NODE
# ==========================================

# 2. RESEARCHER: Extracts data using a fast, literal model.
def researcher_node(state: ContentState):
    # We use a cost-effective, deterministic model for factual accuracy.
    llm = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0)
    res = llm.invoke([
        SystemMessage(content="You are a factual researcher."),
        HumanMessage(content=f"Find facts about: {state['topic']}")
    ])
    print("Researcher: Facts gathered successfully.")
    return {"facts": res.content}

# ==========================================
# PHASE 3: THE WRITER NODE
# ==========================================

# 3. WRITER: Crafts the narrative using a creative model.
def writer_node(state: ContentState):
    # We switch to a high-tier creative model to handle the storytelling and tone.
    llm = ChatOpenAI(model="<LATEST_REASONING_MODEL>", temperature=0.7)
    res = llm.invoke([
        SystemMessage(content="You are a bold tech copywriter."),
        HumanMessage(content=f"Write a post from these facts:\n{state['facts']}")
    ])
    print("Writer: Content draft completed.")
    return {"post": res.content}

# ==========================================
# PHASE 4: ASSEMBLY & EXECUTION
# ==========================================

# 4. GRAPH: Wiring the autonomous assembly line.
builder = StateGraph(ContentState)

# We add the specialized workstations.
builder.add_node("research", researcher_node)
builder.add_node("write", writer_node)

# We define the fixed production sequence.
builder.set_entry_point("research")
builder.add_edge("research", "write")
builder.add_edge("write", END)

# We compile the graph into an executable worker.
app = builder.compile()

# 5. EXECUTION: One idea triggers the whole chain.
# task = {"topic": "Agentic AI in logistics"}
# final_content = app.invoke(task)
# print(f"--- FINAL POST ---\n{final_content['post']}")
