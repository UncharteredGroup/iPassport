import { useState } from "react";
import GuideChat from "./components/GuideChat";
import CaptureStep from "./components/CaptureStep";
import PackageView from "./components/PackageView";
import { api } from "./lib/api";
import type { AppType, DocumentResult, FaceResult, PackageResult, PhotoResult, StatusResult } from "./types";

const APP_TYPES: { id: AppType; label: string }[] = [
  { id: "new", label: "New application" },
  { id: "renewal", label: "Renewal" },
  { id: "replacement", label: "Replacement" },
  { id: "minor", label: "Minor" },
];

export default function App() {
  const [appType, setAppType] = useState<AppType>("renewal");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [nin, setNin] = useState("");
  const [doc, setDoc] = useState<DocumentResult | null>(null);
  const [face, setFace] = useState<FaceResult | null>(null);
  const [photo, setPhoto] = useState<PhotoResult | null>(null);
  const [pkg, setPkg] = useState<PackageResult | null>(null);
  const [status, setStatus] = useState<StatusResult | null>(null);
  const [notice, setNotice] = useState("");
  const [applicant, setApplicant] = useState({ surname: "", given_names: "", nin: "", dob: "" });

  async function captureDoc(image: string) {
    setBusy(true);
    try {
      const res = await api.verifyDocument({
        document_type: "national_id_front",
        image,
        expected: nin ? { nin } : {},
      });
      setDoc(res);
      if (res.extracted.nin && !applicant.nin) setApplicant({ ...applicant, nin: res.extracted.nin });
    } catch {
      setNotice("Document check failed — is the backend running?");
    } finally {
      setBusy(false);
    }
  }

  async function captureFace(image: string) {
    setBusy(true);
    try {
      const res = await api.verifyFace({ selfie: image, references: [], liveness_events: [{ prompt: "blink", passed: true }] });
      setFace(res);
    } catch {
      setNotice("Face check failed — is the backend running?");
    } finally {
      setBusy(false);
    }
  }

  async function capturePhoto(image: string) {
    setBusy(true);
    try {
      setPhoto(await api.verifyPhoto({ image }));
    } catch {
      setNotice("Photo check failed — is the backend running?");
    } finally {
      setBusy(false);
    }
  }

  async function buildPackage() {
    setBusy(true);
    setNotice("");
    try {
      const res = await api.buildPackage({
        session_id: sessionId ?? "demo-session",
        applicant,
        application_type: appType,
        evidence: { document_ids: doc ? [doc.evidence_id] : [], face_id: face?.evidence_id ?? null, photo_id: photo?.evidence_id ?? null },
        payment_ref: "demo-pay-001",
      });
      setPkg(res);
      setStatus(await api.status(res.package_id));
    } catch {
      setNotice("Packaging failed — is the backend running?");
    } finally {
      setBusy(false);
    }
  }

  async function escalate() {
    if (!pkg) return;
    const res = await api.escalate({ package_id: pkg.package_id, reason: "Applicant requested human review" });
    setNotice(`Queued for human review at position ${res.position}.`);
  }

  const set = (k: keyof typeof applicant) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setApplicant({ ...applicant, [k]: e.target.value });

  return (
    <main className="wrap">
      <header>
        <h1>iPassport</h1>
        <p className="muted">AI-assisted passport application — civic-tech demo, not an official service.</p>
      </header>

      {notice && <p className="notice">{notice}</p>}

      <div className="panel">
        <h2>1. Application type</h2>
        <div className="row" role="radiogroup" aria-label="Application type">
          {APP_TYPES.map((t) => (
            <button key={t.id} className={appType === t.id ? "primary" : "secondary"} onClick={() => setAppType(t.id)}>
              {t.label}
            </button>
          ))}
        </div>
      </div>

      <GuideChat appType={appType} sessionId={sessionId} onSession={setSessionId} />

      <div className="panel">
        <h2>2. Your details</h2>
        <div className="grid">
          <label>Surname<input value={applicant.surname} onChange={set("surname")} /></label>
          <label>Given names<input value={applicant.given_names} onChange={set("given_names")} /></label>
          <label>NIN<input value={applicant.nin} onChange={(e) => { set("nin")(e); setNin(e.target.value); }} placeholder="CM…" /></label>
          <label>Date of birth<input value={applicant.dob} onChange={set("dob")} placeholder="1990-01-01" /></label>
        </div>
      </div>

      <CaptureStep
        title="3. National ID capture"
        hint="Align your National ID in the frame. Segmentation regions appear after analysis."
        regions={doc?.regions ?? []}
        checks={doc?.checks ?? []}
        decision={doc?.decision}
        scoreLine={doc ? `Quality ${doc.quality_score.toFixed(2)}` : undefined}
        onCapture={captureDoc}
        busy={busy}
      />

      <CaptureStep
        title="4. Selfie + liveness"
        hint="Face the camera and blink when prompted."
        facingMode="user"
        checks={face ? [
          { name: "face_match", passed: face.match_score >= 0.8, detail: face.match_score.toFixed(2) },
          { name: "liveness", passed: face.liveness_score >= 0.7, detail: face.liveness_score.toFixed(2) },
        ] : []}
        decision={face?.decision}
        scoreLine={face ? `Match ${face.match_score.toFixed(2)} · Liveness ${face.liveness_score.toFixed(2)}` : undefined}
        onCapture={captureFace}
        busy={busy}
      />

      <CaptureStep
        title="5. Passport photo"
        hint="Plain background, even light, face filling the frame."
        facingMode="user"
        checks={photo?.icao_checks ?? []}
        decision={photo?.decision}
        scoreLine={photo ? `Score ${photo.score.toFixed(2)} — ${photo.guidance}` : undefined}
        onCapture={capturePhoto}
        busy={busy}
      />

      <div className="panel">
        <h2>6. Payment (demo stub) + package</h2>
        <p className="muted">Production would integrate mobile money / URA here. The demo uses a fixed reference.</p>
        <div className="row">
          <button className="primary" onClick={buildPackage} disabled={busy || !applicant.surname || !applicant.nin}>
            {busy ? "Working…" : "Generate application package"}
          </button>
        </div>
      </div>

      <PackageView pkg={pkg} status={status} onEscalate={escalate} />

      <footer>
        <p className="muted">Open source (MIT). Evidence is temporary; scores are AI-assisted and reviewable.</p>
      </footer>
    </main>
  );
}
