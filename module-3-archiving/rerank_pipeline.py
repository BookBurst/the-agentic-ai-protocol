from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# 1. THE FRANTIC CLERK (Base Retriever)
# We assume a Chroma database is already loaded with our documents.
# We instruct the base retriever to cast a wide net and grab 20 documents.
# Grabbing 20 docs ensures we do not miss the correct answer, but it creates massive noise.
base_retriever = database.as_retriever(search_kwargs={"k": 20})

# 2. THE SENIOR CHEF (Cross-Encoder Model)
# We initialize a specialized local model designed specifically for scoring relevance.
# This model does not generate text; it only reads and grades from 0.0 to 1.0.
scoring_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")

# 3. THE COMPRESSOR
# We tell the compressor to use the scoring model and keep ONLY the top 3 highest-scoring documents.
document_compressor = CrossEncoderReranker(model=scoring_model, top_n=3)

# 4. THE TWO-STAGE PIPELINE
# We wrap the base retriever inside the compressor.
# The agent will only interact with this final object.
re_ranking_retriever = ContextualCompressionRetriever(
    base_compressor=document_compressor,
    base_retriever=base_retriever
)

def retrieve_clean_context(user_query: str) -> list[Document]:
    print("Executing Stage 1: Fast Vector Search (Top 20)...")
    print("Executing Stage 2: Cross-Encoder Re-Ranking (Filtering to Top 3)...")
    
    # The agent calls the pipeline. 
    # The pipeline handles the two-stage logic automatically in the background.
    clean_documents = re_ranking_retriever.invoke(user_query)
    
    return clean_documents

# The agent requests highly specific data.
final_docs = retrieve_clean_context("What is the policy for a laptop battery fire?")
print(f"Clean Context Retrieved: {len(final_docs)} documents.")
