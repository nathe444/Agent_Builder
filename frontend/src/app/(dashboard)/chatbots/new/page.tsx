"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useCreateChatbot } from "@/hooks/use-chatbots";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";

const MODELS = [
  { value: "gpt-4o", label: "GPT-4o" },
  { value: "gpt-4o-mini", label: "GPT-4o Mini" },
  { value: "gpt-3.5-turbo", label: "GPT-3.5 Turbo" },
  { value: "claude-3-sonnet", label: "Claude 3 Sonnet" },
  { value: "claude-3-haiku", label: "Claude 3 Haiku" },
  { value: "llama-3.1-70b", label: "Llama 3.1 70B" },
];

export default function NewChatbotPage() {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [systemPrompt, setSystemPrompt] = useState("");
  const [modelName, setModelName] = useState("gpt-4o-mini");
  const createChatbot = useCreateChatbot();
  const router = useRouter();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    createChatbot.mutate(
      { name, description, system_prompt: systemPrompt, model_name: modelName },
      { onSuccess: (chatbot) => router.push(`/chatbots/${chatbot.id}`) },
    );
  }

  return (
    <div className="mx-auto max-w-lg animate-fade-in">
      <Link href="/chatbots" className="inline-flex items-center gap-1 text-sm text-muted hover:text-foreground mb-6">
        <ArrowLeft className="h-3.5 w-3.5" />
        Back
      </Link>

      <h1 className="text-lg font-semibold tracking-tight">New chatbot</h1>
      <p className="mt-1 text-sm text-muted">Configure how your chatbot behaves.</p>

      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <div className="space-y-1.5">
          <label className="text-sm font-medium text-foreground">Name</label>
          <input
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full rounded-lg border border-border bg-card px-3 py-2 text-sm placeholder:text-muted-light"
            placeholder="e.g. Support Assistant"
          />
        </div>

        <div className="space-y-1.5">
          <label className="text-sm font-medium text-foreground">Description</label>
          <textarea
            required
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={2}
            className="w-full rounded-lg border border-border bg-card px-3 py-2 text-sm resize-none placeholder:text-muted-light"
            placeholder="What this chatbot does"
          />
        </div>

        <div className="space-y-1.5">
          <label className="text-sm font-medium text-foreground">System prompt</label>
          <textarea
            required
            value={systemPrompt}
            onChange={(e) => setSystemPrompt(e.target.value)}
            rows={5}
            className="w-full rounded-lg border border-border bg-card px-3 py-2 font-mono text-xs resize-none placeholder:text-muted-light"
            placeholder="You are a helpful assistant..."
          />
        </div>

        <div className="space-y-1.5">
          <label className="text-sm font-medium text-foreground">Model</label>
          <select
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
            className="w-full rounded-lg border border-border bg-card px-3 py-2 text-sm"
          >
            {MODELS.map((m) => (
              <option key={m.value} value={m.value}>{m.label}</option>
            ))}
          </select>
        </div>

        {createChatbot.isError && (
          <div className="rounded-lg border border-danger/20 bg-danger-light px-3 py-2 text-sm text-danger">
            {(createChatbot.error as any)?.response?.data?.detail || "Failed to create chatbot"}
          </div>
        )}

        <button
          type="submit"
          disabled={createChatbot.isPending}
          className="w-full rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-hover disabled:opacity-50"
        >
          {createChatbot.isPending ? "Creating..." : "Create chatbot"}
        </button>
      </form>
    </div>
  );
}
