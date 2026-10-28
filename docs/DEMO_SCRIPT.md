# Demo Script (3–5 minutes)

Goal: show the before/after and prove every AI claim is auditable.

## 0:00–0:45 — The pain (traditional process)

- Online form on passports.go.ug → UGX 250,000 bank payment → appointment →
  travel to Kampala / Mbale / Mbarara / Gulu / Arua / Jinja for biometrics.
- 1–3 physical visits, 7–14+ day waits, fibre-cut outages, broker pressure.

## 0:45–3:30 — The iPassport flow (live)

1. Open the PWA, pick **Renewal**. The Muse agent asks only what a renewal
   needs and explains the recommender + photo rules.
2. Capture a National ID. Show the **SAM 3.1 segmentation overlay**
   (photo / name / NIN regions) and the extracted fields cross-checked live.
3. Hold up a blurry image on purpose: the agent flags glare/crop and asks for
   a retake. Then capture a clean one and watch it pass.
4. Guided selfie with a liveness prompt (blink / turn). Show face-match and
   liveness scores side by side.
5. Capture the passport photo. Show one failing ICAO check (e.g. background)
   with fix guidance, then the passing version.
6. Payment stub → **Generate package**. Open the JSON: applicant data,
   evidence refs, per-check scores, overall risk score, signature, audit log.

## 3:30–4:30 — Trust story

- Every score expands to its evidence. One click escalates to human review.
- Tracker: `AI Verified → Ready for Official Review → Approved for Issuance`.
- Close: open-source repo link, contribution invite.

## Backup plan

- No camera on stage: use the sample images in `frontend/public/samples/`.
- No network: backend `IPASSPORT_MOCK_MODE=true` runs the whole flow offline.
