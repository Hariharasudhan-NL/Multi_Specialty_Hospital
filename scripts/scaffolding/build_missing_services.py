import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"d:\C_28_Proj\hospital-bed-coordination\backend"

write_file(os.path.join(base_dir, "app/services/data_quality_engine.py"), "def check_quality(): pass")
write_file(os.path.join(base_dir, "app/services/coordination_engine.py"), "def coordinate(): pass")
write_file(os.path.join(base_dir, "app/services/alert_service.py"), "def check_alerts(): pass")
write_file(os.path.join(base_dir, "app/services/audit_service.py"), "def log_audit(): pass")
write_file(os.path.join(base_dir, "app/services/demo_service.py"), "def start_demo(): pass")
write_file(os.path.join(base_dir, "app/services/failure_service.py"), """
def inject_missing_discharge_order(bed_id): pass
def inject_stale_bed_data(bed_id): pass
def inject_conflicting_bed_state(bed_id): pass
def inject_duplicate_event(patient_id): pass
def inject_invalid_timestamp(bed_id): pass
def inject_delayed_event(patient_id): pass
def reset_scenario(): pass
""")
