import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.services.auth_service import get_password_hash

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(User).count() == 0:
        users = [
            User(email="admin@hospital.local", hashed_password=get_password_hash("Admin@123"), role="ADMIN", full_name="Admin User", is_active=True),
            User(email="bedmanager@hospital.local", hashed_password=get_password_hash("BedMgr@123"), role="BED_MANAGER", full_name="Bed Manager", is_active=True),
            User(email="doctor@hospital.local", hashed_password=get_password_hash("Doctor@123"), role="CLINICAL_STAFF", full_name="Dr. Smith", is_active=True),
            User(email="nurse@hospital.local", hashed_password=get_password_hash("Nurse@123"), role="NURSE", full_name="Nurse Johnson", is_active=True),
            User(email="operations@hospital.local", hashed_password=get_password_hash("Ops@123"), role="OPERATIONS", full_name="Operations Team", is_active=True),
        ]
        db.add_all(users); db.commit()
        print("Demo users seeded.")
    db.close()
    from scripts.generate_synthetic_data import generate_data
    generate_data(n_patients=500)

if __name__ == "__main__":
    seed()
