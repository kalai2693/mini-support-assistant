from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from app.chunker import split_pdf

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "chroma_db"

def create_vector_store():
    chunks = split_pdf()

    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(path=str(DB_PATH))

    collection = client.get_or_create_collection(
        name="supportpro_manual",
        embedding_function=embedding_function
    )

    collection.upsert(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=[chunk.page_content for chunk in chunks],
        metadatas=[chunk.metadata for chunk in chunks]
    )

    print("Vector store created successfully!")
    print("Total documents stored:", collection.count())

if __name__ == "__main__":
    create_vector_store()