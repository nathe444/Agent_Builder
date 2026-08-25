"use client";

import { use, useState, useRef } from "react";
import Link from "next/link";
import {
  useDocuments,
  useUploadDocument,
  useAddUrlDocument,
  useDeleteDocument,
} from "@/hooks/use-documents";
import { ArrowLeft, Upload, Link as LinkIcon, Trash2, FileText, Globe, Loader2 } from "lucide-react";

function StatusBadge({ status }: { status: string }) {
  const config: Record<string, { bg: string; text: string }> = {
    ready:      { bg: "bg-success-light", text: "text-success" },
    queued:     { bg: "bg-warning-light", text: "text-warning" },
    processing: { bg: "bg-accent-light", text: "text-accent" },
    uploaded:   { bg: "bg-warning-light", text: "text-warning" },
    error:      { bg: "bg-danger-light", text: "text-danger" },
  };
  const c = config[status] || { bg: "bg-card-hover", text: "text-muted" };
  return (
    <span className={`inline-flex items-center gap-1 rounded px-1.5 py-0.5 text-[11px] font-medium ${c.bg} ${c.text}`}>
      {status === "processing" || status === "queued" ? (
        <span className="h-1 w-1 rounded-full bg-current animate-pulse-dot" />
      ) : null}
      {status}
    </span>
  );
}

export default function DocumentsPage({
  params,
}: {
  params: Promise<{ chatbotId: string }>;
}) {
  const { chatbotId } = use(params);
  const id = Number(chatbotId);

  const { data: documents, isLoading } = useDocuments(id);
  const uploadDoc = useUploadDocument();
  const addUrl = useAddUrlDocument();
  const deleteDoc = useDeleteDocument();

  const fileInputRef = useRef<HTMLInputElement>(null);
  const [url, setUrl] = useState("");
  const [dragOver, setDragOver] = useState(false);

  function handleFileSelect(file: File) {
    uploadDoc.mutate({ chatbotId: id, file });
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFileSelect(file);
  }

  function handleUrlSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!url.trim()) return;
    addUrl.mutate({ chatbot_id: id, url: url.trim() }, { onSuccess: () => setUrl("") });
  }

  function handleDelete(docId: number) {
    if (confirm("Delete this document?")) {
      deleteDoc.mutate({ id: docId, chatbotId: id });
    }
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6 animate-fade-in">
      <Link href={`/chatbots/${id}`} className="inline-flex items-center gap-1 text-sm text-muted hover:text-foreground">
        <ArrowLeft className="h-3.5 w-3.5" />
        Back
      </Link>

      <h1 className="text-lg font-semibold tracking-tight">Documents</h1>

      {/* Upload */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`cursor-pointer rounded-lg border-2 border-dashed p-8 text-center transition-colors ${
          dragOver ? "border-foreground bg-card-hover" : "border-border hover:border-border-hover"
        }`}
      >
        <Upload className="mx-auto h-5 w-5 text-muted-light mb-2" />
        <p className="text-sm text-foreground">Drop a file or click to upload</p>
        <p className="text-xs text-muted mt-1">PDF, DOCX, TXT, CSV, MD, JSON</p>
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept=".pdf,.docx,.txt,.csv,.md,.json,.doc"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) handleFileSelect(file);
            e.target.value = "";
          }}
        />
      </div>

      {uploadDoc.isPending && (
        <div className="flex items-center gap-2 text-sm text-muted">
          <Loader2 className="h-3.5 w-3.5 animate-spin" />
          Uploading {uploadDoc.variables?.file.name}...
        </div>
      )}

      {/* URL */}
      <form onSubmit={handleUrlSubmit} className="flex gap-2">
        <input
          type="url"
          required
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="flex-1 rounded-lg border border-border bg-card px-3 py-2 text-sm placeholder:text-muted-light"
          placeholder="https://example.com/docs"
        />
        <button
          type="submit"
          disabled={addUrl.isPending}
          className="flex items-center gap-1 rounded-lg border border-border bg-card px-3 py-2 text-sm font-medium text-foreground hover:bg-card-hover disabled:opacity-50"
        >
          <LinkIcon className="h-3.5 w-3.5" />
          Add URL
        </button>
      </form>

      {/* List */}
      {isLoading && (
        <div className="space-y-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-14 animate-pulse rounded-lg bg-card border border-border" />
          ))}
        </div>
      )}

      {!isLoading && documents?.length === 0 && (
        <p className="text-sm text-muted text-center py-8">No documents yet.</p>
      )}

      {documents && documents.length > 0 && (
        <div className="space-y-1">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className="flex items-center justify-between rounded-lg border border-transparent px-3 py-2.5 transition-colors hover:border-border hover:bg-card"
            >
              <div className="flex items-center gap-3 min-w-0">
                <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded bg-primary-light text-primary">
                  {doc.source_type === "url" ? (
                    <Globe className="h-3.5 w-3.5" />
                  ) : (
                    <FileText className="h-3.5 w-3.5" />
                  )}
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-medium text-foreground truncate max-w-xs">
                    {doc.file_name || doc.source_value || "Untitled"}
                  </p>
                  <p className="text-xs text-muted">
                    {doc.source_type.toUpperCase()} / {new Date(doc.created_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3 shrink-0 ml-3">
                <StatusBadge status={doc.status} />
                <button
                  onClick={() => handleDelete(doc.id)}
                  className="rounded p-1 text-muted-light hover:text-danger"
                  title="Delete"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
