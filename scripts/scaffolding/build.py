import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"d:\C_28_Proj\hospital-bed-coordination\backend"

write_file(os.path.join(base_dir, "requirements.txt"), """
fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy==2.0.36
pydantic==2.9.2
pydantic-settings==2.5.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.12
websockets==13.1
pandas==2.2.3
numpy==1.26.4
scikit-learn==1.5.2
xgboost==2.1.2
joblib==1.4.2
aiofiles==24.1.0
httpx==0.27.2
pytest==8.3.3
pytest-asyncio==0.24.0
""")

write_file(os.path.join(base_dir, ".env.example"), """
DATABASE_URL=sqlite:///./hospital.db
JWT_SECRET=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=480
FRONTEND_URL=http://localhost:5173
FRESHNESS_THRESHOLD_MINUTES=15
STALE_THRESHOLD_MINUTES=30
PREDICTION_CONFIDENCE_THRESHOLD=0.7
SIMULATION_SPEED=1.0
TARGET_IMPROVEMENT_PERCENTAGE=20.0
""")

write_file(os.path.join(base_dir, "app/__init__.py"), "")
write_file(os.path.join(base_dir, "app/models/__init__.py"), "")
write_file(os.path.join(base_dir, "app/schemas/__init__.py"), "")
write_file(os.path.join(base_dir, "app/routes/__init__.py"), "")
write_file(os.path.join(base_dir, "app/services/__init__.py"), "")
write_file(os.path.join(base_dir, "app/ml/__init__.py"), "")

write_file(os.path.join(base_dir, "app/config.py"), """
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = 'sqlite:///./hospital.db'
    jwt_secret: str = 'change-me-in-production'
    access_token_expire_minutes: int = 480
    frontend_url: str = 'http://localhost:5173'
    freshness_threshold_minutes: int = 15
    stale_threshold_minutes: int = 30
    prediction_confidence_threshold: float = 0.7
    simulation_speed: float = 1.0
    target_improvement_percentage: float = 20.0
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

settings = Settings()
""")

write_file(os.path.join(base_dir, "app/database.py"), """
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

engine = create_engine(
    settings.database_url, connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")

print("Successfully created config, database, and structure.")
