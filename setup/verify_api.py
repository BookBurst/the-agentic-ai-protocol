import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# 1. UNLOCKING THE VAULT
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("The API vault is empty. Check the .env file.")

# 2. BUILDING THE BOUNCER
class TestResponse(BaseModel):
    system_status: str = Field(description="Reply with exactly 'ALL SYSTEMS GREEN'")
    confidence_score: int = Field(description="A number between 1 and 100")

# 3. WAKING UP THE MODEL
# Utilizziamo un modello veloce ed economico per il test
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(TestResponse)

# 4. EXECUTING THE TEST
print("Pinging the intelligence provider...")
response = structured_llm.invoke("Run a quick system diagnostic.")
print(f"Status: {response.system_status}")
print(f"Confidence: {response.confidence_score}%")
print("The workshop is ready.")
