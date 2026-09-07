from datetime import datetime, timezone, timedelta
from typing import Optional

class DataQualityEngine:
    DUPLICATE_WINDOW_MINUTES = 5
    DELAY_THRESHOLD_MINUTES = 60

    @staticmethod
    def check_future_timestamp(event_time: datetime) -> bool:
        now = datetime.now(timezone.utc)
        if event_time.tzinfo is None:
            event_time = event_time.replace(tzinfo=timezone.utc)
        return event_time > now + timedelta(minutes=1)

    @staticmethod
    def check_delayed(event_time: datetime, received_time: datetime) -> bool:
        if event_time.tzinfo is None:
            event_time = event_time.replace(tzinfo=timezone.utc)
        if received_time.tzinfo is None:
            received_time = received_time.replace(tzinfo=timezone.utc)
        return (received_time - event_time).total_seconds() / 60 > DataQualityEngine.DELAY_THRESHOLD_MINUTES

    @staticmethod
    def get_quality_status(event_time: datetime, received_time: datetime, is_duplicate: bool = False) -> str:
        if DataQualityEngine.check_future_timestamp(event_time):
            return "INVALID"
        if is_duplicate:
            return "DUPLICATE"
        if DataQualityEngine.check_delayed(event_time, received_time):
            return "DELAYED"
        return "VALID"

    @staticmethod
    def check_bed_conflict(cleaning_status: Optional[str], bed_state: Optional[str]) -> bool:
        return cleaning_status == "COMPLETED" and bed_state == "OCCUPIED"

    @staticmethod
    def get_summary(db) -> dict:
        from app.models.discharge import DischargeEvent, PatientExitEvent
        from app.models.bed import BedStateEvent, CleaningEvent
        all_events = []
        for e in db.query(DischargeEvent).all(): all_events.append(e.quality_status)
        for e in db.query(PatientExitEvent).all(): all_events.append(e.quality_status)
        for e in db.query(BedStateEvent).all(): all_events.append(e.quality_status)
        for e in db.query(CleaningEvent).all(): all_events.append(e.quality_status)
        total = len(all_events)
        if total == 0:
            return {"total": 0, "valid": 0, "missing": 0, "stale": 0, "duplicate": 0,
                    "invalid": 0, "conflict": 0, "delayed": 0, "uncertain": 0, "quality_pct": 100.0}
        counts = {s.lower(): sum(1 for e in all_events if e == s)
                  for s in ["VALID","MISSING","STALE","DUPLICATE","INVALID","CONFLICT","DELAYED","UNCERTAIN"]}
        valid_pct = round((counts["valid"] / total) * 100, 1)
        return {"total": total, **counts, "quality_pct": valid_pct}
