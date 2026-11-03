
from pathlib import Path
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIR / "documents" / "product_manual.pdf"


def load_pdf():
    reader = PdfReader(str(PDF_PATH))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append({
            "page": page_number,
            "text": text
        })

    return pages


if __name__ == "__main__":
    pages = load_pdf()

    print("Total pages:", len(pages))

    for page in pages:
        print(f"\nPage {page['page']}:")
        print(page["text"][:300])
