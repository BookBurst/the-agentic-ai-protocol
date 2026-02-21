from langchain_core.tools import tool

# We use a simple dictionary to track state in this example.
# In a production environment, builders use Redis or a SQL database.
processed_transactions = {}

@tool
def issue_refund(ticket_id: str, customer_id: str, amount: int) -> str:
    """
    Issues a refund to a customer. 
    Requires the ticket_id to prevent accidental double refunds.
    """
    print(f"Tool called: Attempting to refund ${amount} for ticket {ticket_id}")
    
    # 1. THE IDEMPOTENCY CHECK
    # We inspect our database to see if this exact ticket was already processed.
    if ticket_id in processed_transactions:
        print("ALERT: Duplicate request detected. Blocking execution.")
        
        # We return a positive confirmation to the agent so it stops trying.
        # We do NOT execute the actual financial API call again.
        return f"Refund for ticket {ticket_id} was already completed successfully."
    
    # 2. THE DANGEROUS EXECUTION
    # This section represents the actual call to Stripe, PayPal, or a bank API.
    print(f"Executing network call to payment gateway for {customer_id}...")
    
    # 3. STATE RECORDING
    # We record the ticket_id permanently before returning control to the agent.
    processed_transactions[ticket_id] = {
        "status": "refunded",
        "amount": amount
    }
    
    return f"Refund of ${amount} processed successfully for {ticket_id}."

# First attempt: The agent executes the tool normally.
response_one = issue_refund.invoke({"ticket_id": "TCK-992", "customer_id": "USER-44", "amount": 50})
print(f"Agent sees: {response_one}\n")

# Second attempt: The agent hallucinates or retries due to a network timeout.
response_two = issue_refund.invoke({"ticket_id": "TCK-992", "customer_id": "USER-44", "amount": 50})
print(f"Agent sees: {response_two}")
