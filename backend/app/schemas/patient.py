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
