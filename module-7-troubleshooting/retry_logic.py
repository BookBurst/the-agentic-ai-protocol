from typing import TypedDict, Annotated
import operator

# 1. DEFINING THE STATE WITH A TRACKER
# We add a dedicated variable called 'retry_count'. 
# We use the Annotated and operator.add logic to increase the number mathematically on each pass.
class ProductionState(TypedDict):
    current_task: str
    tool_output: str
    task_success: bool
    retry_count: Annotated[int, operator.add]

# 2. BUILDING THE REFEREE NODE
# This function decides where the data goes next. It never trusts the agent.
def safety_router(state: ProductionState):
    # We pull the current number of attempts. We default to 0 on the first run.
    attempts = state.get("retry_count", 0)
    
    # Rule A: If the task worked perfectly, we exit the loop and move forward.
    if state.get("task_success") == True:
        print("Success. Moving to the next phase.")
        return "continue_workflow"
        
    # Rule B: The task failed, but the agent still has remaining attempts.
    if attempts < 3:
        print(f"Error detected. Attempt {attempts + 1} of 3. Forcing a retry.")
        
        # We route the agent back to the thinking phase to try a different approach.
        return "agent_reasoning_node"
        
    # Rule C: The agent hit the hard limit. The circuit breaker trips.
    print("CRITICAL LIMIT REACHED: Agent failed 3 times. Terminating loop to save budget.")
    
    # We route the data entirely out of the loop and trigger a human alarm.
    return "human_review_queue"
