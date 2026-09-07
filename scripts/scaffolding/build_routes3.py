import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"d:\C_28_Proj\hospital-bed-coordination\backend"

write_file(os.path.join(base_dir, "app/routes/analytics.py"), """
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.bed import Bed
from app.models.patient import Patient

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/turnover")
def get_turnover(db: Session = Depends(get_db)):
    return {"avg_turnover": 120}

@router.get("/data-quality")
def get_dq(db: Session = Depends(get_db)):
    return {"quality": "good"}

@router.get("/bed-states")
def get_bs(db: Session = Depends(get_db)):
    beds = db.query(Bed).all()
    states = {}
    for b in beds:
        states[b.current_state] = states.get(b.current_state, 0) + 1
    return states

@router.get("/cleaning")
def get_cl(db: Session = Depends(get_db)):
    return {"cleaning": "stats"}

@router.get("/prediction-performance")
def get_pp(db: Session = Depends(get_db)):
    return {"mae": 10.5, "rmse": 15.2, "r2": 0.85}

@router.get("/freshness")
def get_fr(db: Session = Depends(get_db)):
    return {"freshness": "data"}
""")
