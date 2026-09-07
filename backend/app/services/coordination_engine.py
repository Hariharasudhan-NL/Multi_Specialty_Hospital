from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.services.readiness_engine import ReadinessState, determine_readiness_state
from app.services.freshness_engine import get_freshness_status
from app.services.data_quality_engine import DataQualityEngine
from app.models.patient import Patient
from app.models.discharge import DischargeEvent, PatientExitEvent
from app.models.bed import Bed, CleaningEvent, BedStateEvent
from app.config import settings

def get_patient_coordination_status(patient: Patient, db: Session) -> dict:
    now = datetime.now(timezone.utc)
    discharge_event = (db.query(DischargeEvent)
        .filter(DischargeEvent.patient_id == patient.id, DischargeEvent.is_duplicate == False)
        .order_by(DischargeEvent.event_time.desc()).first())
    exit_event = (db.query(PatientExitEvent)
        .filter(PatientExitEvent.patient_id == patient.id)
        .order_by(PatientExitEvent.event_time.desc()).first())
    bed = db.query(Bed).filter(Bed.id == patient.bed_id).first() if patient.bed_id else None
    cleaning_event = None
    latest_bed_state = None
    if bed:
        cleaning_event = (db.query(CleaningEvent).filter(CleaningEvent.bed_id == bed.id)
            .order_by(CleaningEvent.event_time.desc()).first())
        latest_bed_state = (db.query(BedStateEvent).filter(BedStateEvent.bed_id == bed.id)
            .order_by(BedStateEvent.event_time.desc()).first())
    data_stale = False
    if bed and bed.last_updated:
        lu = bed.last_updated
        if lu.tzinfo is None: lu = lu.replace(tzinfo=timezone.utc)
        mins = (now - lu).total_seconds() / 60
        if mins > settings.stale_threshold_minutes:
            data_stale = True
    conflict = False
    if cleaning_event and latest_bed_state:
        conflict = DataQualityEngine.check_bed_conflict(cleaning_event.cleaning_status, latest_bed_state.state)
    state = determine_readiness_state(discharge_event, exit_event, cleaning_event,
                                       latest_bed_state, data_stale, conflict)
    ref_time = discharge_event.event_time if discharge_event else None
    freshness_status, time_since = get_freshness_status(ref_time, now)
    uncertainty = _build_uncertainty(state, time_since)
    return {
        "patient_id": patient.id, "patient_code": patient.patient_code,
        "department": patient.department, "ward": patient.ward,
        "bed_id": patient.bed_id, "bed_code": bed.bed_code if bed else None,
        "readiness_state": state.value, "admission_time": patient.admission_time, "status": patient.status,
        "discharge_event": discharge_event, "exit_event": exit_event,
        "cleaning_event": cleaning_event, "bed_state": latest_bed_state,
        "freshness_status": freshness_status,
        "time_since_update_minutes": round(time_since, 1) if time_since is not None else None,
        "data_stale": data_stale, "conflict": conflict, "uncertainty": uncertainty,
    }

def _build_uncertainty(state: ReadinessState, time_since) -> dict:
    if state == ReadinessState.ORDER_PENDING:
        return {"has_uncertainty": True, "reason": "ORDER PENDING",
                "message": "Clinical readiness is confirmed, but no discharge order event has been received.",
                "recommended_action": "Contact responsible clinical staff to issue discharge order."}
    if state == ReadinessState.DATA_STALE:
        mins = round(time_since or 0)
        return {"has_uncertainty": True, "reason": "AVAILABILITY UNCERTAIN",
                "message": f"Last bed-state update was {mins} minutes ago. Verify with authorized ward staff.",
                "recommended_action": "Request fresh bed status update from ward staff."}
    if state == ReadinessState.CONFLICT:
        return {"has_uncertainty": True, "reason": "CONFLICTING DATA",
                "message": "Cleaning system reports COMPLETE, but bed-state system reports OCCUPIED.",
                "recommended_action": "Do not mark bed available. Verify with housekeeping and ward staff."}
    if state == ReadinessState.DATA_MISSING:
        return {"has_uncertainty": True, "reason": "MISSING DATA",
                "message": "Discharge readiness event has not been received for this patient.",
                "recommended_action": "Verify patient discharge readiness with clinical staff."}
    return {"has_uncertainty": False, "reason": None, "message": None, "recommended_action": None}
