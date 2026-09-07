from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.patient import Patient
from app.models.bed import Bed
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/search", tags=["search"])

@router.get("")
def search(q: str="", db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    if len(q) < 2: return {"patients": [], "beds": []}
    patients = db.query(Patient).filter(Patient.patient_code.like(f"%{q.upper()}%")).limit(10).all()
    beds = db.query(Bed).filter(Bed.bed_code.like(f"%{q}%")).limit(10).all()
    return {
        "patients": [{"id": p.id, "patient_code": p.patient_code, "department": p.department} for p in patients],
        "beds": [{"id": b.id, "bed_code": b.bed_code, "department": b.department, "current_state": b.current_state} for b in beds]
    }
