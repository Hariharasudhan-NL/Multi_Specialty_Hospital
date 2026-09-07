from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class DischargeEvent(Base):
    __tablename__ = "discharge_events"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    readiness_status = Column(String)
    confirmed_by = Column(String, nullable=True)
    readiness_time = Column(DateTime, nullable=True)
    order_status = Column(String, nullable=True)
    order_time = Column(DateTime, nullable=True)
    event_time = Column(DateTime)
    received_time = Column(DateTime)
    quality_status = Column(String)
    is_duplicate = Column(Boolean, default=False)

class PatientExitEvent(Base):
    __tablename__ = "patient_exit_events"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    exit_status = Column(String)
    event_time = Column(DateTime)
    received_time = Column(DateTime)
    quality_status = Column(String)
