from fastapi import APIRouter
import time

router = APIRouter(tags=["health"])

start_time = time.time()

@router.get("/health")
def health_check():
    """General health check endpoint."""
    return {"status": "ok", "uptime_seconds": time.time() - start_time}

@router.get("/live")
def liveness_probe():
    """Liveness probe for orchestrator (e.g. Kubernetes). Returns 200 if app is running."""
    return {"status": "alive"}

@router.get("/ready")
def readiness_probe():
    """Readiness probe. Checks if the app is ready to accept traffic (e.g. DB is connected)."""
    # For Sprint 6 foundation, we assume it's ready. In production, we'd check DB ping.
    return {"status": "ready"}
