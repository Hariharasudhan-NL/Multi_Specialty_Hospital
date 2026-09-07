from fastapi import APIRouter, Depends
from app.routes.auth import require_role
from app.services.demo_service import start_demo, pause_demo, reset_demo, get_demo_status, advance_step

router = APIRouter(prefix="/api/demo", tags=["demo"])

@router.post("/start")
def demo_start(speed: float=1.0, current_user=Depends(require_role("ADMIN"))):
    start_demo(speed); return get_demo_status()

@router.post("/pause")
def demo_pause(current_user=Depends(require_role("ADMIN"))):
    pause_demo(); return get_demo_status()

@router.post("/reset")
def demo_reset(current_user=Depends(require_role("ADMIN"))):
    reset_demo(); return get_demo_status()

@router.post("/advance")
def demo_advance(current_user=Depends(require_role("ADMIN"))):
    advance_step(); return get_demo_status()

@router.get("/status")
def demo_status(current_user=Depends(require_role("ADMIN"))):
    return get_demo_status()
