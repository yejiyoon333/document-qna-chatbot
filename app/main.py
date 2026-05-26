from fastapi import FastAPI, UploadFile, File
from app.pdf_loader import extract_text_from_pdf
from app.text_chunk import chunk_text

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Document Q&A Chatbot API is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_bytes = await file.read()
    extracted_text = extract_text_from_pdf(file_bytes)

    chunks = chunk_text(extracted_text)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "text_length": len(extracted_text),
        "chunk_count": len(chunks),
        "first_chunk_preview": chunks[0][:500] if chunks else "",
        "message": "PDF text extracted and chunked successfully"
    }