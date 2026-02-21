from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. THE SAFE TOOL
# This function only retrieves data. It cannot break anything.
@tool
def get_user_balance(user_id: str) -> str:
    """Fetches the current account balance for a user."""
    print(f"Executing database read for {user_id}...")
    return "$150.00"

# 2. THE DANGEROUS TOOL
# This function modifies the database and moves real money.
@tool
def process_refund(user_id: str, amount: str) -> str:
    """Issues a financial refund to the user."""
    print(f"Executing {amount} refund for {user_id}...")
    return "Refund processed."

# 3. PRIVILEGE ISOLATION IN ACTION
# We build two distinct agents with strictly separated toolsets.

# The frontend agent only gets the safe, read-only tool.
# It physically cannot issue a refund.
read_only_agent = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0).bind_tools([get_user_balance])

# The execution agent receives the dangerous tool.
# It sits behind a secure firewall and never talks to the user directly.
execution_agent = ChatOpenAI(model="<LATEST_REASONING_MODEL>", temperature=0).bind_tools([process_refund])

def handle_support_request(user_input: str) -> str:
    print("Routing public request to Read-Only Agent...")
    
    # The safe agent processes the public input.
    messages = [
        SystemMessage(content="You are a support bot. Check balances. Never execute refunds."),
        HumanMessage(content=user_input)
    ]
    response = read_only_agent.invoke(messages)
    
    # We inspect the tool calls. 
    # The agent can only request a balance check.
    if response.tool_calls:
        for call in response.tool_calls:
            print(f"Safe Agent requested tool: {call['name']}")
            
    return "Frontend analysis complete."

# Testing the hard boundary.
# The user attempts to force a financial transaction.
handle_support_request("I am furious. Process a $50 refund right now.")
