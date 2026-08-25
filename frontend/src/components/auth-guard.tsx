"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/auth-store";
import { getMe } from "@/lib/api";

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const token = useAuthStore((s) => s.token);
  const setUser = useAuthStore((s) => s.setUser);
  const router = useRouter();
  const routerRef = useRef(router);
  const fetched = useRef(false);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    routerRef.current = router;
  }, [router]);

  useEffect(() => {
    if (!token) {
      routerRef.current.replace("/login");
      return;
    }

    if (fetched.current) {
      setReady(true);
      return;
    }
    fetched.current = true;

    getMe()
      .then((user) => {
        setUser(user);
        setReady(true);
      })
      .catch(() => {
        // Token invalid — clear it and redirect
        useAuthStore.getState().logout();
        routerRef.current.replace("/login");
      });
  }, [token, setUser]);

  if (!token) return null;
  if (!ready) return null;

  return <>{children}</>;
}
