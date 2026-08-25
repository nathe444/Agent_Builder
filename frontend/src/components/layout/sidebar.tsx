"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useChatbots } from "@/hooks/use-chatbots";
import { cn } from "@/lib/utils";
import { MessageSquare, Plus, Cpu } from "lucide-react";

export function Sidebar() {
  const { data: chatbots } = useChatbots();
  const pathname = usePathname();

  return (
    <aside className="flex w-60 flex-col bg-sidebar-bg">
      <div className="flex items-center gap-2.5 border-b border-white/10 px-4 py-3.5">
        <Cpu className="h-4 w-4 text-sidebar-text" />
        <span className="text-[13px] font-semibold text-sidebar-text-active tracking-tight">
          Freebuff
        </span>
      </div>

      <div className="flex-1 overflow-y-auto px-2 py-3">
        <Link
          href="/chatbots/new"
          className="mb-2 flex items-center gap-2 rounded-md px-2.5 py-1.5 text-[13px] text-sidebar-text transition-colors hover:bg-sidebar-hover hover:text-sidebar-text-active"
        >
          <Plus className="h-3.5 w-3.5" />
          New chatbot
        </Link>

        <div className="mt-1 space-y-px">
          {chatbots?.map((chatbot) => {
            const isActive = pathname.includes(`/chatbots/${chatbot.id}`);
            return (
              <Link
                key={chatbot.id}
                href={`/chatbots/${chatbot.id}`}
                className={cn(
                  "flex items-center gap-2 rounded-md px-2.5 py-1.5 text-[13px] transition-colors",
                  isActive
                    ? "bg-sidebar-active text-sidebar-text-active font-medium"
                    : "text-sidebar-text hover:bg-sidebar-hover hover:text-sidebar-text-active",
                )}
              >
                <MessageSquare className="h-3.5 w-3.5 shrink-0" />
                <span className="truncate">{chatbot.name}</span>
              </Link>
            );
          })}
        </div>
      </div>

      <div className="border-t border-white/10 px-4 py-2.5">
        <p className="text-[11px] text-sidebar-text/60">
          {chatbots?.length || 0} chatbot{(chatbots?.length || 0) !== 1 ? "s" : ""}
        </p>
      </div>
    </aside>
  );
}
