"use client";

import { use, useState, useRef, useEffect, useCallback } from "react";
import Link from "next/link";
import { useChatbot } from "@/hooks/use-chatbots";
import { useMessages } from "@/hooks/use-chat";
import {
  createConversation,
  getConversations,
  deleteConversation,
  sendMessageStream,
} from "@/lib/api";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, Plus, Send, Trash2, MessageSquare } from "lucide-react";
import type { Message } from "@/lib/types";

export default function ChatPage({
  params,
}: {
  params: Promise<{ chatbotId: string }>;
}) {
  const { chatbotId } = use(params);
  const id = Number(chatbotId);
  const chatbot = useChatbot(id);
  const qc = useQueryClient();

  const [activeConvId, setActiveConvId] = useState<number | null>(null);
  const [isSending, setIsSending] = useState(false);
  const [input, setInput] = useState("");
  const [localMessages, setLocalMessages] = useState<Message[]>([]);
  const [streamedTokens, setStreamedTokens] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { data: serverMessages } = useMessages(activeConvId);
  const { data: conversations } = useQuery({
    queryKey: ["conversations", id],
    queryFn: () => getConversations(id),
  });

  // Merge server messages with local optimistic messages
  const messages = (() => {
    const server = serverMessages || [];
    const localOnly = localMessages.filter(
      (lm) => !server.some((sm) => sm.id === lm.id)
    );
    return [...server, ...localOnly];
  })();

  // Clear local messages once server catches up
  useEffect(() => {
    if (serverMessages && serverMessages.length > 0) {
      setLocalMessages((prev) =>
        prev.filter((lm) => !serverMessages.some((sm) => sm.id === lm.id))
      );
    }
  }, [serverMessages]);

  const createConv = useMutation({
    mutationFn: () => createConversation(id, "New conversation"),
    onSuccess: (conv) => {
      qc.invalidateQueries({ queryKey: ["conversations", id] });
      setActiveConvId(conv.id);
    },
  });

  const deleteConv = useMutation({
    mutationFn: (convId: number) => deleteConversation(convId),
    onSuccess: (_, convId) => {
      qc.invalidateQueries({ queryKey: ["conversations", id] });
      if (activeConvId === convId) {
        setActiveConvId(null);
        setLocalMessages([]);
      }
    },
  });

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamedTokens]);

  const handleSend = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      const question = input.trim();
      if (!question || isSending) return;

      setInput("");
      setIsSending(true);
      setStreamedTokens("");

      // 1. Show user message immediately (optimistic)
      const tempUserMsg: Message = {
        id: Date.now(),
        role: "user",
        content: question,
        conversation_id: activeConvId || 0,
        created_at: new Date().toISOString(),
        citations: [],
      };
      setLocalMessages((prev) => [...prev, tempUserMsg]);

      try {
        // 2. Auto-create conversation if needed
        let convId = activeConvId;
        if (!convId) {
          const conv = await createConversation(id, question.slice(0, 50));
          convId = conv.id;
          setActiveConvId(convId);
          qc.invalidateQueries({ queryKey: ["conversations", id] });
        }

        // 3. Stream response directly — no hook closure issues
        let fullResponse = "";

        await sendMessageStream(
          convId,
          { question },
          (token) => {
            fullResponse += token;
            setStreamedTokens(fullResponse);
          }
        );

        // 4. Invalidate — server already saved the message during streaming
        await qc.invalidateQueries({ queryKey: ["messages", convId] });
      } catch (err) {
        console.error("Chat error:", err);
        setLocalMessages((prev) =>
          prev.filter((m) => m.id !== tempUserMsg.id)
        );
      } finally {
        setIsSending(false);
        // Keep streamedTokens visible until server response replaces it
        // Clear after a short delay to avoid flash
        setTimeout(() => setStreamedTokens(""), 100);
      }
    },
    [input, isSending, activeConvId, id, qc]
  );

  return (
    <div className="flex h-full gap-0">
      {/* Conversations sidebar */}
      <div className="flex w-56 shrink-0 flex-col border-r border-border bg-card">
        <div className="flex items-center justify-between border-b border-border px-3 py-2.5">
          <span className="text-xs font-medium text-muted">Conversations</span>
          <button
            onClick={() => createConv.mutate()}
            disabled={createConv.isPending}
            className="rounded p-1 text-muted-light hover:text-foreground"
          >
            <Plus className="h-3.5 w-3.5" />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-1.5">
          {conversations?.map((conv) => (
            <div
              key={conv.id}
              className={`group mb-0.5 flex items-center justify-between rounded px-2 py-1.5 text-[13px] transition-colors ${
                activeConvId === conv.id
                  ? "bg-primary-light font-medium text-foreground"
                  : "text-muted hover:bg-card-hover hover:text-foreground"
              }`}
            >
              <button
                onClick={() => setActiveConvId(conv.id)}
                className="flex flex-1 items-center gap-1.5 truncate"
              >
                <MessageSquare className="h-3 w-3 shrink-0" />
                <span className="truncate">{conv.title || "New"}</span>
              </button>
              <button
                onClick={() => deleteConv.mutate(conv.id)}
                className="rounded p-0.5 text-muted-light opacity-0 hover:text-danger group-hover:opacity-100"
              >
                <Trash2 className="h-3 w-3" />
              </button>
            </div>
          ))}
          {conversations && conversations.length === 0 && (
            <p className="py-6 text-center text-xs text-muted-light">
              No conversations
            </p>
          )}
        </div>
      </div>

      {/* Chat area */}
      <div className="flex flex-1 flex-col">
        {/* Header */}
        <div className="flex items-center gap-3 border-b border-border bg-card px-4 py-2.5">
          <Link
            href={`/chatbots/${id}`}
            className="text-muted-light hover:text-foreground"
          >
            <ArrowLeft className="h-4 w-4" />
          </Link>
          <div>
            <p className="text-sm font-medium">{chatbot?.name || "Chat"}</p>
            <p className="text-[11px] text-muted">{chatbot?.model_name}</p>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4">
          {messages.length === 0 && !isSending ? (
            <div className="flex h-full items-center justify-center text-sm text-muted">
              Send a message to start
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${
                    msg.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[70%] rounded-lg px-3 py-2 text-sm leading-relaxed ${
                      msg.role === "user"
                        ? "bg-primary text-white"
                        : "bg-card border border-border text-foreground"
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                    {msg.citations && msg.citations.length > 0 && (
                      <div className="mt-1.5 flex flex-wrap gap-1">
                        {msg.citations.map((c, i) => (
                          <span
                            key={i}
                            className={`rounded px-1.5 py-0.5 text-[10px] font-mono ${
                              msg.role === "user"
                                ? "bg-white/15 text-white/70"
                                : "bg-primary-light text-primary"
                            }`}
                          >
                            Doc {c.document_id}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {/* Streaming response */}
              {isSending && streamedTokens && (
                <div className="flex justify-start">
                  <div className="max-w-[70%] rounded-lg bg-card border border-border px-3 py-2 text-sm leading-relaxed text-foreground">
                    <p className="whitespace-pre-wrap">{streamedTokens}</p>
                  </div>
                </div>
              )}
              {/* Typing indicator */}
              {isSending && !streamedTokens && (
                <div className="flex justify-start">
                  <div className="rounded-lg bg-card border border-border px-3 py-2 text-sm text-muted-light">
                    <span className="animate-pulse">...</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input */}
        <form
          onSubmit={handleSend}
          className="flex items-center gap-2 border-t border-border px-4 py-3 bg-card"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            disabled={isSending}
            className="flex-1 rounded-lg border border-border bg-background px-3 py-2 text-sm placeholder:text-muted-light disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isSending || !input.trim()}
            className="rounded-lg bg-primary p-2 text-white transition-colors hover:bg-primary-hover disabled:opacity-30"
          >
            <Send className="h-4 w-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
