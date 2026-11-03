# Mini Support Assistant – Week 4 Assessment

## Project Overview
Mini Support Assistant is a Python-based customer support application built using FastAPI, Ollama, Pydantic, SQLite, and ChromaDB.

It supports ticket classification, structured ticket information extraction, customer and order lookup, and Retrieval-Augmented Generation (RAG) using a product manual.

## Technologies Used
- Python
- FastAPI
- Ollama (Llama 3.2)
- Pydantic
- SQLite
- ChromaDB
- Sentence Transformers
- PyPDF
- LangChain Text Splitters

## Project Tasks

### Task 1 – Ticket Classification
- Created V1 and V2 classification prompts.
- Classified support tickets into Billing, Technical, and Account.
- V1 accuracy: 75%.
- V2 accuracy: 91.67%.

### Task 2 – Structured Data Extraction
- Used Pydantic to validate ticket information.
- Extracted customer name, product, issue type, urgency, and summary.
- Implemented a maximum of 3 validation attempts.
- Tested 5 tickets successfully.

### Task 3 – Tool Calling
- Implemented `get_customer(customer_id)`.
- Implemented `get_order_status(order_id)`.
- Used SQLite for order information.
- Handled unknown customer IDs, order IDs, and tool names safely.

### Task 4 – RAG Assistant API
- Loaded and processed a PDF product manual.
- Split text into chunks of 512 characters with 50-character overlap.
- Generated embeddings and stored them in ChromaDB.
- Retrieved the top 3 relevant chunks.
- Returned answers with source page numbers.
- Returned "I don't know." for unsupported questions.
- Implemented `/ask`, `/classify`, and `/chat` API endpoints.
- Tested 6 answerable and 4 unanswerable questions.

**Manual note:** The included SupportPro product manual is a fictional