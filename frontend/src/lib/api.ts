const BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json() as Promise<T>;
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json() as Promise<T>;
}

export const api = {
  health: () => get<{ status: string; mode: string }>("/api/health"),
  guideChat: (body: unknown) =>
    post<{ session_id: string; reply: string; missing_fields: string[]; next_actions: string[]; done: boolean }>(
      "/api/guide/chat",
      body
    ),
  verifyDocument: (body: unknown) => post<import("../types").DocumentResult>("/api/verify/document", body),
  verifyFace: (body: unknown) => post<import("../types").FaceResult>("/api/verify/face", body),
  verifyPhoto: (body: unknown) => post<import("../types").PhotoResult>("/api/verify/photo", body),
  buildPackage: (body: unknown) => post<import("../types").PackageResult>("/api/package", body),
  status: (id: string) => get<import("../types").StatusResult>(`/api/status/${id}`),
  escalate: (body: unknown) => post<{ package_id: string; queued: boolean; position: number }>("/api/review/escalate", body),
};
