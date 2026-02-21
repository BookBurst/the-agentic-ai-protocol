from typing import TypedDict, Annotated, List
import operator

# We define the shared notebook.
# This keeps the agent from losing context between steps.
class AgentState(TypedDict):
    # Annotated and operator.add allow the list to grow.
    # New messages append to the list instead of overwriting the previous one.
    messages: Annotated[List[str], operator.add]
    is_finished: bool
