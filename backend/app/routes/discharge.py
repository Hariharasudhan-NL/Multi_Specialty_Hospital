from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional
from app.database import get_db
from app.models.patient import Patient
from app.models.discharge import DischargeEvent, PatientExitEvent
from app.services.coordination_engine import get_patient_coordination_status
from app.services.audit_service import log_action
from app.routes.auth import get_current_user, require_role

router = APIRouter(prefix="/api/discharge", tags=["discharge"])

@router.get("/readiness")
def get_readiness(department: Optional[str]=None, db: Session=Depends(get_db),
                  current_user=Depends(get_current_user)):
    q = db.query(Patient).filter(Patient.status == "ADMITTED")
    if department: q = q.filter(Patient.department == department)
    patients = q.limit(200).all()
    result = []
    for p in patients:
        s = get_patient_coordination_status(p, db)
        de = s.get("discharge_event")
        ee = s.get("exit_event")
        ce = s.get("cleaning_event")
        result.append({
            "patient_id": p.id, "patient_code": p.patient_code,
            "department": p.department, "ward": p.ward, "bed_code": s.get("bed_code"),
            "readiness_state": s.get("readiness_state"),
            "freshness_status": s.get("freshness_status"),
            "time_since_update_minutes": s.get("time_since_update_minutes"),
            "discharge_order_status": de.order_status if de else None,
            "exit_status": ee.exit_status if ee else None,
            "cleaning_status": ce.cleaning_status if ce else None,
            "uncertainty": s.get("uncertainty"),
        })
    return result

@router.get("/{patient_id}")
def get_discharge(patient_id: int, db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    p = db.query(Patient).filter(Patient.id == patient_id).first()
    if not p: raise HTTPException(404, "Patient not found")
    log_action(db, current_user.id, current_user.email, "VIEW_PATIENT", "PATIENT", patient_id)
    s = get_patient_coordination_status(p, db)
    # Serialize datetime objects
    for key in ["discharge_event","exit_event","cleaning_event","bed_state"]:
        if s.get(key) and hasattr(s[key], '__dict__'):
            obj = s[key]
            s[key] = {k: (v.isoformat() if hasattr(v,'isoformat') else v)
                      for k, v in obj.__dict__.items() if not k.startswith('_')}
    if s.get("admission_time") and hasattr(s["admission_time"], 'isoformat'):
        s["admission_time"] = s["admission_time"].isoformat()
    return s

@router.post("/{patient_id}/confirm-readiness")
def confirm_readiness(patient_id: int, db: Session=Depends(get_db),
                      current_user=Depends(require_role("CLINICAL_STAFF","ADMIN"))):
    p = db.query(Patient).filter(Patient.id == patient_id).first()
    if not p: raise HTTPException(404, "Patient not found")
    now = datetime.now(timezone.utc)
    de = (db.query(DischargeEvent).filter(DischargeEvent.patient_id == patient_id,
          DischargeEvent.is_duplicate == False).order_by(DischargeEvent.event_time.desc()).first())
    if de:
        de.readiness_status = "READY_CONFIRMED"; de.confirmed_by = current_user.email; de.readiness_time = now
    else:
        de = DischargeEvent(patient_id=patient_id, readiness_status="READY_CONFIRMED",
                            confirmed_by=current_user.email, readiness_time=now,
                            event_time=now, received_time=now, quality_status="VALID", is_duplicate=False)
        db.add(de)
    db.commit()
    log_action(db, current_user.id, current_user.email, "CONFIRM_READINESS", "PATIENT", patient_id)
    return {"status": "READY_CONFIRMED", "confirmed_by": current_user.email, "time": now.isoformat()}

@router.post("/{patient_id}/update-order")
def update_order(patient_id: int, order_status: str="ORDERED",
                 db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    p = db.query(Patient).filter(Patient.id == patient_id).first()
    if not p: raise HTTPException(404, "Patient not found")
    de = (db.query(DischargeEvent).filter(DischargeEvent.patient_id == patient_id,
          DischargeEvent.is_duplicate == False).order_by(DischargeEvent.event_time.desc()).first())
    now = datetime.now(timezone.utc)
    if de: de.order_status = order_status; de.order_time = now
    db.commit()
    log_action(db, current_user.id, current_user.email, "UPDATE_DISCHARGE_ORDER", "PATIENT", patient_id)
    return {"status": order_status, "time": now.isoformat()}
