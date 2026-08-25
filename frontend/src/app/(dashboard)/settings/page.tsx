"use client";

import { useAuthStore } from "@/stores/auth-store";
import { useRouter } from "next/navigation";
import { LogOut } from "lucide-react";

export default function SettingsPage() {
  const { user, logout } = useAuthStore();
  const router = useRouter();

  function handleLogout() {
    logout();
    router.replace("/login");
  }

  return (
    <div className="mx-auto max-w-lg space-y-6 animate-fade-in">
      <h1 className="text-lg font-semibold tracking-tight">Settings</h1>

      <div className="rounded-lg border border-border bg-card p-4">
        <h2 className="text-sm font-medium mb-3">Profile</h2>
        <dl className="space-y-2 text-sm">
          <div className="flex items-center justify-between rounded-md bg-background px-3 py-2">
            <dt className="text-muted">Name</dt>
            <dd className="text-foreground">{user?.name}</dd>
          </div>
          <div className="flex items-center justify-between rounded-md bg-background px-3 py-2">
            <dt className="text-muted">Email</dt>
            <dd className="text-foreground">{user?.email}</dd>
          </div>
        </dl>
      </div>

      <div className="rounded-lg border border-border bg-card p-4">
        <h2 className="text-sm font-medium mb-2">Sign out</h2>
        <p className="text-xs text-muted mb-3">End your current session.</p>
        <button
          onClick={handleLogout}
          className="flex items-center gap-1.5 rounded-md border border-border px-3 py-1.5 text-sm font-medium text-foreground hover:bg-card-hover"
        >
          <LogOut className="h-3.5 w-3.5" />
          Sign out
        </button>
      </div>
    </div>
  );
}
