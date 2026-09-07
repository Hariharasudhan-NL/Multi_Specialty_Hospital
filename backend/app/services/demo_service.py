from datetime import datetime, timezone
from typing import Optional

DEMO_STEPS = [
    {"step": 1, "title": "Patient Admission", "description": "PATIENT-00123 admitted to Cardiology."},
    {"step": 2, "title": "Clinical Milestones", "description": "Clinical milestones recorded. Authorized staff confirms discharge readiness."},
    {"step": 3, "title": "Discharge & Bed Ready", "description": "Order issued, patient exits, cleaning completes, bed becomes BED_READY."},
    {"step": 4, "title": "Failure Scenarios", "description": "Injecting: Missing Order → Stale Data → Conflict."},
    {"step": 5, "title": "Analytics & Results", "description": "Baseline vs Prototype evaluation complete."},
]

class DemoState:
    status: str = "STOPPED"
    current_step: int = 0
    speed: float = 1.0
    started_at: Optional[datetime] = None

_state = DemoState()

def start_demo(speed: float = 1.0):
    _state.status = "RUNNING"; _state.current_step = 1
    _state.speed = speed; _state.started_at = datetime.now(timezone.utc)

def pause_demo(): _state.status = "PAUSED"

def reset_demo():
    _state.status = "STOPPED"; _state.current_step = 0
    _state.speed = 1.0; _state.started_at = None

def advance_step():
    if _state.current_step < len(DEMO_STEPS): _state.current_step += 1
    else: _state.status = "STOPPED"

def get_demo_status() -> dict:
    return {
        "status": _state.status, "current_step": _state.current_step,
        "total_steps": len(DEMO_STEPS), "speed": _state.speed,
        "steps": DEMO_STEPS,
        "current_step_info": DEMO_STEPS[_state.current_step-1] if 0 < _state.current_step <= len(DEMO_STEPS) else None
    }
