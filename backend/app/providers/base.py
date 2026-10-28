"""Abstract provider: every model call the backend needs lives here."""

from abc import ABC, abstractmethod
from typing import Any


class Provider(ABC):
    name: str = "base"

    @abstractmethod
    async def agent_turn(
        self, application_type: str, messages: list[dict[str, str]]
    ) -> dict[str, Any]:
        """One agentic guidance turn. Returns reply/missing_fields/next_actions."""

    @abstractmethod
    async def segment_document(
        self, document_type: str, image: str
    ) -> dict[str, Any]:
        """SAM-style segmentation + extraction. Returns regions/extracted/quality."""

    @abstractmethod
    async def face_scores(
        self, selfie: str, references: list[str], liveness: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Face match + liveness. Returns match/liveness scores + indicators."""

    @abstractmethod
    async def photo_assessment(self, image: str) -> dict[str, Any]:
        """Passport-photo ICAO assessment. Returns checks/score/guidance."""
