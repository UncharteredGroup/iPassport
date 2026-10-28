"""Append-only in-memory audit log (persist to DB in production)."""

from datetime import UTC, datetime
from typing import Any


class AuditLog:
    def __init__(self) -> None:
        self._entries: list[dict[str, Any]] = []

    def record(self, kind: str, ref: str, detail: dict[str, Any]) -> str:
        entry = {"at": datetime.now(UTC).isoformat(), "kind": kind,
                 "ref": ref, "detail": detail}
        self._entries.append(entry)
        return f"audit-{len(self._entries):06d}"

    def for_ref(self, ref: str) -> list[dict[str, Any]]:
        return [e for e in self._entries if e["ref"] == ref]


audit = AuditLog()
