// ─── User ───────────────────────────────────────────────
export interface User {
  id: number;
  name: string;
  email: string;
}

export interface UserCreate {
  name: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

// ─── Chatbot ────────────────────────────────────────────
export interface Chatbot {
  id: number;
  name: string;
  description: string;
  system_prompt: string;
  model_name: string;
}

export interface ChatbotCreate {
  name: string;
  description: string;
  system_prompt: string;
  model_name: string;
}

export interface ChatbotUpdate {
  name?: string;
  description?: string;
  system_prompt?: string;
  model_name?: string;
}

// ─── Document ───────────────────────────────────────────
export interface Document {
  id: number;
  file_name: string | null;
  source_type: string;
  status: string;
  created_at: string;
  source_value: string | null;
}

export interface UrlDocumentCreate {
  chatbot_id: number;
  url: string;
}

export interface UploadResponse {
  message: string;
  document_id: number;
  file_name: string;
  source_type: string;
  status: string;
}

// ─── Conversation ───────────────────────────────────────
export interface Conversation {
  id: number;
  chatbot_id: number;
  user_id: number;
  title: string | null;
  created_at: string;
  updated_at: string;
}

// ─── Message ────────────────────────────────────────────
export type MessageRole = "user" | "assistant" | "system";

export interface Message {
  id: number;
  conversation_id: number;
  role: MessageRole;
  content: string;
  citations: Citation[] | null;
  created_at: string;
}

export interface Citation {
  document_id: number;
  chunk_id: number;
  score: number;
}

// ─── Chat ───────────────────────────────────────────────
export interface ChatRequest {
  question: string;
}

export interface ChatResponse {
  conversation_id: number;
  message_id: number;
  answer: string;
  citations: Citation[];
}
