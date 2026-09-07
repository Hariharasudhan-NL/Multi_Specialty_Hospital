from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.database import Base

class StakeholderValidation(Base):
    __tablename__ = "stakeholder_validations"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    q1_bed_status = Column(Integer)
    q2_stale_info = Column(Integer)
    q3_unavailability_reason = Column(Integer)
    q4_evidence = Column(Integer)
    q5_coordination_help = Column(Integer)
    q6_would_use = Column(Integer)
    comments = Column(String, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
class OperatingTheatre(Base):
    __tablename__ = "operating_theatres"
    id = Column(Integer, primary_key=True, index=True)
    theatre_code = Column(String)
    department = Column(String)
    current_status = Column(String)
    current_case_status = Column(String)
    next_scheduled_department = Column(String, nullable=True)
    expected_turnover_minutes = Column(Integer, nullable=True)
    cleaning_status = Column(String)
    delay_minutes = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
class ExperimentResult(Base):
    __tablename__ = "experiment_results"
    id = Column(Integer, primary_key=True, index=True)
    system_type = Column(String)
    metric_name = Column(String)
    metric_value = Column(Float)
    calculated_at = Column(DateTime, default=datetime.utcnow)
