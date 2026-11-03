import requests
import chromadb
from pathlib import Path
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "chroma_db"

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_collection(
    name="supportpro_manual",
    embedding_function=embedding_function
)


def ask_question(question):
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(documents)

    prompt = f"""
You are a SupportPro support assistant.
Answer using ONLY the manual context below.
Do not invent information.
If the context does not clearly contain the answer,
reply exactly: I don't know.

Manual context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0}
        },
        timeout=120
    )

    response.raise_for_status()
    answer = response.json()["response"].strip()

    if answer == "I don't know.":
        sources = []
    else:
        sources = sorted({
            metadata["page"]
            for metadata in metadatas
            if "page" in metadata
        })

    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":
    result = ask_question(
        "How many team members does the Enterprise plan support?"
    )
    print(result)