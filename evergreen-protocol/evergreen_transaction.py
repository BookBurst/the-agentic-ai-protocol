import tiktoken
from decimal import Decimal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. THE IDEMPOTENCY CACHE
# We store processed transaction IDs in a local set.
# In a production environment, this is a fast Redis cache.
completed_transactions = set()

# 2. THE TOKEN COUNTER
# We load the exact mathematical encoding for our reasoning model.
encoding = tiktoken.encoding_for_model("<LATEST_REASONING_MODEL>")
INPUT_COST_PER_1K = Decimal('0.005')

def execute_evergreen_transaction(transaction_id: str, prompt_text: str) -> dict:
    print(f"Initiating protocol for transaction: {transaction_id}")

    # 3. THE IDEMPOTENCY CHECK
    # We block duplicate requests immediately.
    # This acts as our elevator button, ignoring the panic presses.
    if transaction_id in completed_transactions:
        print("Idempotency lock triggered. Transaction already processed.")
        return {"status": "rejected", "reason": "duplicate_request"}

    # 4. THE FINANCIAL CIRCUIT BREAKER
    # We calculate the exact weight of the payload.
    token_count = len(encoding.encode(prompt_text))
    projected_cost = (Decimal(token_count) / Decimal('1000')) * INPUT_COST_PER_1K
    MAX_SAFE_COST = Decimal('0.03')

    if projected_cost > MAX_SAFE_COST:
        print(f"Safety block: Projected cost ${projected_cost} exceeds limit.")
        return {"status": "blocked", "reason": "financial_ceiling_exceeded"}

    # 5. THE ISOLATED EXECUTION
    # Only after passing all architectural gates does the agent act.
    safe_llm = ChatOpenAI(model="<LATEST_REASONING_MODEL>", temperature=0.0)
    messages = [
        SystemMessage(content="Process the financial record strictly as written."),
        HumanMessage(content=prompt_text)
    ]
    
    response = safe_llm.invoke(messages)
    
    # We log the transaction as permanently completed.
    completed_transactions.add(transaction_id)
    print("Execution finished and state permanently saved.")
    
    return {"status": "success", "data": response.content}

# Simulating a safe, first-time execution.
print(execute_evergreen_transaction("TXN-100", "Process client invoice for $500."))

# Simulating a dangerous retry loop where the agent hallucinates a duplicate call.
print(execute_evergreen_transaction("TXN-100", "Process client invoice for $500."))
