from pydantic import BaseModel

class DashboardSummary(BaseModel):
    total_beds: int
    occupied_beds: int
    available_beds: int
    cleaning_beds: int
    discharge_ready: int
    discharge_pending: int
    stale_data_count: int
    active_alerts: int
    average_turnover_minutes: float
    baseline_turnover_minutes: float
    prototype_turnover_minutes: float
    improvement_percentage: float
    conflicting_events: int
    missing_events: int
    data_quality_percentage: float
