from langchain_core.tools import tool

processed_transactions = {}

@tool
def issue_refund(ticket_id: str, customer_id: str, amount: int) -> str:
    """
    Issues a refund to a customer. 
    Requires the ticket_id to prevent accidental double refunds.
    """
    # 1. THE IDEMPOTENCY CHECK
    if ticket_id in processed_transactions:
        return f"Refund for ticket {ticket_id} was already completed successfully."
    
    # 2. STATE RECORDING (Executed before or during the actual call)
    processed_transactions[ticket_id] = {"status": "refunded", "amount": amount}
    return f"Refund of ${amount} processed successfully for {ticket_id}."
