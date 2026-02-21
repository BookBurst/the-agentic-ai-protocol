import requests
import uuid

def execute_safe_refund(customer_charge_id: str, refund_amount: int, workflow_state_id: str):
    # The workflow_state_id is generated once per graph execution.
    # It acts as our permanent receipt number for this specific task.
    
    stripe_endpoint = "https://api.stripe.com/v1/refunds"
    
    headers = {
        "Authorization": "Bearer sk_live_your_secret_key",
        # We inject the state ID directly into the payment gateway header.
        # This single line of defense stops duplicate charges entirely.
        "Idempotency-Key": workflow_state_id
    }
    
    payload = {
        "charge": customer_charge_id,
        "amount": refund_amount
    }
    
    try:
        # The script fires the request to the external financial server.
        response = requests.post(stripe_endpoint, headers=headers, data=payload)
        
        # If the agent loops and sends the exact same Idempotency-Key,
        # Stripe ignores the duplicate action and returns the original success data.
        return response.json()
        
    except requests.exceptions.RequestException as network_error:
        # The connection dropped before the gateway could confirm the transaction.
        # The agent can safely retry this function later. The funds are locked and safe.
        print(f"Connection dropped. Funds secured by idempotency. Log: {network_error}")
        return None
