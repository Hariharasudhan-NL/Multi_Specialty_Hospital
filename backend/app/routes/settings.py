from fastapi import APIRouter, Depends
from app.config import settings
from app.routes.auth import require_role

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("")
def get_settings(current_user=Depends(require_role("ADMIN"))):
    return {
        "freshness_threshold_minutes": settings.freshness_threshold_minutes,
        "stale_threshold_minutes": settings.stale_threshold_minutes,
        "target_improvement_percentage": settings.target_improvement_percentage,
        "simulation_speed": settings.simulation_speed,
        "prediction_confidence_threshold": settings.prediction_confidence_threshold,
    }
