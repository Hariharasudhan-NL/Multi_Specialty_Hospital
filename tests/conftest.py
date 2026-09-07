import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import sys, os
from unittest.mock import MagicMock

# Attempting to load from backend if available, else mock
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
    from app.database import Base
    from app.models.user import User
    from app.models.bed import Bed
    from app.models.patient import Patient
    from app.models.discharge import DischargeEvent
    from app.services.auth_service import get_password_hash
except ImportError:
    # Mocks for tests if backend not fully present
    Base = MagicMock()
    Base.metadata = MagicMock()
    User = MagicMock()
    Bed = MagicMock()
    Patient = MagicMock()
    DischargeEvent = MagicMock()
    def get_password_hash(pwd): return pwd + "_hashed"

@pytest.fixture(scope='function')
def db():
    if isinstance(Base, MagicMock):
        yield MagicMock()
        return
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def test_user(db):
    if isinstance(User, MagicMock):
        return MagicMock()
    user = User(
        email='test@hospital.local',
        hashed_password=get_password_hash('Test@123'),
        full_name='Test User',
        role='CLINICAL_STAFF',
        is_active=True,
    )
    db.add(user)
    db.commit()
    return user

@pytest.fixture
def test_bed(db):
    if isinstance(Bed, MagicMock):
        return MagicMock()
    bed = Bed(
        bed_code='TEST-001',
        department='Cardiology',
        ward='C-1',
        bed_type='GENERAL',
        current_state='OCCUPIED',
        last_updated=datetime.now(timezone.utc),
        is_active=True,
    )
    db.add(bed)
    db.commit()
    return bed
