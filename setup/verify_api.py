import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# 1. LOAD CONFIGURATION
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("API Key missing. Check your .env file.")

# 2. DEFINE STRUCTURED OUTPUT
class SystemCheck(BaseModel):
    status: str = Field(description="Must be 'SYSTEM_OPERATIONAL'")
    latency_score: int = Field(description="A simulated value between 1 and 100")

# 3. INITIALIZE MODEL
# Using a cost-effective model for the initial handshake
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(SystemCheck)

# 4. EXECUTION
print("Testing connection to intelligence provider...")
response = structured_llm.invoke("Perform a system handshake.")
print(f"Connection Status: {response.status}")
print(f"Latency Score: {response.latency_score}")
print("API verification complete.")
