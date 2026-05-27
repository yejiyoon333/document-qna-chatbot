from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.document_loader import extract_text_from_file
from app.text_chunk import chunk_text
from app.retriever import index_chunks, search_chunks, get_index_status, get_all_chunks
from app.qa_service import build_context_sources, build_display_sources
from app.llm_service import generate_llm_answer

# http://127.0.0.1:8000
# http://localhost:5173

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "Document Q&A Chatbot API is running"}


@app.get("/status")
def status():
    return get_index_status()


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_bytes = await file.read()

    try:
        extracted_text = extract_text_from_file(
            file_bytes=file_bytes,
            content_type=file.content_type,
            filename=file.filename
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, TXT, and DOCX files are supported."
        )

    if not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No text could be extracted from the uploaded file."
        )

    chunks = chunk_text(extracted_text)
    index_chunks(chunks, file.filename)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "text_length": len(extracted_text),
        "chunk_count": len(chunks),
        "first_chunk_preview": chunks[0][:500] if chunks else "",
        "message": "Document text extracted, chunked, and indexed successfully"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    status = get_index_status()

    if not status["is_index_ready"]:
        raise HTTPException(
            status_code=400,
            detail="Please upload a document before asking questions."
        )

    retrieved_chunks = search_chunks(request.question)
    context_sources = build_context_sources(retrieved_chunks, get_all_chunks())
    display_sources = build_display_sources(context_sources)

    answer = generate_llm_answer(request.question, context_sources)

    return {
        "question": request.question,
        "answer": answer,
        "sources": display_sources,
        "message": "Answer generated with Gemini API"
    }
