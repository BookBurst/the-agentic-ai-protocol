from langgraph.graph import StateGraph, END

# 1. Initialize the graph with our state definition.
builder = StateGraph(AgentState)

# 2. Add our workstations to the graph.
builder.add_node("researcher", researcher_node)

# 3. Define where the work starts and where it ends.
builder.set_entry_point("researcher")
builder.add_edge("researcher", END)

# 4. Compile the logic into an executable application.
agent_app = builder.compile()

# Testing the execution with a raw query.
test_input = {
    "messages": ["Analyze the benefits of idempotent API design."],
    "is_finished": False
}

for output in agent_app.stream(test_input):
    print(output)
