import { useState } from "react";
import "./App.css";
import {
  uploadDocument,
  askQuestion,
  type UploadResponse,
  type AskResponse,
} from "./api";

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const [question, setQuestion] = useState("");
  const [answerResult, setAnswerResult] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleUpload() {
    if (!selectedFile) {
      setErrorMessage("Please select a document first.");
      return;
    }

    try {
      setLoading(true);
      setErrorMessage("");
      setAnswerResult(null);

      const result = await uploadDocument(selectedFile);
      setUploadResult(result);
    } catch (error) {
      if (error instanceof Error) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage("Upload failed.");
      }
    } finally {
      setLoading(false);
    }
  }

  async function handleAsk() {
    if (!question.trim()) {
      setErrorMessage("Please enter a question.");
      return;
    }

    try {
      setLoading(true);
      setErrorMessage("");

      const result = await askQuestion(question);
      setAnswerResult(result);
    } catch (error) {
      if (error instanceof Error) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage("Failed to get an answer.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-container">
      <section className="hero-section">
        <p className="eyebrow">Document Q&A Chatbot</p>
        <h1>Ask questions about your documents</h1>
        <p className="subtitle">
          Upload a PDF, TXT, or DOCX file and get answers using local retrieval
          and Gemini.
        </p>
      </section>

      <section className="card">
        <h2>1. Upload document</h2>

        <div className="upload-row">
          <input
            type="file"
            accept=".pdf,.txt,.docx"
            onChange={(event) => {
              const file = event.target.files?.[0] ?? null;
              setSelectedFile(file);
            }}
          />

          <button onClick={handleUpload} disabled={loading}>
            Upload
          </button>
        </div>

        {uploadResult && (
          <div className="result-box">
            <p>
              <strong>File:</strong> {uploadResult.filename}
            </p>
            <p>
              <strong>Chunks:</strong> {uploadResult.chunk_count}
            </p>
            <p>
              <strong>Text length:</strong> {uploadResult.text_length}
            </p>
          </div>
        )}
      </section>

      <section className="card">
        <h2>2. Ask a question</h2>

        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Example: What is this document about?"
          rows={4}
        />

        <button onClick={handleAsk} disabled={loading}>
          Ask
        </button>

        {answerResult && (
          <div className="answer-box">
            <h3>Answer</h3>
            <p>{answerResult.answer}</p>

            <h3>Sources</h3>
            {answerResult.sources.map((source, index) => (
              <div className="source-box" key={index}>
                <p>{source.preview}</p>
                <span>
                  Score: {source.score === null ? "fallback" : source.score}
                </span>
              </div>
            ))}
          </div>
        )}
      </section>

      {loading && <p className="loading">Processing...</p>}

      {errorMessage && <p className="error">{errorMessage}</p>}
    </main>
  );
}

export default App;