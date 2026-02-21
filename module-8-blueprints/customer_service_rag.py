from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.tools import create_retriever_tool
from langchain_core.messages import SystemMessage, HumanMessage

# ==========================================
# PHASE 1: KNOWLEDGE BASE SETUP
# ==========================================

# We convert raw policy text into searchable mathematical coordinates.
rules = [
    "Refunds are strictly limited to 30 days.",
    "Damaged items require photographic proof.",
    "No prorated refunds for software."
]
vector_db = InMemoryVectorStore.from_texts(rules, OpenAIEmbeddings())

# ==========================================
# PHASE 2: TOOL CREATION
# ==========================================

# We transform the database into an active search tool for the agent.
retriever = vector_db.as_retriever()
policy_tool = create_retriever_tool(
    retriever, "search_policy", "Find official rules on refunds and returns."
)

# ==========================================
# PHASE 3: AGENT CONFIGURATION
# ==========================================

# We bind the tool to a cost-effective model and set temperature to 0.
llm = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0).bind_tools([policy_tool])

# ==========================================
# PHASE 4: EXECUTION BOUNDARIES
# ==========================================

# We define strict rules to block hallucinations or unauthorized compensation.
directive = SystemMessage(content="""
ROLE: Support Specialist. MISSION: Use search_policy to resolve inquiries.
RULE 1: Always verify rules via the tool.
RULE 2: Deny requests outside defined policy limits.
""")

# ==========================================
# PHASE 5: LIVE PROCESSING
# ==========================================

# The agent processes the ticket, retrieves the 30-day rule, and denies the refund.
ticket = HumanMessage(content="My blender broke! I bought it 45 days ago. Refund now.")
print("Processing ticket...")
response = llm.invoke([directive, ticket])

print(f"Agent Action: {response.tool_calls}")
