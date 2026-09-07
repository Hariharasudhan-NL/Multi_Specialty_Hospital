import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"d:\C_28_Proj\hospital-bed-coordination\backend"

write_file(os.path.join(base_dir, "app/models/user.py"), """
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
""")

write_file(os.path.join(base_dir, "app/models/patient.py"), """
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

class PatientExitEvent(Base):
    __tablename__ = "patient_exit_events"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    exit_status = Column(String)
    event_time = Column(DateTime)
    received_time = Column(DateTime)
    quality_status = Column(String)
""")

write_file(os.path.join(base_dir, "app/models/clinical.py"), """
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
    bed_id = Column(Integer, ForeignKey("beds.id"))
    event_time = Column(DateTime)
    received_time = Column(DateTime)
    quality_status = Column(String)

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
""")

write_file(os.path.join(base_dir, "app/models/discharge.py"), """
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
""")

print("Successfully appended models.")
