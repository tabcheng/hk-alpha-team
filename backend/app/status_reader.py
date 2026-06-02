from __future__ import annotations

from pathlib import Path

STATUS_DOC_PATH = Path(__file__).resolve().parents[2] / "docs" / "11-project-status.md"


def _extract_current_phase(lines: list[str]) -> str:
    for idx, line in enumerate(lines):
        if line.strip() == "## Current Phase" and idx + 2 < len(lines):
            return lines[idx + 2].strip().strip("*")
    return "Unknown"


def _extract_milestone_status(lines: list[str], milestone: str = "M4") -> str:
    for line in lines:
        row = line.strip()
        if row.startswith(f"| {milestone} |"):
            parts = [p.strip() for p in row.split("|") if p.strip()]
            if len(parts) >= 3:
                return parts[2]
    return "Unknown"


def _extract_task_status(lines: list[str], task_ids: tuple[str, ...] = ("005", "006", "007")) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for task_id in task_ids:
        statuses[task_id] = "Unknown"
        for line in lines:
            row = line.strip()
            if row.startswith(f"| {task_id} |"):
                parts = [p.strip() for p in row.split("|") if p.strip()]
                if len(parts) >= 3:
                    statuses[task_id] = parts[2]
                break
    return statuses


def read_project_status() -> dict[str, object]:
    if not STATUS_DOC_PATH.exists():
        return {
            "current_phase": "Unknown",
            "current_milestone": "Unknown",
            "task_status": {"005": "Unknown", "006": "Unknown", "007": "Unknown"},
        }

    lines = STATUS_DOC_PATH.read_text(encoding="utf-8").splitlines()
    phase = _extract_current_phase(lines)
    milestone_status = _extract_milestone_status(lines, "M4")
    task_status = _extract_task_status(lines, ("005", "006", "007"))

    return {
        "current_phase": phase,
        "current_milestone": f"M4 ({milestone_status})",
        "task_status": task_status,
    }
