# iPassport API Reference (MVP)

Base URL: `http://localhost:8000`. All request/response bodies are JSON.
Images are base64 data URLs (`data:image/jpeg;base64,…`).

## POST /api/guide/chat

One agentic guidance turn.

```json
{
  "session_id": "optional-uuid",
  "application_type": "new | renewal | replacement | minor",
  "messages": [{ "role": "user", "content": "I want to renew" }]
}
```

Response:

```json
{
  "session_id": "uuid",
  "reply": "…",
  "missing_fields": ["nin", "passport_photo"],
  "next_actions": ["capture_national_id"],
  "done": false
}
```

## POST /api/verify/document

```json
{
  "document_type": "national_id_front | national_id_back | recommender_id | birth_certificate | old_passport",
  "image": "data:image/jpeg;base64,…",
  "expected": { "nin": "CM123…", "surname": "…" }
}
```

Response:

```json
{
  "extracted": { "nin": "…", "surname": "…", "dob": "…" },
  "regions": [{ "label": "photo", "box": [x, y, w, h], "confidence": 0.98 }],
  "checks": [{ "name": "nin_match", "passed": true, "detail": "…" }],
  "quality": { "score": 0.91, "issues": [] },
  "decision": "accept | retake | escalate"
}
```

## POST /api/verify/face

```json
{
  "selfie": "data:image/jpeg;base64,…",
  "references": ["data:image/jpeg;base64,…"],
  "liveness_events": [{ "prompt": "blink", "passed": true }]
}
```

Response: `{ "match_score": 0.93, "liveness_score": 0.88, "indicators": [], "decision": "accept" }`.

## POST /api/verify/photo

```json
{ "image": "data:image/jpeg;base64,…" }
```

Response: `{ "icao_checks": [{ "name": "plain_background", "passed": true }], "score": 0.9, "guidance": "…", "decision": "accept" }`.

## POST /api/package

```json
{
  "session_id": "uuid",
  "applicant": { "surname": "…", "given_names": "…", "nin": "…", "dob": "…" },
  "application_type": "renewal",
  "evidence": { "document_ids": ["…"], "face_id": "…", "photo_id": "…" },
  "payment_ref": "demo-pay-001"
}
```

Response: `{ "package_id": "uuid", "risk_score": 0.12, "summary": {…}, "signature": "hmac-sha256:…", "audit_ref": "…" }`.

## GET /api/status/{package_id}

Response: `{ "package_id": "…", "stage": "ai_verified", "history": [{ "stage": "…", "at": "…" }] }`.

Stages: `captured → ai_verified → ready_for_official_review → approved_for_issuance`.

## POST /api/review/escalate

```json
{ "package_id": "uuid", "reason": "low face-match confidence" }
```

Response: `{ "package_id": "…", "queued": true, "position": 3 }`.
