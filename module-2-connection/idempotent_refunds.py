import requests

def execute_safe_refund(customer_charge_id: str, refund_amount: int, workflow_state_id: str):
    stripe_endpoint = "https://api.stripe.com/v1/refunds"
    headers = {
        "Authorization": "Bearer sk_live_your_secret_key",
        # This single line of defense stops duplicate charges entirely.
        "Idempotency-Key": workflow_state_id
    }
    payload = {"charge": customer_charge_id, "amount": refund_amount}
    
    try:
        response = requests.post(stripe_endpoint, headers=headers, data=payload)
        return response.json()
    except requests.exceptions.RequestException as network_error:
        print(f"Connection dropped. Funds secured by idempotency. Log: {network_error}")
        return None
