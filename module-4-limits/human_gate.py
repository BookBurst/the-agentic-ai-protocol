import time

def process_high_stakes_action(client_name: str, drafted_email: str):
    # The agent prepares the work but cannot execute it directly.
    print(f"--- HUMAN APPROVAL REQUIRED ---")
    print(f"Target: {client_name}")
    print(f"Proposed Action: Send the following email:\n'{drafted_email}'")
    
    # We simulate a pause in the system waiting for an external trigger.
    # In a real production environment, this would be a webhook waiting for a Slack button press.
    human_decision = input("Type 'APPROVE' to send or 'REJECT' to discard: ")
    
    if human_decision.strip().upper() == "APPROVE":
        # The human accepts the risk. The agent proceeds with the write operation.
        print("Authorization granted. Executing the API call now.")
        # Insert actual email sending logic here.
        return True
        
    elif human_decision.strip().upper() == "REJECT":
        # The human spots an error. The system drops the task safely.
        print("Authorization denied. Task discarded.")
        return False
        
    else:
        # We handle typos in the approval process by defaulting to a safe rejection.
        print("Unrecognized command. Defaulting to safe rejection.")
        return False

# We test the gate with a potentially dangerous automated response.
bad_ai_draft = "Your account has been cancelled as requested. Goodbye."
process_high_stakes_action("VIP Corp", bad_ai_draft)
