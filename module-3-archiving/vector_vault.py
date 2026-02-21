import chromadb
from chromadb.utils import embedding_functions

# We define the physical path on the hard drive for our data vault.
# This makes sure the data survives even if the computer turns off.
client = chromadb.PersistentClient(path="./agent_memory_vault")

# We select the embedding function to translate text into numbers.
# We use a standard provider to maintain consistency.
ef = embedding_functions.OpenAIEmbeddingFunction(api_key="your_api_key_here")

# We create or load the particular collection (the filing cabinet drawer).
collection = client.get_or_create_collection(
    name="company_policies", 
    embedding_function=ef
)

def save_to_permanent_memory(chunks: list):
    # We assign a unique ID to every chunk to avoid duplicates.
    ids = [f"id_{i}" for i in range(len(chunks))]
    
    # We lock the data into the persistent storage.
    collection.add(
        documents=chunks,
        ids=ids
    )
    print(f"Stored {len(chunks)} chunks permanently to disk.")

# After saving, the agent can search this vault next week without re-ingesting the file.
