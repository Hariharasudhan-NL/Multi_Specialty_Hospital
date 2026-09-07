import os, sys, json
import numpy as np
import pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib
from app.ml.features import engineer_features, DEPT_MAP, BED_TYPE_MAP

MODELS_DIR = Path(__file__).parent / "models"

def _generate_training_data(n=3000):
    import random
    random.seed(42); np.random.seed(42)
    depts = list(DEPT_MAP.keys())
    rows = []
    for _ in range(n):
        dept = random.choice(depts)
        r2o = max(0, random.gauss(30, 15))
        o2e = max(0, random.gauss(60, 25))
        clean = max(10, random.gauss(35, 12))
        delay = 1 if random.random() < 0.1 else 0
        quality = random.uniform(0.5, 0.8) if delay else random.uniform(0.85, 1.0)
        target = max(5, r2o + o2e + clean + random.gauss(0, 10))
        rows.append({"department": dept, "bed_type": random.choice(list(BED_TYPE_MAP.keys())),
                     "hour_of_day": random.randint(6,22), "day_of_week": random.randint(0,6),
                     "readiness_to_order_minutes": r2o, "order_to_exit_minutes": o2e,
                     "cleaning_duration_minutes": clean, "data_quality_score": quality,
                     "event_delay_flag": delay, "minutes_until_safe_bed_available": target})
    return pd.DataFrame(rows)

def train_models():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating training data...")
    df = _generate_training_data(3000)
    X = engineer_features(df)
    y = df["minutes_until_safe_bed_available"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("Training RandomForest...")
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_m = {"model": "RandomForest", "mae": float(mean_absolute_error(y_test, rf_pred)),
             "rmse": float(np.sqrt(mean_squared_error(y_test, rf_pred))), "r2": float(r2_score(y_test, rf_pred))}
    joblib.dump(rf, MODELS_DIR / "random_forest.joblib")
    print("Training XGBoost...")
    xgb = XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=6, random_state=42, verbosity=0)
    xgb.fit(X_train, y_train)
    xgb_pred = xgb.predict(X_test)
    xgb_m = {"model": "XGBoost", "mae": float(mean_absolute_error(y_test, xgb_pred)),
              "rmse": float(np.sqrt(mean_squared_error(y_test, xgb_pred))), "r2": float(r2_score(y_test, xgb_pred))}
    joblib.dump(xgb, MODELS_DIR / "xgboost.joblib")
    metrics = {"random_forest": rf_m, "xgboost": xgb_m, "trained_at": str(pd.Timestamp.now())}
    with open(MODELS_DIR / "metrics.json", "w") as f: json.dump(metrics, f, indent=2)
    print(f"Done. XGBoost MAE={xgb_m['mae']:.1f}min R2={xgb_m['r2']:.3f}")
    return metrics

if __name__ == "__main__":
    train_models()
