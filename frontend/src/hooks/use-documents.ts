"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getDocuments,
  uploadDocument,
  addUrlDocument,
  deleteDocument,
} from "@/lib/api";
import type { UrlDocumentCreate } from "@/lib/types";

export function useDocuments(chatbotId: number) {
  return useQuery({
    queryKey: ["documents", chatbotId],
    queryFn: () => getDocuments(chatbotId),
    refetchInterval: (query) => {
      // Poll while any document is still processing
      const docs = query.state.data;
      if (docs?.some((d) => ["queued", "processing"].includes(d.status))) {
        return 3000;
      }
      return false;
    },
  });
}

export function useUploadDocument() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      chatbotId,
      file,
    }: {
      chatbotId: number;
      file: File;
    }) => uploadDocument(chatbotId, file),
    onSuccess: (_data, vars) => {
      qc.invalidateQueries({ queryKey: ["documents", vars.chatbotId] });
    },
  });
}

export function useAddUrlDocument() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: UrlDocumentCreate) => addUrlDocument(data),
    onSuccess: (_data, vars) => {
      qc.invalidateQueries({ queryKey: ["documents", vars.chatbot_id] });
    },
  });
}

export function useDeleteDocument() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      chatbotId,
    }: {
      id: number;
      chatbotId: number;
    }) => deleteDocument(id),
    onSuccess: (_data, vars) => {
      qc.invalidateQueries({ queryKey: ["documents", vars.chatbotId] });
    },
  });
}
