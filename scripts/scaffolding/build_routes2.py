import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"d:\C_28_Proj\hospital-bed-coordination\backend"

write_file(os.path.join(base_dir, "app/routes/discharge.py"), """
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/discharge", tags=["discharge"])

@router.get("/readiness")
def get_readiness(db: Session = Depends(get_db)):
    return []
@router.get("/{patient_id}")
def get_discharge(patient_id: int, db: Session = Depends(get_db)):
    return {}
@router.post("/{patient_id}/confirm-readiness")
def confirm(patient_id: int, db: Session = Depends(get_db)):
    return {}
@router.post("/{patient_id}/update-order")
def update_order(patient_id: int, db: Session = Depends(get_db)):
    return {}
""")

write_file(os.path.join(base_dir, "app/routes/alerts.py"), """
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.get("")
def get_alerts(db: Session = Depends(get_db)):
    return []
@router.post("/{id}/resolve")
def resolve(id: int, db: Session = Depends(get_db)):
    return {}
""")

write_file(os.path.join(base_dir, "app/routes/events.py"), """
from fastapi import APIRouter
router = APIRouter(prefix="/api/events", tags=["events"])
@router.get("")
def get_events(): return []
@router.get("/{id}")
def get_event(id: int): return {}
""")

write_file(os.path.join(base_dir, "app/routes/analytics.py"), """
from fastapi import APIRouter
router = APIRouter(prefix="/api/analytics", tags=["analytics"])
@router.get("/turnover")
def get_turnover(): return {}
@router.get("/data-quality")
def get_dq(): return {}
@router.get("/bed-states")
def get_bs(): return {}
@router.get("/cleaning")
def get_cl(): return {}
@router.get("/prediction-performance")
def get_pp(): return {}
@router.get("/freshness")
def get_fr(): return {}
""")

write_file(os.path.join(base_dir, "app/routes/experiments.py"), """
from fastapi import APIRouter
router = APIRouter(prefix="/api/experiments", tags=["experiments"])
@router.get("/baseline")
def get_baseline(): return {}
@router.get("/prototype")
def get_prototype(): return {}
@router.get("/comparison")
def get_comp(): return {}
@router.get("/error-analysis")
def get_ea(): return {}
""")

write_file(os.path.join(base_dir, "app/routes/demo.py"), """
from fastapi import APIRouter
router = APIRouter(prefix="/api/demo", tags=["demo"])
@router.post("/start")
def start(): return {}
@router.post("/pause")
def pause(): return {}
@router.post("/reset")
def reset(): return {}
@router.get("/status")
def status(): return {}
""")

write_file(os.path.join(base_dir, "app/routes/failure.py"), """
from fastapi import APIRouter
router = APIRouter(prefix="/api/failure", tags=["failure"])
@router.post("/missing-order")
def f1(): return {}
@router.post("/stale-bed")
def f2(): return {}
@router.post("/conflict")
def f3(): return {}
@router.post("/duplicate-event")
def f4(): return {}
@router.post("/invalid-timestamp")
def f5(): return {}
@router.post("/delayed-event")
def f6(): return {}
@router.post("/reset")
def f7(): return {}
@router.get("/status")
def f8(): return {}
""")

write_file(os.path.join(base_dir, "app/routes/validation.py"), """
from fastapi import APIRouter
router = APIRouter(prefix="/api/validation", tags=["validation"])
@router.get("/results")
def r1(): return []
@router.post("/submit")
def r2(): return {}
""")

write_file(os.path.join(base_dir, "app/routes/audit.py"), """
from fastapi import APIRouter
router = APIRouter(prefix="/api/audit", tags=["audit"])
@router.get("")
def r1(): return []
""")

write_file(os.path.join(base_dir, "app/routes/theatre.py"), """
from fastapi import APIRouter
router = APIRouter(prefix="/api/theatre", tags=["theatre"])
@router.get("")
def r1(): return []
@router.get("/{id}")
def r2(id: int): return {}
""")

write_file(os.path.join(base_dir, "app/routes/settings.py"), """
from fastapi import APIRouter
router = APIRouter(prefix="/api/settings", tags=["settings"])
@router.get("")
def r1(): return {}
@router.put("")
def r2(): return {}
""")

write_file(os.path.join(base_dir, "app/routes/search.py"), """
from fastapi import APIRouter
router = APIRouter(prefix="/api/search", tags=["search"])
@router.get("")
def r1(q: str = ""): return []
""")

write_file(os.path.join(base_dir, "app/main.py"), """
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from app.database import engine, Base, SessionLocal
from app.services.websocket_manager import manager
from app.routes import auth, dashboard, beds, patients, discharge, alerts, events, analytics, experiments, demo, failure, validation, audit, theatre, settings, search
from app.config import settings as app_settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    # Check if empty, run seed if needed
    db = SessionLocal()
    from app.models.user import User
    if db.query(User).count() == 0:
        import subprocess
        import os
        # Run seed script
        script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "seed_db.py")
        subprocess.run(["python", script_path], check=False)
    db.close()
    
    # Broadcast task
    async def broadcast_task():
        while True:
            await asyncio.sleep(5)
            await manager.broadcast({"type": "ping"})
            
    task = asyncio.create_task(broadcast_task())
    yield
    task.cancel()

app = FastAPI(title="Hospital Discharge Readiness System", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[app_settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(beds.router)
app.include_router(patients.router)
app.include_router(discharge.router)
app.include_router(alerts.router)
app.include_router(events.router)
app.include_router(analytics.router)
app.include_router(experiments.router)
app.include_router(demo.router)
app.include_router(failure.router)
app.include_router(validation.router)
app.include_router(audit.router)
app.include_router(theatre.router)
app.include_router(settings.router)
app.include_router(search.router)

@app.websocket("/ws/operations")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except:
        manager.disconnect(websocket)
""")
