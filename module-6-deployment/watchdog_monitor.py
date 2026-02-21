import time
import requests
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. THE WATCHDOG LIMITS
# We define the absolute maximum number of times the agent can retry a task.
MAXIMUM_ALLOWED_LOOPS = 3
ALARM_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# 2. THE INTELLIGENCE ENGINE
agent_llm = ChatOpenAI(model="<LATEST_REASONING_MODEL>", temperature=0.1)

def trigger_critical_alarm(reason: str, loop_count: int) -> None:
    print("WATCHDOG TRIGGERED: Broadcasting emergency alarm...")
    
    # We format a payload to send to our communication channel.
    alert_payload = {
        "text": f"CRITICAL AGENT FAILURE: {reason}. Halted at loop {loop_count}."
    }
    
    # We push the alert over the network to wake up the operator.
    try:
        requests.post(ALARM_WEBHOOK_URL, json=alert_payload, timeout=5)
    except requests.exceptions.RequestException:
        print("Failed to reach alarm webhook. Resorting to local system halt.")

def execute_monitored_task(user_request: str) -> str:
    current_loop = 0
    task_resolved = False
    
    # 3. THE PROTECTED LOOP
    while not task_resolved:
        current_loop += 1
        print(f"Starting execution cycle {current_loop}...")
        
        # 4. THE DEAD MAN'S SWITCH
        if current_loop > MAXIMUM_ALLOWED_LOOPS:
            trigger_critical_alarm("Infinite loop detected", current_loop)
            return "System halted. Operator notified."
            
        messages = [
            SystemMessage(content="Solve the user query. Reply 'DONE' when finished."),
            HumanMessage(content=user_request)
        ]
        
        # The agent attempts to generate a solution.
        response = agent_llm.invoke(messages)
        
        # We check if the agent successfully completed the mandate.
        if "DONE" in response.content:
            task_resolved = True
            print("Task completed successfully.")
        else:
            print("Task incomplete. Agent requires another iteration.")
            time.sleep(1)
            
    return "Execution finished perfectly."
