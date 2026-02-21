# We import TypedDict to define the exact shape of our memory.
from typing import TypedDict, Annotated
# We import operator to help us update the memory safely.
import operator

# This class defines the "Suitcase" our agent carries between tasks.
class AgentState(TypedDict):
    # We store the original instruction from the user.
    user_goal: str
    
    # We track the code the AI generates. 
    current_code: str
    
    # We keep track of how many times the AI has tried to fix a bug.
    # We want to avoid infinite loops that drain our API budget.
    retry_count: int
    
    # We track any error messages returned by our tools.
    error_message: str
    
    # We use a boolean (True/False) to mark the job as finished.
    is_successful: bool

def check_execution_status(state: AgentState) -> str:
    # This acts as our Conditional Edge (The Tollbooth).
    # We check the Suitcase to see if the previous task succeeded.
    
    if state["is_successful"]:
        # The code worked. We route the flow to the end of the program.
        return "end_process"
        
    elif state["retry_count"] >= 3:
        # The AI failed three times. We stop to protect our wallet.
        print("Max retries hit. Stopping execution.")
        return "end_process"
        
    else:
        # The code failed, but we still have retries left.
        # We route the flow backward to try again.
        return "retry_task"
