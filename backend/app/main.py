from fastapi import FastAPI

from app.contracts import success_envelope
from app.status_reader import read_project_status

app = FastAPI(title="HK Alpha Team Backend", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return success_envelope({"service": "ok"})


@app.get("/api/v1/project-status")
def project_status() -> dict:
    return success_envelope(read_project_status())
