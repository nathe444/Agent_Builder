"use client";

import { use } from "react";
import Link from "next/link";
import { useChatbot, useUpdateChatbot, useDeleteChatbot } from "@/hooks/use-chatbots";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, FileText, MessageSquare, Save, Pencil } from "lucide-react";

const MODELS = [
  { value: "gpt-4o", label: "GPT-4o" },
  { value: "gpt-4o-mini", label: "GPT-4o Mini" },
  { value: "gpt-3.5-turbo", label: "GPT-3.5 Turbo" },
  { value: "claude-3-sonnet", label: "Claude 3 Sonnet" },
  { value: "claude-3-haiku", label: "Claude 3 Haiku" },
  { value: "llama-3.1-70b", label: "Llama 3.1 70B" },
];

export default function ChatbotDetailPage({
  params,
}: {
  params: Promise<{ chatbotId: string }>;
}) {
  const { chatbotId } = use(params);
  const id = Number(chatbotId);
  const chatbot = useChatbot(id);
  const updateChatbot = useUpdateChatbot();
  const deleteChatbot = useDeleteChatbot();
  const router = useRouter();

  const [editing, setEditing] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [systemPrompt, setSystemPrompt] = useState("");
  const [modelName, setModelName] = useState("");

  function startEditing() {
    if (!chatbot) return;
    setName(chatbot.name);
    setDescription(chatbot.description);
    setSystemPrompt(chatbot.system_prompt);
    setModelName(chatbot.model_name);
    setEditing(true);
  }

  function handleSave() {
    updateChatbot.mutate(
      { id, data: { name, description, system_prompt: systemPrompt, model_name: modelName } },
      { onSuccess: () => setEditing(false) },
    );
  }

  function handleDelete() {
    if (confirm(`Delete "${chatbot?.name}"?`)) {
      deleteChatbot.mutate(id, { onSuccess: () => router.push("/chatbots") });
    }
  }

  if (!chatbot) {
    return <div className="py-12 text-sm text-muted">Loading...</div>;
  }

  return (
    <div className="mx-auto max-w-xl space-y-6 animate-fade-in">
      <Link href="/chatbots" className="inline-flex items-center gap-1 text-sm text-muted hover:text-foreground">
        <ArrowLeft className="h-3.5 w-3.5" />
        Back
      </Link>

      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-lg font-semibold tracking-tight">{chatbot.name}</h1>
          <p className="mt-0.5 text-sm text-muted">{chatbot.description}</p>
        </div>
        <div className="flex gap-2">
          <Link
            href={`/chatbots/${id}/documents`}
            className="flex items-center gap-1.5 rounded-lg border border-border px-3 py-1.5 text-[13px] font-medium text-foreground hover:bg-card-hover"
          >
            <FileText className="h-3.5 w-3.5" />
            Docs
          </Link>
          <Link
            href={`/chatbots/${id}/chat`}
            className="flex items-center gap-1.5 rounded-lg bg-primary px-3 py-1.5 text-[13px] font-medium text-white hover:bg-primary-hover"
          >
            <MessageSquare className="h-3.5 w-3.5" />
            Chat
          </Link>
        </div>
      </div>

      {/* Settings */}
      <div className="rounded-lg border border-border bg-card p-4">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-sm font-medium">Settings</h2>
          {!editing ? (
            <button
              onClick={startEditing}
              className="flex items-center gap-1 rounded-md px-2 py-1 text-xs text-muted hover:bg-card-hover hover:text-foreground"
            >
              <Pencil className="h-3 w-3" />
              Edit
            </button>
          ) : (
            <button
              onClick={handleSave}
              disabled={updateChatbot.isPending}
              className="flex items-center gap-1 rounded-md bg-primary px-2.5 py-1 text-xs font-medium text-white hover:bg-primary-hover disabled:opacity-50"
            >
              <Save className="h-3 w-3" />
              {updateChatbot.isPending ? "Saving..." : "Save"}
            </button>
          )}
        </div>

        {editing ? (
          <div className="space-y-3">
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm"
              placeholder="Name"
            />
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={2}
              className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm resize-none"
              placeholder="Description"
            />
            <textarea
              value={systemPrompt}
              onChange={(e) => setSystemPrompt(e.target.value)}
              rows={5}
              className="w-full rounded-lg border border-border bg-background px-3 py-2 font-mono text-xs resize-none"
              placeholder="System prompt"
            />
            <select
              value={modelName}
              onChange={(e) => setModelName(e.target.value)}
              className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm"
            >
              {MODELS.map((m) => (
                <option key={m.value} value={m.value}>{m.label}</option>
              ))}
            </select>
          </div>
        ) : (
          <dl className="space-y-3 text-sm">
            <div className="flex items-center justify-between rounded-md bg-background px-3 py-2">
              <dt className="text-muted">Model</dt>
              <dd className="font-mono text-xs text-foreground">{chatbot.model_name}</dd>
            </div>
            <div className="rounded-md bg-background px-3 py-2">
              <dt className="text-muted mb-1">System prompt</dt>
              <dd className="whitespace-pre-wrap font-mono text-xs text-foreground leading-relaxed">
                {chatbot.system_prompt}
              </dd>
            </div>
          </dl>
        )}
      </div>

      {/* Danger zone */}
      <div className="rounded-lg border border-danger/20 bg-danger-light/50 p-4">
        <h2 className="text-sm font-medium text-danger">Delete chatbot</h2>
        <p className="mt-0.5 text-xs text-muted">This action cannot be undone.</p>
        <button
          onClick={handleDelete}
          disabled={deleteChatbot.isPending}
          className="mt-3 rounded-md border border-danger/30 bg-white px-3 py-1.5 text-xs font-medium text-danger hover:bg-danger-light disabled:opacity-50"
        >
          {deleteChatbot.isPending ? "Deleting..." : "Delete"}
        </button>
      </div>
    </div>
  );
}
