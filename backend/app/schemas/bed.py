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
