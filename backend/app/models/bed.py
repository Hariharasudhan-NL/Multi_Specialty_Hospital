from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Bed(Base):
    __tablename__ = "beds"
    id = Column(Integer, primary_key=True, index=True)
    bed_code = Column(String, unique=True, index=True)
    department = Column(String)
    ward = Column(String)
    bed_type = Column(String)
    current_state = Column(String)
    last_updated = Column(DateTime)
    is_active = Column(Boolean, default=True)

class BedStateEvent(Base):
    __tablename__ = "bed_state_events"
    id = Column(Integer, primary_key=True, index=True)
    bed_id = Column(Integer, ForeignKey("beds.id"))
    state = Column(String)
    event_time = Column(DateTime)
    received_time = Column(DateTime)
    source = Column(String)
    quality_status = Column(String)
    is_duplicate = Column(Boolean, default=False)

class CleaningEvent(Base):
    __tablename__ = "cleaning_events"
    id = Column(Integer, primary_key=True, index=True)
    bed_id = Column(Integer, ForeignKey("beds.id"))
    cleaning_status = Column(String)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    quality_status = Column(String)
    event_time = Column(DateTime)
    received_time = Column(DateTime)
