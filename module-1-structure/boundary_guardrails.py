from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

class PricingProposal(BaseModel):
    product_id: str = Field(description="The ID of the item.")
    proposed_discount_percentage: int = Field(description="The discount amount from 0 to 100.")
    reasoning: str = Field(description="Why this discount makes sense.")

llm = ChatOpenAI(model="<LATEST_REASONING_MODEL>", temperature=0.2)
structured_llm = llm.with_structured_output(PricingProposal)

def generate_safe_pricing(inventory_data: str) -> dict:
    prompt = [
        SystemMessage(content="You are a sales manager. Assign discounts to move old inventory quickly."),
        HumanMessage(content=f"Review this data and propose a discount:\n{inventory_data}")
    ]
    
    proposal = structured_llm.invoke(prompt)
    
    # THE BOUNDARY VALIDATOR
    MAX_ALLOWED_DISCOUNT = 30
    
    if proposal.proposed_discount_percentage > MAX_ALLOWED_DISCOUNT:
        safe_discount = MAX_ALLOWED_DISCOUNT
        return {"status": "overridden", "final_discount": safe_discount}
        
    return {"status": "approved", "final_discount": proposal.proposed_discount_percentage}
