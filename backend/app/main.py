from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from app.database import engine, Base, SessionLocal
import app.models  # noqa: F401 — registers all ORM models with Base.metadata
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
