from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. THE AUDIT FORM
# We force the AI auditor to return a strict JSON object.
# The boolean acts as our physical gatekeeper.
class QualityAudit(BaseModel):
    passes_guidelines: bool = Field(description="True ONLY if the draft meets all rules.")
    rejection_reason: str = Field(description="If false, explain exactly which rule failed.")

# 2. THE INSPECTOR ENGINE
# The auditor needs cold, predictable logic, so we set the temperature to absolute zero.
# We use a fast, inexpensive model because the task is narrow and evaluative.
auditor_llm = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0.0)
strict_auditor = auditor_llm.with_structured_output(QualityAudit)

def verify_and_route_draft(draft_text: str) -> dict:
    print("Auditor is scanning the draft...")

    # 3. THE RULEBOOK
    # We give the auditor a strict, unforgiving set of constraints.
    rules = """
    1. The message must be under 30 words.
    2. It must NOT contain corporate buzzwords like 'synergy' or 'robust'.
    3. It must end with a question mark.
    """
    
    prompt = [
        SystemMessage(content=f"You are a ruthless QA auditor. Follow these rules exactly:\n{rules}"),
        HumanMessage(content=f"Audit this draft:\n{draft_text}")
    ]

    # 4. THE VERIFICATION
    # The agent reads the text and grades it against the rulebook.
    result = strict_auditor.invoke(prompt)

    if result.passes_guidelines:
        print("Status: APPROVED. Routing to execution pipeline.")
        # In production, this triggers the webhook or email API.
        return {"status": "send", "content": draft_text}
    else:
        print(f"Status: REJECTED. Reason: {result.rejection_reason}")
        # The bad draft gets pushed to a database for the human manager to review later.
        return {"status": "human_review", "content": draft_text}

# Execution Test 1: A compliant draft that respects all constraints.
print("\n--- Testing Draft 1 ---")
verify_and_route_draft("Hi John, loved your recent post on scaling infrastructure. Are you free for a quick chat?")

# Execution Test 2: A non-compliant draft that breaks length and vocabulary rules.
print("\n--- Testing Draft 2 ---")
verify_and_route_draft("Greetings. We offer great synergy for your team. Let us schedule a call to discuss our robust solutions.")
