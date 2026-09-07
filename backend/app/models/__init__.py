# Import all models so SQLAlchemy registers them with Base.metadata
# This ensures Base.metadata.create_all() creates all tables
from app.models.user import User
from app.models.patient import Patient
from app.models.clinical import Admission, ClinicalMilestone
from app.models.discharge import DischargeEvent, PatientExitEvent
from app.models.bed import Bed, BedStateEvent, CleaningEvent
from app.models.alert import Alert
from app.models.audit import AuditLog
from app.models.validation import StakeholderValidation, OperatingTheatre, ExperimentResult
