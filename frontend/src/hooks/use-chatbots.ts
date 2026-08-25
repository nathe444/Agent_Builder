"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getChatbots,
  createChatbot,
  updateChatbot,
  deleteChatbot,
} from "@/lib/api";
import type { ChatbotCreate, ChatbotUpdate } from "@/lib/types";

export function useChatbots() {
  return useQuery({ queryKey: ["chatbots"], queryFn: getChatbots });
}

export function useChatbot(id: number) {
  const { data: chatbots } = useChatbots();
  return chatbots?.find((c) => c.id === id) ?? null;
}

export function useCreateChatbot() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: ChatbotCreate) => createChatbot(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["chatbots"] }),
  });
}

export function useUpdateChatbot() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ChatbotUpdate }) =>
      updateChatbot(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["chatbots"] }),
  });
}

export function useDeleteChatbot() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteChatbot(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["chatbots"] }),
  });
}
