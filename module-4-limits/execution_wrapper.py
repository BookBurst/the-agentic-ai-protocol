import time

def safe_execution_wrapper(agent_function, max_attempts=3):
    # We start a strict counter outside the agent's control.
    attempt_tracker = 0
    
    while attempt_tracker < max_attempts:
        try:
            # The script tries to run the primary task.
            result = agent_function()
            return result
            
        except Exception as system_error:
            attempt_tracker += 1
            print(f"Task failed. Attempt {attempt_tracker} of {max_attempts}. Log: {system_error}")
            
            # We force a brief pause to prevent rate-limit penalties.
            time.sleep(2)
            
    # The counter hits the limit. We kill the loop permanently.
    print("Circuit breaker triggered. Task terminated to protect the budget.")
    return None
