from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.patient import Patient
from app.services.coordination_engine import get_patient_coordination_status
from app.services.audit_service import log_action
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/patients", tags=["patients"])

@router.get("")
def list_patients(department: Optional[str]=None, status: Optional[str]="ADMITTED",
                  db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(Patient)
    if department: q = q.filter(Patient.department == department)
    if status: q = q.filter(Patient.status == status)
    patients = q.limit(300).all()
    result = []
    for p in patients:
        s = get_patient_coordination_status(p, db)
        result.append({
            "id": p.id, "patient_code": p.patient_code, "department": p.department,
            "ward": p.ward, "bed_code": s.get("bed_code"),
            "admission_time": p.admission_time.isoformat() if p.admission_time else None,
            "status": p.status, "readiness_state": s.get("readiness_state"),
            "freshness_status": s.get("freshness_status")
        })
    return result

@router.get("/{patient_id}")
def get_patient(patient_id: int, db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    p = db.query(Patient).filter(Patient.id == patient_id).first()
    if not p: raise HTTPException(404, "Patient not found")
    log_action(db, current_user.id, current_user.email, "VIEW_PATIENT", "PATIENT", patient_id)
    s = get_patient_coordination_status(p, db)
    for key in ["discharge_event","exit_event","cleaning_event","bed_state"]:
        if s.get(key) and hasattr(s[key], '__dict__'):
            obj = s[key]
            s[key] = {k: (v.isoformat() if hasattr(v,'isoformat') else v)
                      for k, v in obj.__dict__.items() if not k.startswith('_')}
    if s.get("admission_time") and hasattr(s["admission_time"], 'isoformat'):
        s["admission_time"] = s["admission_time"].isoformat()
    return s
