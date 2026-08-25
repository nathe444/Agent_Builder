"use client";

import { useAuthStore } from "@/stores/auth-store";
import { useRouter } from "next/navigation";
import { LogOut } from "lucide-react";

export function Topbar() {
  const { user, logout } = useAuthStore();
  const router = useRouter();

  function handleLogout() {
    logout();
    router.replace("/login");
  }

  return (
    <header className="flex items-center justify-between border-b border-border bg-card px-5 py-2.5">
      <div />
      <div className="flex items-center gap-3">
        <span className="text-[13px] text-muted">{user?.name || ""}</span>
        <button
          onClick={handleLogout}
          className="rounded p-1 text-muted-light transition-colors hover:text-foreground"
          title="Sign out"
        >
          <LogOut className="h-4 w-4" />
        </button>
      </div>
    </header>
  );
}
