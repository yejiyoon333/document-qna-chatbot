from io import BytesIO
from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf_file = BytesIO(file_bytes)
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_txt(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")


def extract_text_from_docx(file_bytes: bytes) -> str:
    docx_file = BytesIO(file_bytes)
    document = Document(docx_file)

    text = ""

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    return text


def extract_text_from_file(file_bytes: bytes, content_type: str, filename: str) -> str:
    filename = filename.lower()

    if content_type == "application/pdf" or filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if content_type == "text/plain" or filename.endswith(".txt"):
        return extract_text_from_txt(file_bytes)

    if (
        content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        or filename.endswith(".docx")
    ):
        return extract_text_from_docx(file_bytes)

    raise ValueError("Unsupported file type.")
