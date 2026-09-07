from datetime import datetime, timezone


def _utc(dt: datetime) -> datetime:
    """Ensure datetime is UTC-aware. SQLite returns naive datetimes — treat them as UTC."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def get_freshness_status(event_time: datetime, now: datetime = None):
    if not event_time:
        return "MISSING", None
    if not now:
        now = datetime.now(timezone.utc)
    event_time = _utc(event_time)
    now = _utc(now)
    diff = (now - event_time).total_seconds() / 60.0
    if diff < 15:
        return "FRESH", diff
    elif diff <= 30:
        return "AGING", diff
    else:
        return "STALE", diff
