from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

# We assign a fast, highly literal model tier for basic parsing tasks.
# Setting temperature to 0 eliminates creative guessing.
worker_llm = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0)

# We define the iron box. Notice the lack of conversational phrasing.
directive = """
ROLE: Senior Data Classifier.
MISSION: Read the incoming text and categorize the customer intent.
ALLOWED CATEGORIES: [REFUND, TECHNICAL_SUPPORT, SPAM].

NEGATIVE CONSTRAINTS:
- DO NOT output any text outside of the three allowed categories.
- DO NOT explain your reasoning.
- DO NOT add conversational pleasantries.
- If the text does not clearly fit, default to TECHNICAL_SUPPORT.
"""

# We load the directive into the machine's permanent memory block.
system_instruction = SystemMessage(content=directive)
