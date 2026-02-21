import tiktoken
from decimal import Decimal

# 1. THE PRICING TIERS
# We define the exact cost per thousand tokens based on our provider's current rates.
INPUT_COST_PER_1K = Decimal('0.005')

# 2. THE TOKEN COUNTER
# We load the exact mathematical encoding used by our chosen reasoning model.
encoding = tiktoken.encoding_for_model("<LATEST_REASONING_MODEL>")

def evaluate_transaction_cost(system_prompt: str, user_data: str) -> dict:
    print("Calculating financial projection for requested task...")

    # We combine all text the agent will read during this cycle.
    full_payload = system_prompt + user_data
    
    # 3. THE MATHEMATICAL MEASUREMENT
    # We count the exact number of tokens in the payload.
    token_count = len(encoding.encode(full_payload))
    print(f"Payload weight: {token_count} tokens.")
    
    # 4. THE FINANCIAL PROJECTION
    # We calculate the precise cost of sending this data to the provider.
    projected_cost = (Decimal(token_count) / Decimal('1000')) * INPUT_COST_PER_1K
    print(f"Projected input cost: ${projected_cost}")
    
    # 5. THE CIRCUIT BREAKER
    # We set a hard ceiling of three cents per execution.
    MAX_SAFE_COST = Decimal('0.03')
    
    if projected_cost > MAX_SAFE_COST:
        print("ALERT: Financial threshold exceeded. Blocking execution.")
        return {"status": "blocked", "cost": projected_cost}
        
    print("Transaction cost approved. Routing to intelligence engine.")
    return {"status": "approved", "cost": projected_cost}

# Simulating a massive data extraction request that causes context bloat.
# massive_document = "invoice_data " * 8000
# evaluate_transaction_cost("Extract all line items.", massive_document)
