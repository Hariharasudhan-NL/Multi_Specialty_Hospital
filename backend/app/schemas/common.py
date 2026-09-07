from pydantic import BaseModel
from typing import Optional

class UncertaintyInfo(BaseModel):
    has_uncertainty: bool
    reason: Optional[str] = None
    message: Optional[str] = None
    recommended_action: Optional[str] = None
