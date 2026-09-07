import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"d:\C_28_Proj\hospital-bed-coordination\backend"

write_file(os.path.join(base_dir, "app/models/bed.py"), """
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
""")

write_file(os.path.join(base_dir, "app/models/alert.py"), """
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String)
    entity_id = Column(String)
    alert_type = Column(String)
    severity = Column(String)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
""")

write_file(os.path.join(base_dir, "app/models/audit.py"), """
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    user_email = Column(String, nullable=True)
    action = Column(String)
    entity_type = Column(String)
    entity_id = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String, nullable=True) # JSON
""")

write_file(os.path.join(base_dir, "app/models/validation.py"), """
from sqlalchemy import Column, Integer, String, DateTime
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
""")

print("Successfully appended models 2.")
