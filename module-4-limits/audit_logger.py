import json
import hashlib
import time

# We simulate a secure storage destination.
# In an enterprise, this is an AWS S3 bucket with Object Lock enabled.
secure_audit_log = []

def create_immutable_record(agent_id: str, prompt: str, tool_used: str, output: str) -> dict:
    print("Generating cryptographically secure audit record...")

    # 1. THE PAYLOAD
    # We capture the exact state of the machine at the moment of execution.
    record = {
        "timestamp": time.time(),
        "agent_id": agent_id,
        "input_prompt": prompt,
        "action_taken": tool_used,
        "final_output": output
    }

    # 2. THE FINGERPRINT
    # We convert the dictionary into a string to hash it.
    record_string = json.dumps(record, sort_keys=True)

    # We generate an SHA-256 mathematical hash.
    # Changing one character in the record completely changes this output hash.
    fingerprint = hashlib.sha256(record_string.encode('utf-8')).hexdigest()

    # 3. THE SEALED ENVELOPE
    # We attach the fingerprint to the payload.
    sealed_record = {
        "data": record,
        "hash": fingerprint
    }

    # We write the record to our secure append-only list.
    secure_audit_log.append(sealed_record)
    return sealed_record

# The agent executes a high-risk financial trade.
trade_prompt = "Buy 500 shares of TSLA at market price."
trade_tool = "execute_market_buy"
trade_result = "Order filled at $180.50."

# We log the event permanently before moving to the next task.
audit_entry = create_immutable_record("TradingBot_01", trade_prompt, trade_tool, trade_result)
print(f"Audit sealed with hash: {audit_entry['hash']}")
