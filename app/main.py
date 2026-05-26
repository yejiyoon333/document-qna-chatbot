from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from app.pdf_loader import extract_text_from_pdf
from app.text_chunk import chunk_text
from app.retriever import index_chunks, search_chunks, get_index_status, get_all_chunks
from app.qa_service import generate_answer

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "Document Q&A Chatbot API is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_bytes = await file.read()
    extracted_text = extract_text_from_pdf(file_bytes)

    chunks = chunk_text(extracted_text)
    index_chunks(chunks)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "text_length": len(extracted_text),
        "chunk_count": len(chunks),
        "first_chunk_preview": chunks[0][:500] if chunks else "",
        "message": "PDF text extracted, chunked, and indexed successfully"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    results = search_chunks(request.question)
    response = generate_answer(request.question, results, get_all_chunks())

    return {
        "question": request.question,
        "answer": response["answer"],
        "sources": response["sources"],
        "message": "Answer generated from retrieved document chunks"
    }

@app.get("/status")
def status():
    return get_index_status()
