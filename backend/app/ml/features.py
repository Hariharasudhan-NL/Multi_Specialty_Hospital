import pandas as pd
import numpy as np

DEPT_MAP = {d: i for i, d in enumerate(["Cardiology","Neurology","Orthopedics","General Surgery",
                                          "ENT","Gastroenterology","Urology","General Medicine"])}
BED_TYPE_MAP = {"GENERAL": 0, "ICU": 1, "HDU": 2, "SURGICAL": 3}
FEATURE_COLUMNS = ["department_enc","bed_type_enc","hour_of_day","day_of_week",
                   "readiness_to_order_minutes","order_to_exit_minutes",
                   "cleaning_duration_minutes","data_quality_score","event_delay_flag"]

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    f = pd.DataFrame()
    f["department_enc"] = df.get("department", pd.Series()).map(DEPT_MAP).fillna(0)
    f["bed_type_enc"] = df.get("bed_type", pd.Series(["GENERAL"]*len(df))).map(BED_TYPE_MAP).fillna(0)
    if "readiness_time" in df.columns:
        rts = pd.to_datetime(df["readiness_time"], errors="coerce")
        f["hour_of_day"] = rts.dt.hour.fillna(12)
        f["day_of_week"] = rts.dt.dayofweek.fillna(0)
    else:
        f["hour_of_day"] = df.get("hour_of_day", pd.Series([12]*len(df))).fillna(12)
        f["day_of_week"] = df.get("day_of_week", pd.Series([0]*len(df))).fillna(0)
    f["readiness_to_order_minutes"] = pd.to_numeric(df.get("readiness_to_order_minutes", 30), errors="coerce").fillna(30)
    f["order_to_exit_minutes"] = pd.to_numeric(df.get("order_to_exit_minutes", 60), errors="coerce").fillna(60)
    f["cleaning_duration_minutes"] = pd.to_numeric(df.get("cleaning_duration_minutes", 35), errors="coerce").fillna(35)
    f["data_quality_score"] = pd.to_numeric(df.get("data_quality_score", 0.95), errors="coerce").fillna(0.95)
    f["event_delay_flag"] = pd.to_numeric(df.get("event_delay_flag", 0), errors="coerce").fillna(0).astype(int)
    return f[FEATURE_COLUMNS]
