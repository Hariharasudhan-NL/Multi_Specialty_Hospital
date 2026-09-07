from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.models.bed import Bed, BedStateEvent, CleaningEvent
from app.models.discharge import DischargeEvent, PatientExitEvent
from app.models.patient import Patient

def inject_missing_discharge_order(db: Session) -> dict:
    patient = db.query(Patient).filter(Patient.status == "ADMITTED").first()
    if not patient:
        return {"error": "No admitted patients found"}
    now = datetime.now(timezone.utc)
    existing = db.query(DischargeEvent).filter(DischargeEvent.patient_id == patient.id).first()
    if existing:
        existing.readiness_status = "READY_CONFIRMED"
        existing.confirmed_by = "doctor@hospital.local"
        existing.readiness_time = now
        existing.order_status = None
        existing.order_time = None
    else:
        de = DischargeEvent(patient_id=patient.id, readiness_status="READY_CONFIRMED",
                            confirmed_by="doctor@hospital.local", readiness_time=now,
                            order_status=None, event_time=now, received_time=now,
                            quality_status="VALID", is_duplicate=False)
        db.add(de)
    db.commit()
    return {"patient_code": patient.patient_code, "state": "READY_CONFIRMED", "order": None,
            "expected": "ORDER_PENDING", "description": "Readiness confirmed but no discharge order"}

def inject_stale_bed_data(db: Session) -> dict:
    bed = db.query(Bed).filter(Bed.current_state == "OCCUPIED").first()
    if not bed:
        bed = db.query(Bed).first()
    bed.last_updated = datetime.now(timezone.utc) - timedelta(hours=1, minutes=10)
    db.commit()
    return {"bed_code": bed.bed_code, "last_updated": bed.last_updated.isoformat(),
            "expected": "DATA_STALE", "description": "Bed last_updated set to 70 minutes ago"}

def inject_conflicting_bed_state(db: Session) -> dict:
    bed = db.query(Bed).first()
    now = datetime.now(timezone.utc)
    ce = CleaningEvent(bed_id=bed.id, cleaning_status="COMPLETED",
                       started_at=now - timedelta(minutes=40),
                       completed_at=now - timedelta(minutes=10),
                       quality_status="VALID", event_time=now - timedelta(minutes=40),
                       received_time=now - timedelta(minutes=38))
    db.add(ce)
    bse = BedStateEvent(bed_id=bed.id, state="OCCUPIED",
                        event_time=now - timedelta(minutes=5), received_time=now - timedelta(minutes=4),
                        source="BED_MANAGEMENT_SYSTEM", quality_status="CONFLICT", is_duplicate=False)
    db.add(bse)
    bed.current_state = "CONFLICT"
    bed.last_updated = now
    db.commit()
    return {"bed_code": bed.bed_code, "cleaning": "COMPLETED", "bed_state": "OCCUPIED",
            "expected": "CONFLICT", "description": "Cleaning complete but bed reports OCCUPIED"}

def inject_duplicate_event(db: Session) -> dict:
    patient = db.query(Patient).filter(Patient.status == "ADMITTED").first()
    if not patient: return {"error": "No admitted patients found"}
    now = datetime.now(timezone.utc)
    orig = db.query(DischargeEvent).filter(DischargeEvent.patient_id == patient.id).first()
    if not orig:
        orig = DischargeEvent(patient_id=patient.id, readiness_status="POSSIBLY_READY",
                              event_time=now, received_time=now, quality_status="VALID", is_duplicate=False)
        db.add(orig)
        db.flush()
    dup = DischargeEvent(patient_id=patient.id, readiness_status=orig.readiness_status,
                         event_time=orig.event_time, received_time=now + timedelta(minutes=2),
                         quality_status="DUPLICATE", is_duplicate=True,
                         confirmed_by=orig.confirmed_by, order_status=orig.order_status)
    db.add(dup)
    db.commit()
    return {"patient_code": patient.patient_code, "expected": "DUPLICATE detected",
            "description": "Same event inserted twice within 5 minutes"}

