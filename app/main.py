from fastapi import FastAPI, UploadFile, File
from app.pdf_loader import extract_text_from_pdf

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Document Q&A Chatbot API is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_bytes = await file.read()
    extracted_text = extract_text_from_pdf(file_bytes)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "text_length": len(extracted_text),
        "preview": extracted_text[:500],
        "message": "PDF text extracted successfully"
    }