from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timezone
from app.database import get_db
from app.models.bed import Bed, CleaningEvent, BedStateEvent
from app.models.patient import Patient
from app.services.freshness_engine import get_freshness_status
from app.routes.auth import get_current_user, require_role

router = APIRouter(prefix="/api/beds", tags=["beds"])

def _bed_dict(b: Bed, db: Session, now: datetime) -> dict:
    lu = b.last_updated
    if lu and lu.tzinfo is None: lu = lu.replace(tzinfo=timezone.utc)
    freshness, time_since = get_freshness_status(lu, now)
    patient = db.query(Patient).filter(Patient.bed_id == b.id, Patient.status == "ADMITTED").first()
    cleaning = db.query(CleaningEvent).filter(CleaningEvent.bed_id == b.id).order_by(CleaningEvent.event_time.desc()).first()
    return {
        "id": b.id, "bed_code": b.bed_code, "department": b.department, "ward": b.ward,
        "bed_type": b.bed_type, "current_state": b.current_state,
        "last_updated": lu.isoformat() if lu else None,
        "freshness_status": freshness,
        "time_since_update_minutes": round(time_since, 1) if time_since is not None else None,
        "patient_id": patient.id if patient else None,
        "patient_code": patient.patient_code if patient else None,
        "cleaning_status": cleaning.cleaning_status if cleaning else None,
    }

@router.get("")
def list_beds(department: Optional[str]=None, ward: Optional[str]=None,
             state: Optional[str]=None, freshness: Optional[str]=None,
             db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    q = db.query(Bed).filter(Bed.is_active == True)
    if department: q = q.filter(Bed.department == department)
    if ward: q = q.filter(Bed.ward == ward)
    if state: q = q.filter(Bed.current_state == state)
    beds = q.limit(500).all()
    result = [_bed_dict(b, db, now) for b in beds]
    if freshness: result = [r for r in result if r["freshness_status"] == freshness]
    return result

@router.get("/{bed_id}")
def get_bed(bed_id: int, db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    b = db.query(Bed).filter(Bed.id == bed_id).first()
    if not b: raise HTTPException(404, "Bed not found")
    now = datetime.now(timezone.utc)
    d = _bed_dict(b, db, now)
    history = (db.query(BedStateEvent).filter(BedStateEvent.bed_id == bed_id)
               .order_by(BedStateEvent.event_time.desc()).limit(20).all())
    d["state_history"] = [{"state": h.state, "event_time": h.event_time.isoformat() if h.event_time else None,
                            "quality_status": h.quality_status} for h in history]
    return d

@router.put("/{bed_id}/state")
def update_state(bed_id: int, state: str, db: Session=Depends(get_db),
                 current_user=Depends(require_role("BED_MANAGER","ADMIN"))):
    b = db.query(Bed).filter(Bed.id == bed_id).first()
    if not b: raise HTTPException(404, "Bed not found")
    b.current_state = state; b.last_updated = datetime.now(timezone.utc)
    db.commit()
    return {"msg": "updated", "new_state": state}
