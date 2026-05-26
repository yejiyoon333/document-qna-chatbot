from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Document Q&A Chatbot API is running"}
