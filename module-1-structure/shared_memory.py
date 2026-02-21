from typing import TypedDict, Annotated, List
import operator

# We define the shared notebook.
class AgentState(TypedDict):
    # Annotated and operator.add allow the list to grow.
    messages: Annotated[List[str], operator.add]
    is_finished: bool
