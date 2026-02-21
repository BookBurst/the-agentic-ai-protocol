from pydantic import BaseModel, Field
from langchain_core.tools import tool

# 1. DEFINING THE RIGID CONTRACT
# We tell the model the exact shape of the data required.
# The descriptions act as micro-prompts to guide the agent's formatting.
class BillingInput(BaseModel):
    customer_id: int = Field(description="The numeric ID. Never use letters or symbols.")
    amount: float = Field(description="The billing amount in USD formatted as a decimal.")

# 2. BUILDING THE RESILIENT TOOL
# We attach the strict contract directly to the tool function using args_schema.
@tool("update_billing", args_schema=BillingInput)
def update_billing_tool(customer_id: int, amount: float) -> str:
    """Updates the billing system. Only call this when ready to charge the client."""
    
    # 3. THE SAFETY CATCH
    # We use a try/except block to prevent the Python script from dying upon failure.
    try:
        # Simulated database logic goes here.
        print(f"System: Charging customer {customer_id} the amount of ${amount}")
        
        # We return a clear success message so the agent knows the job is done.
        return "SUCCESS: The billing system updated correctly."
        
    except Exception as e:
        # We catch the crash and return the exact error message back to the agent's brain.
        # The agent reads this string, understands its mistake, and tries again.
        return f"FAILURE: The database rejected the input. Error details: {str(e)}"
