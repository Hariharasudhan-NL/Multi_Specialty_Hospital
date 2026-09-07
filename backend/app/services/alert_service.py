from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.alert import Alert

def create_alert(db: Session, entity_type: str, entity_id: str, alert_type: str, severity: str, message: str) -> Alert:
    alert = Alert(entity_type=entity_type, entity_id=str(entity_id), alert_type=alert_type,
                  severity=severity, message=message, created_at=datetime.now(timezone.utc), is_active=True)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def resolve_alert(db: Session, alert_id: int, resolved_by: str) -> Alert:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.resolved_at = datetime.now(timezone.utc)
        alert.resolved_by = resolved_by
        alert.is_active = False
        db.commit()
        db.refresh(alert)
    return alert

def get_active_alerts(db: Session, limit: int = 100) -> list:
    return db.query(Alert).filter(Alert.is_active == True).order_by(Alert.created_at.desc()).limit(limit).all()

def get_alert_count(db: Session) -> int:
    return db.query(Alert).filter(Alert.is_active == True).count()
