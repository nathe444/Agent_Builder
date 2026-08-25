"use client";

import Link from "next/link";
import { useChatbots, useDeleteChatbot } from "@/hooks/use-chatbots";
import { Plus, Trash2, MessageSquare } from "lucide-react";

export default function ChatbotsPage() {
  const { data: chatbots, isLoading } = useChatbots();
  const deleteChatbot = useDeleteChatbot();

  function handleDelete(id: number, name: string) {
    if (confirm(`Delete "${name}"?`)) {
      deleteChatbot.mutate(id);
    }
  }

  return (
    <div className="mx-auto max-w-3xl">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-lg font-semibold tracking-tight">Chatbots</h1>
        <Link
          href="/chatbots/new"
          className="flex items-center gap-1.5 rounded-lg bg-primary px-3 py-1.5 text-[13px] font-medium text-white transition-colors hover:bg-primary-hover"
        >
          <Plus className="h-3.5 w-3.5" />
          New
        </Link>
      </div>

      {isLoading && (
        <div className="space-y-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 animate-pulse rounded-lg bg-card border border-border" />
          ))}
        </div>
      )}

      {!isLoading && chatbots?.length === 0 && (
        <div className="rounded-lg border border-dashed border-border p-12 text-center">
          <p className="text-sm text-muted">No chatbots yet.</p>
          <Link
            href="/chatbots/new"
            className="mt-3 inline-flex items-center gap-1 text-sm font-medium text-foreground hover:underline"
          >
            <Plus className="h-3.5 w-3.5" />
            Create your first chatbot
          </Link>
        </div>
      )}

      <div className="space-y-1">
        {chatbots?.map((chatbot) => (
          <div
            key={chatbot.id}
            className="group flex items-center justify-between rounded-lg border border-transparent px-3 py-2.5 transition-colors hover:border-border hover:bg-card"
          >
            <Link href={`/chatbots/${chatbot.id}`} className="flex items-center gap-3 min-w-0 flex-1">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-primary-light text-primary">
                <MessageSquare className="h-4 w-4" />
              </div>
              <div className="min-w-0">
                <p className="text-sm font-medium text-foreground truncate">{chatbot.name}</p>
                <p className="text-xs text-muted truncate">{chatbot.description}</p>
              </div>
            </Link>
            <div className="flex items-center gap-2 shrink-0 ml-3">
              <span className="text-[11px] text-muted-light font-mono">{chatbot.model_name}</span>
              <button
                onClick={() => handleDelete(chatbot.id, chatbot.name)}
                className="rounded p-1 text-muted-light opacity-0 transition-opacity hover:text-danger group-hover:opacity-100"
                title="Delete"
              >
                <Trash2 className="h-3.5 w-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
