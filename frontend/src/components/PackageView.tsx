import type { PackageResult, StatusResult } from "../types";

interface Props {
  pkg: PackageResult | null;
  status: StatusResult | null;
  onEscalate: () => void;
}

export default function PackageView({ pkg, status, onEscalate }: Props) {
  if (!pkg) return null;
  return (
    <div className="panel">
      <h2>Application package</h2>
      <dl className="facts">
        <dt>Package ID</dt><dd><code>{pkg.package_id}</code></dd>
        <dt>Risk score</dt><dd>{pkg.risk_score.toFixed(2)} (lower is better)</dd>
        <dt>Signature</dt><dd><code>{pkg.signature.slice(0, 32)}…</code></dd>
        <dt>Audit ref</dt><dd><code>{pkg.audit_ref}</code></dd>
        {status && (
          <>
            <dt>Stage</dt><dd>{status.stage.replaceAll("_", " ")}</dd>
            <dt>History</dt>
            <dd>{status.history.map((h) => h.stage.replaceAll("_", " ")).join(" → ")}</dd>
          </>
        )}
      </dl>
      <details>
        <summary>Package JSON (auditable evidence)</summary>
        <pre>{JSON.stringify(pkg.summary, null, 2)}</pre>
      </details>
      <div className="row">
        <button className="secondary" onClick={onEscalate}>Escalate to human review</button>
      </div>
    </div>
  );
}
