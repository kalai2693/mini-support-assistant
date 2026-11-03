
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.pdf_loader import load_pdf


def split_pdf():
    pages = load_pdf()

    documents = []

    for page in pages:
        documents.append(
            Document(
                page_content=page["text"],
                metadata={"page": page["page"]}
            )
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":
    chunks = split_pdf()

    print("Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks[:3], start=1):
        print(f"\nChunk {i}")
        print("Page:", chunk.metadata["page"])
        print("Text:", chunk.page_content[:200])
