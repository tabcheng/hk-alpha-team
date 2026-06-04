from __future__ import annotations

from pathlib import Path

STATUS_DOC_PATH = Path(__file__).resolve().parents[2] / "docs" / "11-project-status.md"


def _extract_current_phase(lines: list[str]) -> str:
    for idx, line in enumerate(lines):
        if line.strip() == "## Current Phase" and idx + 2 < len(lines):
            return lines[idx + 2].strip().strip("*")
    return "Unknown"


def _extract_table_status(lines: list[str], row_id: str) -> str:
    for line in lines:
        row = line.strip()
        if row.startswith(f"| {row_id} |"):
            parts = [p.strip() for p in row.split("|") if p.strip()]
            if len(parts) >= 3:
                return parts[2]
    return "Unknown"


def _extract_milestone_status(lines: list[str], milestone: str = "M4") -> str:
    return _extract_table_status(lines, milestone)


def _extract_task_status(lines: list[str], task_ids: tuple[str, ...] = ("005", "006", "007")) -> dict[str, str]:
    return {task_id: _extract_table_status(lines, task_id) for task_id in task_ids}


def _current_milestone_id(phase: str) -> str:
    phase_to_milestone = {
        "Phase 1": "M1",
        "Phase 2": "M2",
        "Phase 3": "M3",
        "Phase 4": "M4",
        "Phase 5": "M5",
        "Phase 6": "M6",
        "Phase 7": "M7",
    }
    for phase_prefix, milestone_id in phase_to_milestone.items():
        if phase.startswith(phase_prefix):
            return milestone_id
    return "M4"


def _tracked_task_ids_for_phase(phase: str) -> tuple[str, ...]:
    if phase.startswith("Phase 5"):
        return ("005", "006", "007", "008")
    return ("005", "006", "007")


def read_project_status() -> dict[str, object]:
    if not STATUS_DOC_PATH.exists():
        return {
            "current_phase": "Unknown",
            "current_milestone": "Unknown",
            "task_status": {"005": "Unknown", "006": "Unknown", "007": "Unknown"},
        }

    lines = STATUS_DOC_PATH.read_text(encoding="utf-8").splitlines()
    phase = _extract_current_phase(lines)
    milestone_id = _current_milestone_id(phase)
    milestone_status = _extract_milestone_status(lines, milestone_id)
    task_status = _extract_task_status(lines, _tracked_task_ids_for_phase(phase))

    return {
        "current_phase": phase,
        "current_milestone": f"{milestone_id} ({milestone_status})",
        "task_status": task_status,
    }
