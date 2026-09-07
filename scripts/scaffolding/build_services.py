import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"d:\C_28_Proj\hospital-bed-coordination\backend"

write_file(os.path.join(base_dir, "app/services/auth_service.py"), """
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")
    return encoded_jwt
""")

write_file(os.path.join(base_dir, "app/services/websocket_manager.py"), """
from fastapi import WebSocket
from typing import List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except:
                pass

manager = ConnectionManager()
""")

write_file(os.path.join(base_dir, "app/services/readiness_engine.py"), """
from enum import Enum

class ReadinessState(str, Enum):
    NOT_READY = 'NOT_READY'
    POSSIBLY_READY = 'POSSIBLY_READY'
    READY_CONFIRMED = 'READY_CONFIRMED'
    ORDER_PENDING = 'ORDER_PENDING'
    DISCHARGE_ORDERED = 'DISCHARGE_ORDERED'
    PATIENT_EXIT_PENDING = 'PATIENT_EXIT_PENDING'
    BED_CLEANING = 'BED_CLEANING'
    BED_READY = 'BED_READY'
    DATA_MISSING = 'DATA_MISSING'
    DATA_STALE = 'DATA_STALE'
    UNCERTAIN = 'UNCERTAIN'
    CONFLICT = 'CONFLICT'

def determine_readiness_state(discharge_event, exit_event, cleaning_event, bed_state_event, data_stale=False, conflict=False):
    if data_stale:
        return ReadinessState.DATA_STALE
    if conflict:
        return ReadinessState.CONFLICT
    if not discharge_event:
        return ReadinessState.DATA_MISSING
        
    rs = discharge_event.readiness_status
    os = discharge_event.order_status
    
    if exit_event and cleaning_event and cleaning_event.cleaning_status == 'COMPLETED':
        if bed_state_event and bed_state_event.state == 'AVAILABLE':
            return ReadinessState.BED_READY
    if exit_event and cleaning_event and cleaning_event.cleaning_status == 'IN_PROGRESS':
        return ReadinessState.BED_CLEANING
    if rs == 'READY_CONFIRMED' and os == 'ORDERED' and not exit_event:
        return ReadinessState.DISCHARGE_ORDERED
    if rs == 'READY_CONFIRMED' and (not os or os == 'PENDING'):
        return ReadinessState.ORDER_PENDING
    if rs == 'POSSIBLY_READY':
        return ReadinessState.POSSIBLY_READY
    if rs == 'NOT_READY':
        return ReadinessState.NOT_READY
    
    return ReadinessState.UNCERTAIN
""")

write_file(os.path.join(base_dir, "app/services/freshness_engine.py"), """
from datetime import datetime, timedelta

def get_freshness_status(event_time: datetime, now: datetime = None):
    if not event_time:
        return "MISSING", None
    if not now:
        now = datetime.utcnow()
    diff = (now - event_time).total_seconds() / 60.0
    if diff < 15:
        return "FRESH", diff
    elif diff <= 30:
        return "AGING", diff
    else:
        return "STALE", diff
""")
