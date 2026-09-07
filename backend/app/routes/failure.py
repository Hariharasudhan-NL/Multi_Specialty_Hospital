from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.failure_service import (
    inject_missing_discharge_order, inject_stale_bed_data, inject_conflicting_bed_state,
    inject_duplicate_event, inject_invalid_timestamp, inject_delayed_event,
    reset_scenario, get_scenario_status)
from app.routes.auth import require_role

router = APIRouter(prefix="/api/failure", tags=["failure"])

@router.post("/missing-order")
def missing_order(db: Session=Depends(get_db), current_user=Depends(require_role("ADMIN"))):
    return inject_missing_discharge_order(db)

@router.post("/stale-bed")
def stale_bed(db: Session=Depends(get_db), current_user=Depends(require_role("ADMIN"))):
    return inject_stale_bed_data(db)

@router.post("/conflict")
def conflict(db: Session=Depends(get_db), current_user=Depends(require_role("ADMIN"))):
    return inject_conflicting_bed_state(db)

@router.post("/duplicate-event")
def duplicate(db: Session=Depends(get_db), current_user=Depends(require_role("ADMIN"))):
    return inject_duplicate_event(db)

@router.post("/invalid-timestamp")
def invalid_ts(db: Session=Depends(get_db), current_user=Depends(require_role("ADMIN"))):
    return inject_invalid_timestamp(db)

@router.post("/delayed-event")
def delayed(db: Session=Depends(get_db), current_user=Depends(require_role("ADMIN"))):
    return inject_delayed_event(db)

@router.post("/reset")
def reset(db: Session=Depends(get_db), current_user=Depends(require_role("ADMIN"))):
    return reset_scenario(db)

@router.get("/status")
def status(db: Session=Depends(get_db), current_user=Depends(require_role("ADMIN"))):
    return get_scenario_status(db)
