from typing import TypedDict, Annotated, List
import operator

# We define the State Schema to act as our centralized chart.
# This prevents the agent from guessing what happened in previous steps.
class AgentState(TypedDict):
    # We use Annotated and operator.add to allow list appending.
    # This means new messages won't overwrite the old history.
    messages: Annotated[List[str], operator.add]
    # This boolean tells the system if the task is done.
    is_complete: bool
    # We store the search results in particular to avoid re-running expensive tools.
    collected_data: List[dict]

# Why we use this logic:
# By defining a strict TypedDict, we create a contract for every node.
# Every worker in our graph knows exactly where to find data and where to save it.
