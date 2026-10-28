import { useState } from "react";
import { api } from "../lib/api";
import type { AppType } from "../types";

interface Props {
  appType: AppType;
  sessionId: string | null;
  onSession: (id: string) => void;
}

interface Msg {
  role: "user" | "assistant";
  content: string;
}

export default function GuideChat({ appType, sessionId, onSession }: Props) {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [missing, setMissing] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);

  async function send() {
    const text = input.trim();
    if (!text || busy) return;
    setBusy(true);
    const next = [...messages, { role: "user" as const, content: text }];
    setMessages(next);
    setInput("");
    try {
      const res = await api.guideChat({ session_id: sessionId, application_type: appType, messages: next });
      onSession(res.session_id);
      setMessages([...next, { role: "assistant", content: res.reply }]);
      setMissing(res.missing_fields);
    } catch {
      setMessages([...next, { role: "assistant", content: "The guide is unreachable. Is the backend running?" }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="panel">
      <h2>Application guide</h2>
      <p className="muted">The agent asks only what a {appType} application needs.</p>
      <div className="chat">
        {messages.length === 0 && <p className="muted">Say hello to begin — e.g. “I want to apply”.</p>}
        {messages.map((m, i) => (
          <p key={i} className={m.role === "user" ? "msg user" : "msg agent"}>{m.content}</p>
        ))}
      </div>
      <div className="row">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Type your answer…"
          aria-label="Message the guide"
        />
        <button onClick={send} disabled={busy}>{busy ? "…" : "Send"}</button>
      </div>
      {missing.length > 0 && (
        <p className="muted">Still needed: {missing.join(", ")}</p>
      )}
    </div>
  );
}
