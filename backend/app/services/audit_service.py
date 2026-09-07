import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.audit import AuditLog

def log_action(db: Session, user_id, user_email: str, action: str, entity_type: str,
               entity_id=None, details: dict = None):
    try:
        entry = AuditLog(user_id=user_id, user_email=user_email, action=action,
                         entity_type=entity_type, entity_id=str(entity_id) if entity_id else None,
                         timestamp=datetime.now(timezone.utc),
                         details=json.dumps(details) if details else None)
        db.add(entry)
        db.commit()
    except Exception:
        db.rollback()

def get_audit_logs(db: Session, limit: int = 100, offset: int = 0) -> list:
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).offset(offset).limit(limit).all()
