from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

SCHEMA_VERSION = "v0.1"
SOURCE = "HK_ALPHA_TEAM"


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _metadata() -> dict[str, str]:
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_timestamp(),
        "source": SOURCE,
    }


def success_envelope(data: dict[str, Any], warnings: list[str] | None = None) -> dict[str, Any]:
    return {
        "request_id": str(uuid4()),
        "status": "success",
        "data": data,
        "metadata": _metadata(),
        "warnings": warnings or [],
    }


def error_envelope(code: str, message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "request_id": str(uuid4()),
        "status": "error",
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        },
    }
