const API_BASE_URL = "http://127.0.0.1:8000";

export type UploadResponse = {
  filename: string;
  content_type: string;
  text_length: number;
  chunk_count: number;
  first_chunk_preview: string;
  message: string;
};

export type StatusResponse = {
  document_name: string | null;
  indexed_chunk_count: number;
  is_index_ready: boolean;
};

export type SourcePreview = {
  preview: string;
  score: number | null;
};

export type AskResponse = {
  question: string;
  answer: string;
  sources: SourcePreview[];
  message: string;
};

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to upload document.");
  }

  return response.json();
}

export async function getDocumentStatus(): Promise<StatusResponse> {
  const response = await fetch(`${API_BASE_URL}/status`);

  if (!response.ok) {
    throw new Error("Failed to get document status.");
  }

  return response.json();
}

export async function askQuestion(question: string): Promise<AskResponse> {
  const response = await fetch(`${API_BASE_URL}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to ask question.");
  }

  return response.json();
}