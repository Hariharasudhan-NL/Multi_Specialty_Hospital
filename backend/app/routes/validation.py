from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone
from app.database import get_db
from app.models.validation import StakeholderValidation
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/validation", tags=["validation"])

@router.post("/submit")
def submit(q1: int, q2: int, q3: int, q4: int, q5: int, q6: int,
           comments: str="", db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    v = StakeholderValidation(role=current_user.role, q1_bed_status=q1, q2_stale_info=q2,
                               q3_unavailability_reason=q3, q4_evidence=q4, q5_coordination_help=q5,
                               q6_would_use=q6, comments=comments, submitted_at=datetime.now(timezone.utc))
    db.add(v); db.commit()
    return {"status": "submitted"}

@router.get("/results")
def get_results(db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    total = db.query(StakeholderValidation).count()
    if total == 0:
        return {"total_responses": 0, "averages": {},
                "disclaimer": "Prototype stakeholder validation only. Not clinical validation."}
    avgs = db.query(
        func.avg(StakeholderValidation.q1_bed_status),
        func.avg(StakeholderValidation.q2_stale_info),
        func.avg(StakeholderValidation.q3_unavailability_reason),
        func.avg(StakeholderValidation.q4_evidence),
        func.avg(StakeholderValidation.q5_coordination_help),
        func.avg(StakeholderValidation.q6_would_use)).first()
    return {
        "total_responses": total,
        "disclaimer": "Prototype stakeholder validation only. Not clinical validation.",
        "averages": {
            "q1_bed_status": round(avgs[0] or 0, 2), "q2_stale_info": round(avgs[1] or 0, 2),
            "q3_unavailability_reason": round(avgs[2] or 0, 2), "q4_evidence": round(avgs[3] or 0, 2),
            "q5_coordination_help": round(avgs[4] or 0, 2), "q6_would_use": round(avgs[5] or 0, 2)}
    }
