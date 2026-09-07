import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"d:\C_28_Proj\hospital-bed-coordination\backend"

write_file(os.path.join(base_dir, "app/schemas/user.py"), """
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    full_name: str
    role: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
""")

write_file(os.path.join(base_dir, "app/schemas/common.py"), """
from pydantic import BaseModel
from typing import Optional

class UncertaintyInfo(BaseModel):
    has_uncertainty: bool
    reason: Optional[str] = None
    message: Optional[str] = None
    recommended_action: Optional[str] = None
""")

write_file(os.path.join(base_dir, "app/schemas/patient.py"), """
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PatientBase(BaseModel):
    patient_code: str
    department: str
    ward: str
    bed_id: Optional[int]
    status: str

class PatientResponse(PatientBase):
    id: int
    admission_time: Optional[datetime]
    created_at: datetime
    class Config:
        from_attributes = True
""")

write_file(os.path.join(base_dir, "app/schemas/bed.py"), """
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BedBase(BaseModel):
    bed_code: str
    department: str
    ward: str
    bed_type: str
    current_state: str
    is_active: bool = True

class BedResponse(BedBase):
    id: int
    last_updated: Optional[datetime]
    freshness_status: Optional[str] = None
    time_since_update: Optional[str] = None
    class Config:
        from_attributes = True
""")

write_file(os.path.join(base_dir, "app/schemas/dashboard.py"), """
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
""")
