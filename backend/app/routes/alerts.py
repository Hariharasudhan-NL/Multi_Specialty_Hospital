from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.alert_service import get_active_alerts, resolve_alert
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.get("")
def list_alerts(db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    alerts = get_active_alerts(db, limit=100)
    return [{"id": a.id, "entity_type": a.entity_type, "entity_id": a.entity_id,
              "alert_type": a.alert_type, "severity": a.severity, "message": a.message,
              "created_at": a.created_at.isoformat() if a.created_at else None,
              "is_active": a.is_active} for a in alerts]

@router.post("/{alert_id}/resolve")
def resolve(alert_id: int, db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    a = resolve_alert(db, alert_id, current_user.email)
    if not a: raise HTTPException(404, "Alert not found")
    return {"status": "resolved"}
