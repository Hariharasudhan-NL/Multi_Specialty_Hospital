from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/theatre", tags=["theatre"])

DEPTS = ["Cardiology","Neurology","Orthopedics","General Surgery","ENT","Gastroenterology","Urology","General Medicine"]

@router.get("")
def list_theatres(db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    now = datetime.now(timezone.utc).isoformat()
    theatres = []
    for i, dept in enumerate(DEPTS):
        for j in range(1, 3):
            theatres.append({
                "id": i*2+j, "theatre_code": f"TH-{dept[:3].upper()}-{j:02d}",
                "department": dept,
                "current_status": "AVAILABLE" if j == 2 else "IN_USE",
                "current_case_status": "NONE" if j == 2 else "IN_PROGRESS",
                "next_scheduled_department": dept,
                "expected_turnover_minutes": 45,
                "cleaning_status": "COMPLETE",
                "delay_minutes": 0,
                "last_updated": now,
                "disclaimer": "Operational coordination only. No surgical/clinical decisions."
            })
    return theatres
