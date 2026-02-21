import operator
from typing import TypedDict, Annotated, List
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

# 1. DEFINING THE RIGID CLIPBOARD (THE STATE)
# Every variable here must be strictly defined. The Annotated logic tells
# the graph to add new items to the existing list rather than overwriting it.
class ResearchState(TypedDict):
    topic: str
    search_queries: List[str]
    raw_content: Annotated[List[str], operator.add]
    final_report: str

# 2. CONFIGURING THE TOOLS AND MODELS
# We initialize our search tool to pull exactly 3 results per query to control API costs.
search_tool = TavilySearchResults(max_results=3)

# EVERGREEN STRATEGY: We assign the cheapest, fastest model tier available.
# We never waste flagship reasoning tokens on simple list generation.
planner_llm = ChatOpenAI(model="latest-economy-tier-model", temperature=0)

# 3. BUILDING THE PLANNER NODE
def planner_node(state: ResearchState):
    current_topic = state["topic"]
    
    # We instruct the model to act as a strict search strategist.
    system_prompt = f"Break down '{current_topic}' into 3 Google queries. Return ONLY commas."
    response = planner_llm.invoke(system_prompt)
    
    # We clean the text and split it into a proper Python list.
    query_list = [q.strip() for q in response.content.split(",")]
    
    print(f"Generated Queries: {query_list}")
    return {"search_queries": query_list}

# 4. BUILDING THE SEARCH NODE
def search_node(state: ResearchState):
    queries = state["search_queries"]
    gathered_text = []
    
    # The node loops through each query created by the planner.
    for query in queries:
        print(f"Executing search for: {query}")
        results = search_tool.invoke({"query": query})
        
        # We extract just the clean page content from the search results.
        for result in results:
            gathered_text.append(result["content"])
            
    # We add all the scraped text blocks to the global clipboard.
    return {"raw_content": gathered_text}


# 5. BUILDING THE SYNTHESIZER NODE
def synthesizer_node(state: ResearchState):
    print("--- SYNTHESIZER: Creating Executive Summary ---")
    # We pull the massive list of raw text from the shared clipboard.
    all_content = " ".join(state["raw_content"])
    
    # We use a system prompt that forces the LLM to be brutal and concise.
    # The goal is a signal-to-noise ratio that favors facts over adjectives.
    prompt = f"Synthesize this research into a 3-page executive report: {all_content[:15000]}"
    
    # We invoke the model to generate the structured briefing.
    report = planner_llm.invoke(prompt)
    
    # We write the final string into the 'final_report' key for the next node.
    return {"final_report": report.content}

# 6. BUILDING THE DELIVERY NODE (THE KILL SWITCH/SENDER)
def delivery_node(state: ResearchState):
    print("--- DELIVERY: Firing to Slack ---")
    report_to_send = state["final_report"]
    
    # This node functions as a bridge to the external world.
    # In a production environment, we would trigger the Slack API or PDF converter here.
    # For the skeleton, we print the success status to verify the chain.
    print(f"REPORT READY FOR SLACK: {report_to_send[:100]}...")
    
    return {"final_report": report_to_send}

from langgraph.graph import StateGraph, END

# ======== ASSEMBLING THE COMPLETE FACTORY LINE ========

# We initialize the blank graph using our strict clipboard rules.
workflow = StateGraph(ResearchState)

# We register every specialized worker into the central system.
workflow.add_node("planner", planner_node)
workflow.add_node("searcher", search_node)
workflow.add_node("synthesizer", synthesizer_node)
workflow.add_node("delivery", delivery_node)

# We draw the rigid arrows connecting the workers in a fixed sequence.
# This prevents the AI from skipping steps or hallucinating its own path.
workflow.set_entry_point("planner")
workflow.add_edge("planner", "searcher")
workflow.add_edge("searcher", "synthesizer")
workflow.add_edge("synthesizer", "delivery")
workflow.add_edge("delivery", END)

# We compile the graph into an executable application ready for the VPS.
research_app = workflow.compile()
