"""Live Meta Model API provider (Muse agent, SAM 3.1, Muse Image).

Thin httpx client: one place to adapt when model endpoints change. Every call
returns the same shape as MockProvider so services stay model-agnostic.
"""

from typing import Any

import httpx

from .base import Provider


class MetaApiProvider(Provider):
    name = "meta-api"

    def __init__(self, api_base: str, api_key: str, agent_model: str,
                 vision_model: str, image_model: str) -> None:
        self.api_base = api_base.rstrip("/")
        self.api_key = api_key
        self.agent_model = agent_model
        self.vision_model = vision_model
        self.image_model = image_model

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    async def agent_turn(
        self, application_type: str, messages: list[dict[str, str]]
    ) -> dict[str, Any]:
        system = (
            "You are the iPassport application guide for Ugandan passports. "
            f"Application type: {application_type}. Ask only for required evidence, "
            "explain each requirement plainly, and reply with JSON: "
            '{"reply": str, "missing_fields": [str], "next_actions": [str], "done": bool}.'
        )
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                f"{self.api_base}/agent/turn",
                headers=self._headers(),
                json={"model": self.agent_model, "system": system, "messages": messages},
            )
            resp.raise_for_status()
            return resp.json()

    async def segment_document(
        self, document_type: str, image: str
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=90) as client:
            resp = await client.post(
                f"{self.api_base}/vision/segment",
                headers=self._headers(),
                json={"model": self.vision_model, "document_type": document_type,
                      "image": image},
            )
            resp.raise_for_status()
            return resp.json()

    async def face_scores(
        self, selfie: str, references: list[str], liveness: list[dict[str, Any]]
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=90) as client:
            resp = await client.post(
                f"{self.api_base}/vision/face",
                headers=self._headers(),
                json={"model": self.vision_model, "selfie": selfie,
                      "references": references, "liveness": liveness},
            )
            resp.raise_for_status()
            return resp.json()

    async def photo_assessment(self, image: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=90) as client:
            resp = await client.post(
                f"{self.api_base}/vision/photo-check",
                headers=self._headers(),
                json={"model": self.image_model, "image": image},
            )
            resp.raise_for_status()
            return resp.json()
