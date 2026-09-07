import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"d:\C_28_Proj\hospital-bed-coordination\backend"

write_file(os.path.join(base_dir, "app/ml/features.py"), """
def engineer_features(data):
    pass
""")

write_file(os.path.join(base_dir, "app/ml/train.py"), """
def train_models():
    pass
""")

write_file(os.path.join(base_dir, "app/ml/predict.py"), """
def predict_bed_availability(patient_id: int, db) -> dict:
    return {
        'estimated_minutes': 120,
        'confidence': 'HIGH',
        'model': 'xgboost',
        'prediction_type': 'Operational estimate',
        'is_available': False,
        'uncertainty_reason': None
    }
""")

write_file(os.path.join(base_dir, "app/ml/evaluate.py"), """
def evaluate():
    pass
""")

write_file(os.path.join(base_dir, "scripts/generate_synthetic_data.py"), """
def generate_data():
    pass

if __name__ == "__main__":
    generate_data()
""")

write_file(os.path.join(base_dir, "scripts/seed_db.py"), """
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.services.auth_service import get_password_hash

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(User).count() == 0:
        users = [
            User(email="admin@hospital.local", hashed_password=get_password_hash("Admin@123"), role="ADMIN", full_name="Admin"),
            User(email="bedmanager@hospital.local", hashed_password=get_password_hash("BedMgr@123"), role="BED_MANAGER", full_name="Bed Mgr"),
            User(email="doctor@hospital.local", hashed_password=get_password_hash("Doctor@123"), role="CLINICAL_STAFF", full_name="Doctor"),
            User(email="nurse@hospital.local", hashed_password=get_password_hash("Nurse@123"), role="NURSE", full_name="Nurse"),
            User(email="operations@hospital.local", hashed_password=get_password_hash("Ops@123"), role="OPERATIONS", full_name="Ops")
        ]
        db.add_all(users)
        db.commit()
    db.close()
    print("Database seeded.")

if __name__ == "__main__":
    seed()
""")
