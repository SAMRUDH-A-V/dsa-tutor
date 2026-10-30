from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# Connect to the same embedding model used during ingestion
embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Load our existing Chroma database
db = Chroma(
    persist_directory="db/chroma_db",
    embedding_function=embedding_model
)

# Student's question
query = "Give me a hint for Two Sum"

# Retrieve the 2 most relevant chunks
retriever = db.as_retriever(
    search_kwargs={"k": 2}
)

results = retriever.invoke(query)

print("\n--- Retrieved Knowledge ---")

for i, doc in enumerate(results, 1):
    print(f"\nResult {i}:")
    print(doc.page_content)