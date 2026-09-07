from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from datetime import datetime
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_code = Column(String, unique=True, index=True)
    department = Column(String)
    ward = Column(String)
    bed_id = Column(Integer, ForeignKey("beds.id"))
    admission_time = Column(DateTime)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
