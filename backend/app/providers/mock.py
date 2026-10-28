"""Deterministic mock provider: full demo flow with no API keys.

Heuristics are intentionally simple and documented: short/empty payloads read
as low quality so the UI can demonstrate retake guidance.
"""

from typing import Any

from .base import Provider

REQUIRED_BY_TYPE = {
    "new": ["nin", "surname", "dob", "recommender", "passport_photo"],
    "renewal": ["nin", "old_passport", "passport_photo"],
    "replacement": ["nin", "police_report", "passport_photo"],
    "minor": ["birth_certificate", "parental_consent", "parent_id", "passport_photo"],
}


class MockProvider(Provider):
    name = "mock"

    async def agent_turn(
        self, application_type: str, messages: list[dict[str, str]]
    ) -> dict[str, Any]:
        required = REQUIRED_BY_TYPE.get(application_type, REQUIRED_BY_TYPE["new"])
        text = " ".join(m.get("content", "") for m in messages).lower()
        missing = [f for f in required if f.replace("_", " ") not in text and f not in text]
        if not missing:
            return {
                "reply": "Everything required is covered. Capture your documents and photo, then generate the package.",
                "missing_fields": [],
                "next_actions": ["capture_documents", "capture_photo", "generate_package"],
                "done": True,
            }
        nxt = missing[0]
        return {
            "reply": (
                f"For a {application_type} application I still need: {', '.join(missing)}. "
                f"Let's start with {nxt.replace('_', ' ')}."
            ),
            "missing_fields": missing,
            "next_actions": [f"provide_{nxt}"],
            "done": False,
        }

    async def segment_document(
        self, document_type: str, image: str
    ) -> dict[str, Any]:
        payload_len = len(image or "")
        if payload_len < 500:
            return {
                "regions": [],
                "extracted": {},
                "quality": {"score": 0.2, "issues": ["image_too_small", "possible_crop"]},
            }
        # Deterministic pseudo-extraction from payload length (demo only).
        seed = payload_len % 997
        return {
            "regions": [
                {"label": "photo", "box": [0.05, 0.2, 0.25, 0.4], "confidence": 0.98},
                {"label": "name", "box": [0.35, 0.2, 0.55, 0.12], "confidence": 0.96},
                {"label": "nin", "box": [0.35, 0.36, 0.4, 0.1], "confidence": 0.97},
                {"label": "dob", "box": [0.35, 0.5, 0.3, 0.1], "confidence": 0.94},
            ],
            "extracted": {
                "nin": f"CM{100000 + seed:06d}X",
                "surname": "DEMO",
                "given_names": "APPLICANT",
                "dob": "1990-01-01",
                "document_type": document_type,
            },
            "quality": {"score": 0.91, "issues": []},
        }

    async def face_scores(
        self, selfie: str, references: list[str], liveness: list[dict[str, Any]]
    ) -> dict[str, Any]:
        if len(selfie or "") < 500:
            return {"match_score": 0.3, "liveness_score": 0.2,
                    "indicators": ["low_quality_capture"]}
        prompts = [e for e in liveness if e.get("passed")]
        liveness_score = 0.88 if prompts else 0.55
        indicators = [] if prompts else ["no_liveness_events"]
        return {"match_score": 0.93, "liveness_score": liveness_score,
                "indicators": indicators}

    async def photo_assessment(self, image: str) -> dict[str, Any]:
        if len(image or "") < 500:
            return {
                "checks": [
                    {"name": "resolution", "passed": False, "detail": "Image too small"},
                ],
                "score": 0.25,
                "guidance": "Move closer and capture in good light against a plain background.",
            }
        return {
            "checks": [
                {"name": "plain_background", "passed": True, "detail": "Background uniform"},
                {"name": "face_size", "passed": True, "detail": "Face 70% of frame height"},
                {"name": "lighting", "passed": True, "detail": "Even illumination"},
                {"name": "eyes_visible", "passed": True, "detail": "No glasses detected"},
            ],
            "score": 0.92,
            "guidance": "Photo meets ICAO-style checks.",
        }
