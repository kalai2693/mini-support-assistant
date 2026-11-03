from fastapi import FastAPI
from pydantic import BaseModel

from app.rag_assistant import ask_question
from app.classifier import classify_ticket
from app.tool_assistant import ask_assistant

app = FastAPI(title="Mini Support Assistant")


class AskRequest(BaseModel):
    question: str


class ClassifyRequest(BaseModel):
    ticket: str


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Mini Support Assistant is running"}


@app.post("/ask")
def ask(request: AskRequest):
    return ask_question(request.question)


@app.post("/classify")
def classify(request: ClassifyRequest):
    result = classify_ticket(request.ticket, "v2")
    return {"category": result}


@app.post("/chat")
def chat(request: ChatRequest):
    tool_results = ask_assistant(request.message)

    if tool_results:
        return {
            "type": "tool",
            "results": tool_results
        }

    rag_result = ask_question(request.message)

    return {
        "type": "rag",
        "answer": rag_result["answer"],
        "sources": rag_result["sources"]
    }