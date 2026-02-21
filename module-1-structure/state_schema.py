from typing import TypedDict, Annotated, List
import operator

# We define the State Schema to act as our centralized chart.
class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    is_complete: bool
    collected_data: List[dict]
