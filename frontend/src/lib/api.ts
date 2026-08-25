import axios from "axios";
import type {
  LoginRequest,
  LoginResponse,
  User,
  UserCreate,
  Chatbot,
  ChatbotCreate,
  ChatbotUpdate,
  Document,
  UrlDocumentCreate,
  UploadResponse,
  ChatRequest,
  ChatResponse,
  Conversation,
  Message,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

// ── Auth interceptor ────────────────────────────────────
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    return Promise.reject(err);
  },
);

// ── Auth ────────────────────────────────────────────────
export async function register(data: UserCreate): Promise<User> {
  const res = await api.post("/auth/register", data);
  return res.data;
}

export async function login(data: LoginRequest): Promise<LoginResponse> {
  const res = await api.post("/auth/login", data);
  return res.data;
}

export async function getMe(): Promise<User> {
  const res = await api.get("/auth/me");
  return res.data;
}

// ── Chatbots ────────────────────────────────────────────
export async function createChatbot(data: ChatbotCreate): Promise<Chatbot> {
  const res = await api.post("/chatbots/", data);
  return res.data;
}

export async function getChatbots(): Promise<Chatbot[]> {
  const res = await api.get("/chatbots/");
  return res.data;
}

export async function getChatbot(id: number): Promise<Chatbot> {
  const res = await api.get(`/chatbots/${id}`);
  return res.data;
}

export async function updateChatbot(
  id: number,
  data: ChatbotUpdate,
): Promise<Chatbot> {
  const res = await api.put(`/chatbots/${id}`, data);
  return res.data;
}

export async function deleteChatbot(id: number): Promise<void> {
  await api.delete(`/chatbots/${id}`);
}

// ── Documents ───────────────────────────────────────────
export async function uploadDocument(
  chatbotId: number,
  file: File,
): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await api.post(`/documents/upload/${chatbotId}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function addUrlDocument(
  data: UrlDocumentCreate,
): Promise<{ message: string; document_id: number; status: string }> {
  const res = await api.post("/documents/url", data);
  return res.data;
}

export async function getDocuments(chatbotId: number): Promise<Document[]> {
  const res = await api.get(`/documents/chatbot/${chatbotId}`);
  return res.data;
}

export async function getDocument(id: number): Promise<Document> {
  const res = await api.get(`/documents/${id}`);
  return res.data;
}

export async function deleteDocument(id: number): Promise<void> {
  await api.delete(`/documents/${id}`);
}

// ── Conversations ───────────────────────────────────────
export async function createConversation(
  chatbotId: number,
  title?: string,
): Promise<Conversation> {
  const res = await api.post(`/chatbots/${chatbotId}/conversations`, {
    title,
  });
  return res.data;
}

export async function getConversations(
  chatbotId: number,
): Promise<Conversation[]> {
  const res = await api.get(`/chatbots/${chatbotId}/conversations`);
  return res.data;
}

export async function deleteConversation(id: number): Promise<void> {
  await api.delete(`/conversations/${id}`);
}

// ── Messages / Chat ─────────────────────────────────────
export async function getMessages(
  conversationId: number,
): Promise<Message[]> {
  const res = await api.get(`/conversations/${conversationId}/messages`);
  return res.data;
}

export async function sendMessage(
  conversationId: number,
  data: ChatRequest,
): Promise<ChatResponse> {
  const res = await api.post(
    `/chat/conversations/${conversationId}/messages`,
    data,
  );
  return res.data;
}

export async function sendMessageStream(
  conversationId: number,
  data: ChatRequest,
  onChunk: (chunk: string) => void,
): Promise<void> {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  
  const response = await fetch(
    `${API_URL}/chat/conversations/${conversationId}/messages/stream`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      body: JSON.stringify(data),
    },
  );

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) {
    throw new Error("Response body is not readable");
  }

  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      buffer += decoder.decode(value, { stream: true });
      
      // Parse SSE lines: "data: {...}\n\n"
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";
      
      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const payload = line.slice(6).trim();
          if (payload === "[DONE]") return;
          try {
            const parsed = JSON.parse(payload);
            if (parsed.token) {
              onChunk(parsed.token);
            }
          } catch {
            // Not valid JSON, skip
          }
        }
      }
    }
  } catch (error) {
    console.error('Streaming error:', error);
    throw error;
  }
}
