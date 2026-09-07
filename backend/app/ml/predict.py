import json
from pathlib import Path
from typing import Optional
import pandas as pd

MODELS_DIR = Path(__file__).parent / "models"
_xgb = None

def _load():
    global _xgb
    if _xgb is None:
        p = MODELS_DIR / "xgboost.joblib"
        if p.exists():
            import joblib
            _xgb = joblib.load(p)
    return _xgb

def get_metrics() -> dict:
    p = MODELS_DIR / "metrics.json"
    if p.exists():
        with open(p) as f: return json.load(f)
    return {"error": "Models not trained. Run: python app/ml/train.py"}

def predict_bed_availability(department: str="General Medicine", bed_type: str="GENERAL",
                              readiness_to_order_minutes: Optional[float]=None,
                              order_to_exit_minutes: Optional[float]=None,
                              cleaning_duration_minutes: Optional[float]=None,
                              data_quality_score: float=1.0, event_delay_flag: int=0,
                              hour_of_day: int=12, day_of_week: int=0) -> dict:
    if data_quality_score < 0.5:
        return {"estimated_minutes": None, "confidence": "LOW", "model": "unavailable",
                "prediction_type": "Operational estimate", "is_available": False,
                "uncertainty_reason": "Prediction unavailable — insufficient fresh data."}
    model = _load()
    r2o = readiness_to_order_minutes or 30
    o2e = order_to_exit_minutes or 60
    clean = cleaning_duration_minutes or 35
    if model is None:
        est = int(max(1, r2o + o2e + clean))
        return {"estimated_minutes": est, "confidence": "LOW", "model": "rule_based_fallback",
                "prediction_type": "Operational estimate", "is_available": est <= 5,
                "uncertainty_reason": "ML model not trained. Using rule-based estimate."}
    from app.ml.features import engineer_features
    row = pd.DataFrame([{"department": department, "bed_type": bed_type, "hour_of_day": hour_of_day,
                          "day_of_week": day_of_week, "readiness_to_order_minutes": r2o,
                          "order_to_exit_minutes": o2e, "cleaning_duration_minutes": clean,
                          "data_quality_score": data_quality_score, "event_delay_flag": event_delay_flag}])
    pred = float(model.predict(engineer_features(row))[0])
    conf = "HIGH" if data_quality_score > 0.9 and not event_delay_flag else ("MEDIUM" if data_quality_score > 0.7 else "LOW")
    return {"estimated_minutes": max(1, int(pred)), "confidence": conf, "model": "xgboost",
            "prediction_type": "Operational estimate", "is_available": pred <= 5, "uncertainty_reason": None}
