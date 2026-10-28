# Threat Model & Responsible Use

iPassport handles high-stakes identity data. This note bounds the MVP and the
production path. It is not legal advice.

## Assets

- Biometric captures (face images/video), ID document images, NINs, package JSON.
- Model scores and audit logs (integrity-sensitive: they justify issuance).

## Threats & mitigations (MVP)

| Threat | Mitigation |
|--------|------------|
| Presentation attack (photo-of-photo, deepfake) | Multi-modal checks (document + face + liveness); low-confidence auto-escalation |
| Document forgery / tampering | Region-level segmentation checks, cross-field consistency, quality/tamper flags |
| Score fabrication | HMAC-signed packages, append-only audit log of every model call |
| Data breach / over-retention | 24 h default retention, encrypted temp store, explicit consent per capture |
| Model error (false reject/accept) | Thresholds + mandatory human review band; transparent evidence per decision |
| Misuse as “official” service | Non-affiliation banner in UI and packages; demo payment stub only |

## Out-of-scope for the demo (required before any pilot)

- End-to-end encryption at rest/in transit beyond TLS + local encryption.
- Independent biometric PAD testing (ISO 30107) and ICAO compliance audit.
- Formal DPIA under Uganda’s Data Protection and Privacy Act.
- Government key management and HSM-backed package signing.
- Accessibility and local-language certification.

## Responsible-use rules

1. AI assists; officials decide. No auto-issuance path exists in this repo.
2. Borderline scores escalate — they never silently pass.
3. No training on user captures without explicit, revocable consent.
4. Any deployment must publish its thresholds, retention, and reviewer SLAs.
