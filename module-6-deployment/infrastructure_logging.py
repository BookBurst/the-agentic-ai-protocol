import json
import time
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. THE LOGGER CONFIGURATION
# We configure the standard Python logger to output raw messages.
# We strip away the default text formatting because we will pass strict JSON.
logger = logging.getLogger("agent_infrastructure")
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# 2. THE REASONING ENGINE
# We instantiate the model, keeping the temperature low for predictable task execution.
agent_llm = ChatOpenAI(model="<LATEST_REASONING_MODEL>", temperature=0.1)

def execute_and_log_task(task_id: str, system_rules: str, user_input: str) -> str:
    # We start a timer to track execution latency.
    start_time = time.time()

    messages = [
        SystemMessage(content=system_rules),
        HumanMessage(content=user_input)
    ]

    # The model processes the input and generates a response.
    response = agent_llm.invoke(messages)

    # We calculate the exact time it took the model to think.
    execution_latency = round(time.time() - start_time, 2)

    # 3. THE STRUCTURED PAYLOAD
    # We build a comprehensive dictionary capturing the entire cognitive event.
    # This structure maps perfectly to Elasticsearch fields.
    log_payload = {
        "timestamp": time.time(),
        "event_type": "agent_execution",
        "transaction_id": task_id,
        "inputs": {
            "system_prompt": system_rules,
            "user_prompt": user_input
        },
        "outputs": {
            "raw_generation": response.content,
            "tool_calls_detected": bool(response.tool_calls)
        },
        "telemetry": {
            "latency_seconds": execution_latency,
            "model_used": "<LATEST_REASONING_MODEL>"
        }
    }

    # 4. THE EXPORT
    # We convert the dictionary to a JSON string and print it to the stream.
    # The external Logstash pipeline reads this output automatically.
    logger.info(json.dumps(log_payload))

    return response.content

# Triggering the monitored function with a sample business task.
# result = execute_and_log_task(
#     task_id="TXN-8842",
#     system_rules="Process the refund request. Maximum limit is $50.",
#     user_input="The product arrived broken. Please refund me $45."
# )
