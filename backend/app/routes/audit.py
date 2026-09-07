from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.audit_service import get_audit_logs
from app.routes.auth import require_role

router = APIRouter(prefix="/api/audit", tags=["audit"])

@router.get("")
def list_audit(skip: int=0, limit: int=100, db: Session=Depends(get_db),
               current_user=Depends(require_role("ADMIN"))):
    logs = get_audit_logs(db, limit=limit, offset=skip)
    return [{"id": l.id, "user_email": l.user_email, "action": l.action,
              "entity_type": l.entity_type, "entity_id": l.entity_id,
              "timestamp": l.timestamp.isoformat() if l.timestamp else None,
              "details": l.details} for l in logs]
