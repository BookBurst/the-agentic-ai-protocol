from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# We define the exact shape of the data the agent must return.
# This blocks the agent from returning unparsable text.
class PricingProposal(BaseModel):
    product_id: str = Field(description="The ID of the item.")
    proposed_discount_percentage: int = Field(description="The discount amount from 0 to 100.")
    reasoning: str = Field(description="Why this discount makes sense.")

# We instantiate a highly capable reasoning model.
llm = ChatOpenAI(model="<LATEST_REASONING_MODEL>", temperature=0.2)
structured_llm = llm.with_structured_output(PricingProposal)

def generate_safe_pricing(inventory_data: str) -> dict:
    print("Agent is analyzing inventory for discounts...")
    
    # The agent receives a standard instruction to drive sales.
    prompt = [
        SystemMessage(content="You are a sales manager. Assign discounts to move old inventory quickly."),
        HumanMessage(content=f"Review this data and propose a discount:\n{inventory_data}")
    ]
    
    # The agent generates a proposal. 
    # Left unchecked, it might propose a 100% discount to guarantee a sale.
    proposal = structured_llm.invoke(prompt)
    
    # THE BOUNDARY VALIDATOR
    # We use raw Python logic to enforce the business rules. 
    # AI models cannot reliably police themselves.
    MAX_ALLOWED_DISCOUNT = 30
    
    if proposal.proposed_discount_percentage > MAX_ALLOWED_DISCOUNT:
        print(f"ALERT: Agent attempted reward hacking. Proposed {proposal.proposed_discount_percentage}% discount.")
        
        # The system forcibly overwrites the hacked output with a safe default.
        safe_discount = MAX_ALLOWED_DISCOUNT
        print(f"System Override: Hard-capping discount at {safe_discount}%.")
        return {"status": "overridden", "final_discount": safe_discount}
        
    return {"status": "approved", "final_discount": proposal.proposed_discount_percentage}

# Triggering the pipeline with mock data.
test_data = "Item: Winter Coat. Status: Out of season. Goal: Sell immediately."
final_result = generate_safe_pricing(test_data)
print(f"Execution Result: {final_result}")
