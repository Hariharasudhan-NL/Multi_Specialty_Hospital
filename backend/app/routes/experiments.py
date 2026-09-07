from fastapi import APIRouter, Depends
from app.routes.auth import get_current_user
import json, os

router = APIRouter(prefix="/api/experiments", tags=["experiments"])
RESULTS_PATH = os.path.join(os.path.dirname(__file__), "../../../experiments/results/evaluation_report.json")

def _load():
    try:
        if os.path.exists(RESULTS_PATH):
            with open(RESULTS_PATH) as f: return json.load(f)
    except Exception: pass
    return None

@router.get("/baseline")
def get_baseline(current_user=Depends(get_current_user)):
    r = _load()
    return r["baseline"] if r else {"error": "Run: cd experiments && python evaluation.py"}

@router.get("/prototype")
def get_prototype(current_user=Depends(get_current_user)):
    r = _load()
    return r["prototype"] if r else {"error": "Run: cd experiments && python evaluation.py"}

@router.get("/comparison")
def get_comparison(current_user=Depends(get_current_user)):
    r = _load()
    if not r: return {"error": "Run: cd experiments && python evaluation.py"}
    return {
        "baseline_mean": r.get("baseline",{}).get("mean_minutes"),
        "baseline_median": r.get("baseline",{}).get("median_minutes"),
        "baseline_p90": r.get("baseline",{}).get("p90_minutes"),
        "prototype_mean": r.get("prototype",{}).get("mean_minutes"),
        "prototype_median": r.get("prototype",{}).get("median_minutes"),
        "prototype_p90": r.get("prototype",{}).get("p90_minutes"),
        "absolute_improvement_mean": r.get("absolute_improvement_mean"),
        "percentage_improvement": r.get("percentage_improvement"),
        "target_percentage": r.get("target_percentage"),
        "target_achieved": r.get("target_achieved"),
        "target_assessment": r.get("target_assessment"),
    }

@router.get("/error-analysis")
def get_error_analysis(current_user=Depends(get_current_user)):
    from app.ml.predict import get_metrics
    return {"ml_metrics": get_metrics(), "note": "Synthetic simulation. Not clinical data."}
