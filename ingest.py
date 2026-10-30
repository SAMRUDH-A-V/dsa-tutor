from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


# 1. Load DSA knowledge
loader = DirectoryLoader(
    "docs",
    glob="*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)

documents = loader.load()

print(f"Loaded {len(documents)} documents")


# 2. Split documents into smaller chunks
text_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    source = chunk.metadata.get("source", "")
    chunk.metadata["topic"] = source.split("\\")[-1].replace(".txt", "")

print(f"Created {len(chunks)} chunks")


# 3. Create embeddings using Ollama
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)


# 4. Store embeddings in ChromaDB
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="db/chroma_db"
)

print("✅ DSA knowledge stored in ChromaDB")