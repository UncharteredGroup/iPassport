"""Shared Pydantic models for requests, results, and packages."""

from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field

Decision = Literal["accept", "retake", "escalate"]


def new_id() -> str:
    return str(uuid4())


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class GuideChatRequest(BaseModel):
    session_id: str | None = None
    application_type: Literal["new", "renewal", "replacement", "minor"] = "new"
    messages: list[ChatMessage] = Field(default_factory=list)


class GuideChatResponse(BaseModel):
    session_id: str
    reply: str
    missing_fields: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    done: bool = False


class DocumentVerifyRequest(BaseModel):
    document_type: str
    image: str  # base64 data URL
    expected: dict[str, str] = Field(default_factory=dict)


class Region(BaseModel):
    label: str
    box: list[float]  # x, y, w, h (0..1)
    confidence: float


class Check(BaseModel):
    name: str
    passed: bool
    detail: str = ""


class DocumentVerifyResponse(BaseModel):
    evidence_id: str
    extracted: dict[str, str] = Field(default_factory=dict)
    regions: list[Region] = Field(default_factory=list)
    checks: list[Check] = Field(default_factory=list)
    quality_score: float = 0.0
    quality_issues: list[str] = Field(default_factory=list)
    decision: Decision = "escalate"


class LivenessEvent(BaseModel):
    prompt: str
    passed: bool


class FaceVerifyRequest(BaseModel):
    selfie: str
    references: list[str] = Field(default_factory=list)
    liveness_events: list[LivenessEvent] = Field(default_factory=list)


class FaceVerifyResponse(BaseModel):
    evidence_id: str
    match_score: float
    liveness_score: float
    indicators: list[str] = Field(default_factory=list)
    decision: Decision = "escalate"


class PhotoVerifyRequest(BaseModel):
    image: str


class PhotoVerifyResponse(BaseModel):
    evidence_id: str
    icao_checks: list[Check] = Field(default_factory=list)
    score: float = 0.0
    guidance: str = ""
    decision: Decision = "escalate"


class Applicant(BaseModel):
    surname: str
    given_names: str
    nin: str
    dob: str = ""
    sex: str = ""


class PackageRequest(BaseModel):
    session_id: str
    applicant: Applicant
    application_type: str = "new"
    evidence: dict[str, Any] = Field(default_factory=dict)
    payment_ref: str = "demo-pay-001"
    keep_evidence: bool = False


class PackageResponse(BaseModel):
    package_id: str
    risk_score: float
    summary: dict[str, Any] = Field(default_factory=dict)
    signature: str = ""
    audit_ref: str = ""


class StatusEvent(BaseModel):
    stage: str
    at: datetime


class StatusResponse(BaseModel):
    package_id: str
    stage: str
    history: list[StatusEvent] = Field(default_factory=list)


class EscalateRequest(BaseModel):
    package_id: str
    reason: str


class EscalateResponse(BaseModel):
    package_id: str
    queued: bool = True
    position: int = 1
