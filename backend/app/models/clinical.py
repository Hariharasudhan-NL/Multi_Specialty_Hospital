from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
from app.database import Base

class Admission(Base):
    __tablename__ = "admissions"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    admission_type = Column(String)
    department = Column(String)
    ward = Column(String)
    bed_id = Column(Integer, ForeignKey("beds.id"), nullable=True)
    event_time = Column(DateTime)
    received_time = Column(DateTime)
    quality_status = Column(String, default="VALID")

class ClinicalMilestone(Base):
    __tablename__ = "clinical_milestones"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    milestone_type = Column(String)
    status = Column(String)
    event_time = Column(DateTime)
    received_time = Column(DateTime)
    source = Column(String)
    quality_score = Column(Float)
    quality_status = Column(String)
