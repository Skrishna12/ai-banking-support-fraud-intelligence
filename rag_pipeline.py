import os
import pandas as pd
from src.Database import engine

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# ---------------------------------------------------
# Load Policy Documents
# ---------------------------------------------------

policy_files = [
    "Dataset/fraud_handling_policy.txt",
    "Dataset/kyc_policy.txt",
    "Dataset/loan_processing_policy.txt",
    "Dataset/refund_dispute_policy.txt"
]

documents = []

for file in policy_files:
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": os.path.basename(file)
                }
            )
        )

# ---------------------------------------------------
# Load QA Pairs from MySQL
# ---------------------------------------------------

qa_df = pd.read_sql(
    "SELECT * FROM qa_pairs",
    engine
)

for _, row in qa_df.iterrows():

    qa_text = f"""
Category: {row['category']}

Question:
{row['question']}

Answer:
{row['answer']}

Policy Reference:
{row['policy_ref']}

Risk Level:
{row['risk_level']}

Suggested Action:
{row['suggested_action']}
"""

    documents.append(
        Document(
            page_content=qa_text,
            metadata={
                "source": "qa_pairs",
                "category": row["category"]
            }
        )
    )

print(f"Loaded {len(documents)} documents")

# ---------------------------------------------------
# Split Documents into Chunks
# ---------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

# ---------------------------------------------------
# Create Embeddings
# ---------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ---------------------------------------------------
# Create FAISS Vector Store
# ---------------------------------------------------

vector_store = FAISS.from_documents(
    chunks,
    embeddings
)

# Save vector database locally
vector_store.save_local("vector_db")

print("FAISS Vector Database Created Successfully")

# ---------------------------------------------------
# Retrieval Function
# ---------------------------------------------------

def retrieve_context(query, k=3):
    """
    Retrieve relevant documents from FAISS vector store.
    """

    results = vector_store.similarity_search(
        query,
        k=k
    )

    return results


# ---------------------------------------------------
# Testing Section
# ---------------------------------------------------

if __name__ == "__main__":

    query = "I found an unauthorized transaction of ₹10,000."

    results = retrieve_context(query)

    print("\nRetrieved Context:\n")

    for i, result in enumerate(results, 1):
        print(f"\nResult {i}")
        print(result.page_content)
        print("-" * 80)