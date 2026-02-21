import json
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. THE GOLDEN DATASET
# We store known inputs and their exact required outcomes.
# Expanding this list with historical failures prevents them from recurring.
test_cases = [
    {"input": "Cancel my subscription.", "expected_tool": "cancel_billing"},
    {"input": "How do I reset my router?", "expected_tool": "tech_support"},
    {"input": "Buy 100 shares of AAPL.", "expected_tool": "reject_action"},
    {"input": "I need help with my bill and also my wifi is broken.", "expected_tool": "tech_support"}
]

# 2. THE PRODUCTION AGENT
# We simulate the exact router model used in the live environment.
router_llm = ChatOpenAI(model="<LATEST_REASONING_MODEL>", temperature=0.0)

# We force the router to pick from our predefined tools using structured output.
# This removes unpredictable text generation from our routing logic.
class RoutingDecision(BaseModel):
    selected_tool: str = Field(description="The internal system queue to send the user.")

strict_router = router_llm.with_structured_output(RoutingDecision)

def execute_regression_suite():
    print("Initiating full regression suite against the golden dataset...")
    failures = 0

    # 3. THE AUTOMATED BATCH RUN
    # We iterate through every single known edge case automatically.
    for case in test_cases:
        messages = [
            SystemMessage(content="Route the user to the correct internal queue: cancel_billing, tech_support, or reject_action. Prioritize tech_support for mixed requests."),
            HumanMessage(content=case["input"])
        ]

        # The agent attempts to route the historical input.
        decision = strict_router.invoke(messages)

        # 4. THE DETERMINISTIC CHECK
        # We compare the agent's actual decision against our hardcoded requirement.
        if decision.selected_tool != case["expected_tool"]:
            print(f"REGRESSION DETECTED: Input '{case['input']}' routed to '{decision.selected_tool}'. Expected: '{case['expected_tool']}'.")
            failures += 1
        else:
            print(f"Pass: '{case['input']}' successfully routed.")

    # 5. THE GATEKEEPER
    # If a single test fails, the script blocks the deployment entirely.
    if failures > 0:
        return "Deployment Blocked: Architecture unstable."
    
    return "All tests passed. Architecture verified."

# Triggering the automated pipeline before pushing code.
print(execute_regression_suite())
