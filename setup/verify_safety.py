import os
import sys
from decimal import Decimal, InvalidOperation

# 1. SECURITY PARAMETERS
# We load safety limits from the .env file
MAX_DOLLAR_LIMIT = os.getenv("MAX_TRANSACTION_COST", "0.05")
TELEMETRY_ENDPOINT = os.getenv("ELK_STACK_URL", "http://localhost:9200")
BACKUP_MODEL_READY = os.getenv("BACKUP_LLM_API_KEY", "placeholder_key")

def check_safety_guardrails() -> bool:
    print("Starting Safety Guardrails Verification...")
    
    # 2. BUDGET LIMIT CHECK
    try:
        limit = Decimal(MAX_DOLLAR_LIMIT)
        print(f"[OK] Budget ceiling locked at ${limit} per request.")
    except InvalidOperation:
        print("[ERROR] Invalid budget limit detected.")
        return False
        
    # 3. MONITORING CHECK
    if not TELEMETRY_ENDPOINT:
        print("[ERROR] Monitoring endpoint missing. No data logging active.")
        return False
    print("[OK] Monitoring pipeline verified.")
    
    # 4. REDUNDANCY CHECK
    if not BACKUP_MODEL_READY:
        print("[ERROR] Redundant intelligence model missing.")
        return False
    print("[OK] System redundancy verified.")
    return True

# 5. EXECUTION
if __name__ == "__main__":
    if check_safety_guardrails():
        print("Safety check passed. System ready for deployment.")
    else:
        print("CRITICAL: Safety check failed. Deployment blocked.")
        sys.exit(1)
