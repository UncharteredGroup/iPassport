export type Decision = "accept" | "retake" | "escalate";

export interface Check {
  name: string;
  passed: boolean;
  detail: string;
}

export interface Region {
  label: string;
  box: [number, number, number, number];
  confidence: number;
}

export interface DocumentResult {
  evidence_id: string;
  extracted: Record<string, string>;
  regions: Region[];
  checks: Check[];
  quality_score: number;
  quality_issues: string[];
  decision: Decision;
}

export interface FaceResult {
  evidence_id: string;
  match_score: number;
  liveness_score: number;
  indicators: string[];
  decision: Decision;
}

export interface PhotoResult {
  evidence_id: string;
  icao_checks: Check[];
  score: number;
  guidance: string;
  decision: Decision;
}

export interface PackageResult {
  package_id: string;
  risk_score: number;
  summary: Record<string, unknown>;
  signature: string;
  audit_ref: string;
}

export interface StatusResult {
  package_id: string;
  stage: string;
  history: { stage: string; at: string }[];
}

export type AppType = "new" | "renewal" | "replacement" | "minor";
