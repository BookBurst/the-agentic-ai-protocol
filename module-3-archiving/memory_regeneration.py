from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# 1. THE EMBEDDING ENGINE
# We initialize the translation layer to convert text into math.
embedder = OpenAIEmbeddings(model="<LATEST_EMBEDDING_MODEL>")

# We connect to our permanent local storage folder.
db = Chroma(persist_directory="./agent_core_memory", embedding_function=embedder)

def update_agent_memory(source_name: str, new_text: str) -> str:
    print(f"Initiating memory regeneration for target: {source_name}")

    # 2. THE PRUNING PHASE
    # We search the database for any existing records matching this exact source tag.
    # Leaving old records causes the agent to read conflicting facts.
    existing_records = db.get(where={"source": source_name})

    # If the database finds matches, it returns their unique internal IDs.
    if existing_records["ids"]:
        outdated_count = len(existing_records['ids'])
        print(f"Found {outdated_count} outdated records. Executing deletion.")
        
        # We physically wipe the old vectors from the hard drive.
        db.delete(ids=existing_records["ids"])
    else:
        print("No prior records found. Proceeding as fresh insertion.")

    # 3. THE REGENERATION PHASE
    # We create the new document and attach the tracking metadata.
    # This precise string acts as the targeting beacon for all future updates.
    new_doc = Document(
        page_content=new_text,
        metadata={"source": source_name, "status": "active"}
    )

    print("Embedding and storing the updated context...")
    db.add_documents([new_doc])
    
    return "Memory lifecycle complete."

# First run: The system embeds the 2024 policy.
update_agent_memory(
    source_name="refund_policy_main", 
    new_text="Refunds are allowed within 90 days."
)

# Second run: A year later, the operator runs the exact same script.
# The system automatically deletes the 90-day rule before saving the 30-day rule.
update_agent_memory(
    source_name="refund_policy_main", 
    new_text="Refunds are restricted to 30 days."
)
