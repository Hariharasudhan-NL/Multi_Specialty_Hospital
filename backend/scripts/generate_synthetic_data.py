import os, sys, random
from datetime import datetime, timedelta, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import engine, Base, SessionLocal
from app.models.patient import Patient
from app.models.bed import Bed, BedStateEvent, CleaningEvent
from app.models.clinical import Admission, ClinicalMilestone
from app.models.discharge import DischargeEvent, PatientExitEvent

DEPTS = ["Cardiology","Neurology","Orthopedics","General Surgery","ENT","Gastroenterology","Urology","General Medicine"]
WARDS = {d: [f"{d[:2].upper()}-{i}" for i in range(1,4)] for d in DEPTS}
BED_TYPES = ["GENERAL","ICU","HDU","SURGICAL"]

def generate_data(n_patients=500):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Patient).count() > 10:
        print("Synthetic data already exists, skipping."); db.close(); return
    random.seed(42)
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=30)
    print("Creating beds...")
    beds = []
    bed_counter = 1
    for dept in DEPTS:
        for ward in WARDS[dept]:
            for _ in range(random.randint(8, 12)):
                prefix = dept[:2].upper().replace(" ","")
                bed = Bed(bed_code=f"{prefix}-{bed_counter:03d}", department=dept, ward=ward,
                          bed_type=random.choices(BED_TYPES, weights=[70,10,10,10])[0],
                          current_state=random.choices(["AVAILABLE","OCCUPIED","CLEANING","BED_READY"],
                                                        weights=[25,55,10,10])[0],
                          last_updated=now - timedelta(minutes=random.randint(0,45)),
                          is_active=True)
                bed_counter += 1
                db.add(bed); beds.append(bed)
    db.flush()
    print(f"Created {len(beds)} beds. Creating {n_patients} patients...")
    for i in range(1, n_patients+1):
        dept = random.choice(DEPTS)
        ward = random.choice(WARDS[dept])
        dept_beds = [b for b in beds if b.department == dept]
        bed = random.choice(dept_beds) if dept_beds else random.choice(beds)
        adm_time = start + timedelta(minutes=random.randint(0, 25*24*60))
        age_days = (now - adm_time).days
        status = "DISCHARGED" if age_days > 5 and random.random() > 0.4 else "ADMITTED"
        p = Patient(patient_code=f"PATIENT-{i:05d}", department=dept, ward=ward, bed_id=bed.id,
                    admission_time=adm_time, status=status)
        db.add(p); db.flush()
        db.add(Admission(patient_id=p.id, admission_type=random.choice(["ELECTIVE","EMERGENCY","TRANSFER"]),
                          department=dept, ward=ward, bed_id=bed.id,
                          event_time=adm_time, received_time=adm_time+timedelta(minutes=2), quality_status="VALID"))
        last_t = adm_time
        for _ in range(random.randint(2,4)):
            mt = last_t + timedelta(hours=random.randint(2,12))
            if mt > now: break
            db.add(ClinicalMilestone(patient_id=p.id,
                                     milestone_type=random.choice(["VITALS_STABLE","LABS_REVIEWED","IMAGING_REVIEWED","MEDICATION_REVIEWED"]),
                                     status="COMPLETED", event_time=mt,
                                     received_time=mt+timedelta(minutes=5), source="CLINICAL_SYSTEM",
                                     quality_score=random.uniform(0.85,1.0), quality_status="VALID"))
            last_t = mt
        dt = last_t + timedelta(hours=random.randint(4,24))
        if dt <= now:
            rand_issue = random.random()
            if rand_issue < 0.05: rs, os_ = "READY_CONFIRMED", None
            elif rand_issue < 0.08: rs, os_ = "POSSIBLY_READY", None
            else: rs = random.choices(["NOT_READY","POSSIBLY_READY","READY_CONFIRMED"], weights=[20,30,50])[0]; os_ = random.choices([None,"ORDERED"], weights=[30,70])[0] if rs=="READY_CONFIRMED" else None
            ot = dt+timedelta(minutes=random.randint(10,60)) if os_=="ORDERED" else None
            if ot and ot > now: ot = None; os_ = None
            de = DischargeEvent(patient_id=p.id, readiness_status=rs,
                                confirmed_by="doctor@hospital.local" if rs=="READY_CONFIRMED" else None,
                                readiness_time=dt if rs=="READY_CONFIRMED" else None,
                                order_status=os_, order_time=ot, event_time=dt,
                                received_time=dt+timedelta(minutes=random.randint(0,10)),
                                quality_status="VALID", is_duplicate=False)
            db.add(de)
            if os_=="ORDERED" and ot:
                exit_t = ot + timedelta(minutes=random.randint(30,90))
                if exit_t <= now:
                    db.add(PatientExitEvent(patient_id=p.id, exit_status="COMPLETED",
                                            event_time=exit_t, received_time=exit_t+timedelta(minutes=3),
                                            quality_status="VALID"))
                    cs = exit_t + timedelta(minutes=random.randint(5,15))
                    ce = exit_t + timedelta(minutes=random.randint(25,60))
                    db.add(CleaningEvent(bed_id=bed.id, cleaning_status="COMPLETED",
                                        started_at=cs, completed_at=ce, quality_status="VALID",
                                        event_time=cs, received_time=cs+timedelta(minutes=2)))
                    db.add(BedStateEvent(bed_id=bed.id, state="AVAILABLE",
                                        event_time=ce+timedelta(minutes=3), received_time=ce+timedelta(minutes=5),
                                        source="BED_SYSTEM", quality_status="VALID", is_duplicate=False))
                    bed.current_state = "AVAILABLE"
                    bed.last_updated = ce + timedelta(minutes=3)
        if i % 100 == 0:
            db.commit(); print(f"  {i}/{n_patients} patients done")
    db.commit()
    print(f"Synthetic data generation complete: {n_patients} patients, {len(beds)} beds.")
    db.close()

if __name__ == "__main__":
    generate_data()
