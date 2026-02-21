from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# 1. THE EMBEDDING ENGINE
embedder = OpenAIEmbeddings(model="<LATEST_EMBEDDING_MODEL>")

# We connect to our permanent local storage folder.
db = Chroma(persist_directory="./agent_core_memory", embedding_function=embedder)

def update_agent_memory(source_name: str, new_text: str) -> str:
    print(f"Initiating memory regeneration for target: {source_name}")

    # 2. THE PRUNING PHASE
    existing_records = db.get(where={"source": source_name})

    if existing_records["ids"]:
        outdated_count = len(existing_records['ids'])
        print(f"Found {outdated_count} outdated records. Executing deletion.")
        db.delete(ids=existing_records["ids"])
    else:
        print("No prior records found. Proceeding as fresh insertion.")

    # 3. THE REGENERATION PHASE
    new_doc = Document(
        page_content=new_text,
        metadata={"source": source_name, "status": "active"}
    )

    print("Embedding and storing the updated context...")
    db.add_documents([new_doc])
    
    return "Memory lifecycle complete."
