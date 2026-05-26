from fastapi import FastAPI

from app.contracts import success_envelope

app = FastAPI(title="HK Alpha Team Backend", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return success_envelope({"service": "ok"})


@app.get("/api/v1/project-status")
def project_status() -> dict:
    return success_envelope(
        {
            "current_phase": "Phase 3 — Backend Skeleton",
            "current_milestone": "M3",
            "task_status": {
                "005": "Completed",
                "006": "In Progress",
            },
        }
    )
