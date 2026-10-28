import { useEffect, useRef, useState } from "react";
import { captureFrame, fileToDataUrl, startCamera, stopCamera } from "../lib/camera";
import type { Check, Region } from "../types";

interface Props {
  title: string;
  hint: string;
  facingMode?: string;
  regions?: Region[];
  checks?: Check[];
  decision?: string;
  scoreLine?: string;
  onCapture: (image: string) => void;
  busy: boolean;
}

export default function CaptureStep({ title, hint, facingMode = "environment", regions = [], checks = [], decision, scoreLine, onCapture, busy }: Props) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    let s: MediaStream | null = null;
    (async () => {
      try {
        if (videoRef.current) {
          s = await startCamera(videoRef.current, facingMode);
          if (active) setStream(s);
          else stopCamera(s);
        }
      } catch {
        if (active) setError("Camera unavailable — use file upload instead.");
      }
    })();
    return () => {
      active = false;
      stopCamera(s);
    };
  }, [facingMode]);

  function snap() {
    if (videoRef.current && videoRef.current.videoWidth > 0) {
      onCapture(captureFrame(videoRef.current));
    }
  }

  async function upload(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (f) onCapture(await fileToDataUrl(f));
  }

  return (
    <div className="panel">
      <h2>{title}</h2>
      <p className="muted">{hint}</p>
      <div className="viewfinder">
        <video ref={videoRef} playsInline muted />
        {regions.map((r, i) => (
          <span
            key={i}
            className="region"
            style={{ left: `${r.box[0] * 100}%`, top: `${r.box[1] * 100}%`, width: `${r.box[2] * 100}%`, height: `${r.box[3] * 100}%` }}
            title={`${r.label} (${r.confidence.toFixed(2)})`}
          >
            {r.label}
          </span>
        ))}
      </div>
      {error && <p className="warn">{error}</p>}
      <div className="row">
        <button onClick={snap} disabled={busy || !stream}>{busy ? "Checking…" : "Capture"}</button>
        <label className="upload">
          Upload file
          <input type="file" accept="image/*" onChange={upload} hidden />
        </label>
      </div>
      {scoreLine && <p><strong>{scoreLine}</strong></p>}
      {decision && (
        <p className={decision === "accept" ? "ok" : decision === "retake" ? "warn" : "flag"}>
          Decision: {decision}
        </p>
      )}
      {checks.length > 0 && (
        <ul className="checks">
          {checks.map((c) => (
            <li key={c.name} className={c.passed ? "ok" : "flag"}>
              {c.passed ? "✓" : "✗"} {c.name} <span className="muted">{c.detail}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