def inject_invalid_timestamp(db: Session) -> dict:
    bed = db.query(Bed).first()
    future = datetime.now(timezone.utc) + timedelta(hours=2)
    bse = BedStateEvent(bed_id=bed.id, state="AVAILABLE", event_time=future,
                        received_time=datetime.now(timezone.utc), source="TEST",
                        quality_status="INVALID", is_duplicate=False)
    db.add(bse)
    db.commit()
    return {"bed_code": bed.bed_code, "event_time": future.isoformat(),
            "expected": "INVALID", "description": "Event timestamp is 2 hours in the future"}

def inject_delayed_event(db: Session) -> dict:
    patient = db.query(Patient).filter(Patient.status == "ADMITTED").first()
    if not patient: return {"error": "No admitted patients found"}
    event_time = datetime.now(timezone.utc) - timedelta(hours=2)
    received_time = datetime.now(timezone.utc)
    de = DischargeEvent(patient_id=patient.id, readiness_status="POSSIBLY_READY",
                        event_time=event_time, received_time=received_time,
                        quality_status="DELAYED", is_duplicate=False)
    db.add(de)
    db.commit()
    return {"patient_code": patient.patient_code, "event_time": event_time.isoformat(),
            "received_time": received_time.isoformat(),
            "expected": "DELAYED", "description": "Event received 120 minutes after event_time"}

def reset_scenario(db: Session) -> dict:
    db.query(DischargeEvent).filter(DischargeEvent.quality_status.in_(["DUPLICATE","DELAYED","INVALID"])).delete()
    db.query(BedStateEvent).filter(BedStateEvent.quality_status.in_(["CONFLICT","INVALID"])).delete()
    beds = db.query(Bed).filter(Bed.current_state == "CONFLICT").all()
    for b in beds:
        b.current_state = "OCCUPIED"
        from datetime import timezone
        b.last_updated = datetime.now(timezone.utc)
    db.commit()
    return {"status": "reset", "message": "All injected failure scenarios removed"}

def get_scenario_status(db: Session) -> dict:
    from datetime import timedelta
    scenarios = {}
    missing = db.query(DischargeEvent).filter(
        DischargeEvent.readiness_status == "READY_CONFIRMED",
        DischargeEvent.order_status == None, DischargeEvent.is_duplicate == False).count()
    if missing > 0:
        scenarios["MISSING_DISCHARGE_ORDER"] = {
            "active": True, "expected_behavior": "STATE = ORDER_PENDING with uncertainty banner",
            "description": f"{missing} patient(s) with confirmed readiness but no discharge order"}
    stale_cutoff = datetime.now(timezone.utc) - timedelta(minutes=30)
    stale = db.query(Bed).filter(Bed.last_updated < stale_cutoff).count()
    if stale > 0:
        scenarios["STALE_BED_DATA"] = {
            "active": True, "expected_behavior": "STATE = DATA_STALE",
            "description": f"{stale} bed(s) with data older than 30 minutes"}
    conflicts = db.query(Bed).filter(Bed.current_state == "CONFLICT").count()
    if conflicts > 0:
        scenarios["CONFLICT"] = {
            "active": True, "expected_behavior": "STATE = CONFLICT, bed not marked available",
            "description": f"{conflicts} bed(s) in CONFLICT state"}
    duplicates = db.query(DischargeEvent).filter(DischargeEvent.is_duplicate == True).count()
    if duplicates > 0:
        scenarios["DUPLICATE_EVENT"] = {
            "active": True, "expected_behavior": "DUPLICATE flagged, original kept",
            "description": f"{duplicates} duplicate event(s) present"}
    invalid = db.query(BedStateEvent).filter(BedStateEvent.quality_status == "INVALID").count()
    if invalid > 0:
        scenarios["INVALID_TIMESTAMP"] = {
            "active": True, "expected_behavior": "quality_status = INVALID",
            "description": f"{invalid} event(s) with invalid (future) timestamps"}
    delayed = db.query(DischargeEvent).filter(DischargeEvent.quality_status == "DELAYED").count()
    if delayed > 0:
        scenarios["DELAYED_EVENT"] = {
            "active": True, "expected_behavior": "quality_status = DELAYED",
            "description": f"{delayed} delayed event(s) present"}
    return {"active_scenarios": list(scenarios.keys()), "scenario_details": scenarios}
