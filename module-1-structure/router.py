from typing import Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# 1. ARCHITECTURAL BLUEPRINT: THE ROUTING LOGIC
# This defines exactly where the task can be sent.
class Route(BaseModel):
    """Route the user's request to the most appropriate department."""
    destination: Literal["research", "execution", "quality_control"] = Field(
        description="The department responsible for the task."
    )
    priority: int = Field(description="Priority level from 1 to 5")

# 2. INITIALIZE THE DECISION ENGINE
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_router = llm.with_structured_output(Route)

# 3. ROUTING FUNCTION
def classify_task(user_input: str):
    print(f"Analyzing task: {user_input}")
    decision = structured_router.invoke(user_input)
    print(f"Routing to: {decision.destination.upper()} [Priority: {decision.priority}]")
    return decision

# 4. HANDSHAKE TEST
if __name__ == "__main__":
    # Example task
    classify_task("I need a detailed report on the competitors' pricing strategy.")
