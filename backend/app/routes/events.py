from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.discharge import DischargeEvent
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/events", tags=["events"])

@router.get("")
def list_events(skip: int=0, limit: int=50, db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    events = db.query(DischargeEvent).order_by(DischargeEvent.event_time.desc()).offset(skip).limit(limit).all()
    return [{"id": e.id, "patient_id": e.patient_id, "readiness_status": e.readiness_status,
              "order_status": e.order_status,
              "event_time": e.event_time.isoformat() if e.event_time else None,
              "quality_status": e.quality_status, "is_duplicate": e.is_duplicate} for e in events]
