### Multi-Specialty Hospital Operational Prototype

> **Note:** Build scripts used to bootstrap the initial project structure are archived in [`scripts/scaffolding/`](scripts/scaffolding/) and are not required to run the application.

---

> ⚠️ **Safety Notice — Read Before Evaluating**
>
> This is a **synthetic data prototype** for operational coordination research only.
> It does **not** provide medical diagnosis, treatment recommendations, medication advice,
> or autonomous clinical discharge decisions.
> All patient identifiers are synthetic (`PATIENT-XXXXX` format). No real patient data is used anywhere in this project.

---

## Repository

**GitHub:** [https://github.com/Hariharasudhan-NL/Multi_Specialty_Hospital](https://github.com/Hariharasudhan-NL/Multi_Specialty_Hospital)

---

## Project Status at Review 1

| Area | Status |
|------|--------|
| Full-stack web application | ✅ Complete and running |
| Backend API (16 routes) | ✅ Complete |
| Frontend (14 pages) | ✅ Implemented |
| Database with synthetic data | ✅ 230 beds, 500 patients, 995+ events |
| Authentication and role-based access | ✅ 5 roles implemented |
| Discharge readiness board (12 states) | ✅ Complete |
| Bed turnover coordination workflow | ✅ Complete |
| Data freshness engine | ✅ Complete |
| Data quality engine | ✅ Complete |
| Operational alerts | ✅ Complete |
| Failure scenario simulator (6 scenarios) | ✅ Complete |
| ML pipeline (Random Forest + XGBoost) | ✅ Trained, R² = 0.885 |
| Baseline experiment (2,000 samples) | ✅ Complete |
| Prototype experiment (2,000 samples) | ✅ Complete |
| Improvement result | ✅ **52.94%** (target was ≥ 20%) |
| Automated tests | ✅ **11/11 passing** |
| Documentation (9 docs) | ✅ Complete |
| Stakeholder validation sessions | ⏳ Pending |

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Key Features](#3-key-features)
4. [System Architecture](#4-system-architecture)
5. [Technology Stack](#5-technology-stack)
6. [Project Structure](#6-project-structure)
7. [Installation and Setup](#7-installation-and-setup)
8. [Demo Accounts](#8-demo-accounts)
9. [Machine Learning](#9-machine-learning)
10. [Experiment Results](#10-experiment-results)
11. [Testing](#11-testing)
12. [Failure and Edge Cases](#12-failure-and-edge-cases)
13. [Safety and Ethical Limitations](#13-safety-and-ethical-limitations)
14. [Current Status and Future Work](#14-current-status-and-future-work)
15. [Disclaimer](#15-disclaimer)

---

## 1. Project Overview

The AI-Assisted Discharge Readiness and Bed Turnover Coordination System is a full-stack software prototype designed for multi-specialty hospitals to improve the visibility and coordination of patient discharge and bed turnover activities.

The system addresses a key operational problem: bed allocation is delayed because discharge readiness, discharge orders, patient exit, cleaning status, and bed availability are managed in separate disconnected workflows with no centralized visibility.

The prototype provides a centralized operational dashboard that allows authorized hospital staff to monitor discharge progress, bed status, cleaning activities, alerts, data freshness, and expected bed availability — all in one coordinated view.

**Primary measurable outcome:** Time between clinical discharge readiness and next safe bed availability.

---

## 2. Problem Statement

In a multi-specialty hospital, a bed becomes available only after several activities complete in sequence:

1. Patient reaches clinical discharge readiness
2. Discharge order is generated
3. Patient exits the assigned bed
4. Bed is cleaned
5. Bed status is confirmed as updated
6. Bed becomes safely available for the next allocation

When these events are delayed, missing, stale, or distributed across disconnected systems, staff cannot accurately know when a bed will become safely available. This project provides a centralized coordination system that makes every step in this chain visible to authorized staff in real time.

---

## 3. Key Features

### 3.1 Discharge Readiness Board

A real-time kanban board with 12 operational states per patient:

| State | Meaning |
|-------|---------|
| `NOT_READY` | Patient not yet at clinical readiness |
| `POSSIBLY_READY` | Clinical signals suggest readiness |
| `READY_CONFIRMED` | Authorized clinical staff confirmed readiness |
| `ORDER_PENDING` | Readiness confirmed but no discharge order received |
| `DISCHARGE_ORDERED` | Discharge order issued |
| `PATIENT_EXIT_PENDING` | Order issued, patient not yet exited |
| `BED_CLEANING` | Patient exited, cleaning in progress |
| `BED_READY` | All conditions satisfied — bed safely available |
| `DATA_MISSING` | Required information not received |
| `DATA_STALE` | Information exceeds freshness threshold |
| `UNCERTAIN` | Insufficient data to determine state |
| `CONFLICT` | Contradictory events received |

> **Critical safety rule:** `BED_READY` requires ALL of the following simultaneously: patient exit confirmed, cleaning completed, bed state confirmed available, data within freshness threshold, and no conflicts detected. The system never marks a bed ready when any required condition is missing, stale, or conflicting.

### 3.2 Bed Management

Tracks the full operational bed lifecycle:

```
Occupied → Discharge Pending → Exit Pending → Cleaning → Available
```

### 3.3 Data Freshness Engine

Classifies operational information age using configurable thresholds:

| Status | Threshold | Effect |
|--------|-----------|--------|
| `FRESH` | < 15 minutes | Trusted — green indicator |
| `AGING` | 15–30 minutes | Caution — yellow indicator |
| `STALE` | > 30 minutes | Blocks `BED_READY` — red indicator |
| `MISSING` | No update received | Alert raised |

> These thresholds are configurable prototype defaults, not clinical standards.

### 3.4 Data Quality Engine

Detects and flags six categories of data problems:

| Problem | Detection Rule |
|---------|---------------|
| `INVALID` | Event timestamp is in the future |
| `DUPLICATE` | Same event received twice within 5 minutes |
| `DELAYED` | Event received more than 60 minutes after it occurred |
| `CONFLICT` | Cleaning = COMPLETED while bed state = OCCUPIED |
| `MISSING` | Expected event has not arrived |
| `STALE` | Data exceeds freshness threshold |

### 3.5 Drill-Down Evidence

Authorized users can inspect the complete event timeline behind any operational state:

```
Admission → Clinical Milestone → Readiness Confirmation
         → Discharge Order → Patient Exit
         → Cleaning Start → Cleaning Complete → Bed Ready
```

Each event is tagged as: **Observed** / **Predicted** / **Missing** / **Stale** / **Conflicting**

### 3.6 Operational Alerts

Surfaces exceptions including: missing discharge order · stale bed information · conflicting bed state · delayed events · data quality problems.

### 3.7 Failure Scenario Simulator

Administrators can inject and reset six test failure scenarios:

| Scenario | System Response |
|----------|----------------|
| Missing discharge order | `ORDER_PENDING` — does not assume order exists |
| Stale bed data | `DATA_STALE` — does not treat old data as current |
| Conflicting bed state | `CONFLICT` — does not auto-mark bed as available |
| Duplicate event | `DUPLICATE` flagged — event deduplicated |
| Invalid timestamp | `INVALID` flagged — future timestamp rejected |
| Delayed event | `DELAYED` flagged — late arrival noted |

### 3.8 Machine Learning (Operational Estimation Only)

Predicts `minutes_until_safe_bed_available` using Random Forest and XGBoost.

> **Safety boundary enforced:** The model only produces operational estimates ("Estimated bed availability in ~X minutes"). It never states "Patient should be discharged." Clinical discharge readiness is determined exclusively by authorized clinical staff.

### 3.9 Analytics, Role-Based Access, Audit Logging, Real-Time Updates

- Analytics with Recharts charts: turnover time, bed states, cleaning duration, data quality, ML metrics
- JWT authentication with 5 roles: `ADMIN` · `BED_MANAGER` · `CLINICAL_STAFF` · `NURSE` · `OPERATIONS`
- Audit logging of all operational actions
- WebSocket connection for real-time dashboard updates without manual refresh

---

## 4. System Architecture

```
┌─────────────────────────┐
│      React Frontend     │
│   TypeScript / Vite     │
└────────────┬────────────┘
             │
     REST API / WebSocket
             │
             ▼
┌─────────────────────────┐
│     FastAPI Backend     │
│                         │
│  Authentication         │
│  Dashboard APIs         │
│  Patient Management     │
│  Bed Management         │
│  Discharge Management   │
│  Alerts / Analytics     │
└────────────┬────────────┘
             │
   ┌─────────┼──────────┐
   ▼         ▼          ▼
┌──────┐ ┌────────┐ ┌─────────┐
│SQLite│ │Quality │ │Freshness│
│  DB  │ │Engine  │ │Engine   │
└──────┘ └────────┘ └─────────┘
             │
             ▼
   ┌──────────────────┐
   │  Coordination &  │
   │  Readiness Logic │
   └────────┬─────────┘
            │
            ▼
   ┌──────────────────┐
   │  ML Prediction   │
   │  RF / XGBoost    │
   └──────────────────┘
```

---

## 5. Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, React Router, Axios, Recharts, Lucide React |
| **Backend** | Python, FastAPI, Uvicorn, SQLAlchemy, Pydantic, JWT, WebSockets |
| **Database** | SQLite (PostgreSQL-ready via `DATABASE_URL` environment variable) |
| **ML / Data** | Pandas, NumPy, Scikit-learn, XGBoost, Joblib |
| **Testing** | Pytest |

---

## 6. Project Structure

```
Multi_Specialty_Hospital/
│
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy ORM (14 tables)
│   │   ├── routes/          # API route handlers (16 routers)
│   │   ├── services/        # Business logic: readiness, freshness, quality, coordination
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── ml/              # Feature engineering, training, prediction
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── database.py      # DB engine and session
│   │   └── config.py        # Environment-based settings
│   ├── scripts/
│   │   ├── seed_db.py                  # Seeds demo users + generates synthetic data
│   │   └── generate_synthetic_data.py  # 230 beds, 500 patients, 995+ events
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── pages/           # 14 application pages
│   │   ├── components/      # Layout, common UI components
│   │   ├── context/         # AuthContext, WebSocketContext
│   │   ├── api/             # Axios client and endpoint definitions
│   │   └── types/           # TypeScript type definitions
│   ├── package.json
│   └── vite.config.ts
│
├── experiments/
│   ├── baseline_experiment.py    # Simulates existing workflow (2,000 samples)
│   ├── prototype_experiment.py   # Simulates proposed workflow (2,000 samples)
│   ├── evaluation.py             # Computes and saves metrics
│   └── results/
│       ├── evaluation_report.json
│       └── evaluation_report.csv
│
├── tests/                        # Run from project root: python -m pytest tests/ -v
│   ├── conftest.py
│   ├── test_acceptance.py        # 6 acceptance tests
│   ├── test_auth.py
│   ├── test_bed_logic.py
│   ├── test_data_quality.py
│   ├── test_freshness.py
│   └── test_state_engine.py
│
├── scripts/
│   └── scaffolding/         # Bootstrap scripts (not needed to run the app)
│
├── docs/
│   ├── problem_analysis.md
│   ├── user_workflow.md
│   ├── system_architecture.md
│   ├── database_design.md
│   ├── ml_methodology.md
│   ├── experiment_design.md
│   ├── failure_cases.md
│   ├── safety_and_limitations.md
│   └── stakeholder_validation.md
│
├── .env.example
├── .gitignore
└── README.md
```

---

## 7. Installation and Setup

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm

### Clone the Repository

```bash
git clone https://github.com/Hariharasudhan-NL/Multi_Specialty_Hospital.git
cd Multi_Specialty_Hospital
```

---

### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env        # Windows
cp .env.example .env          # Linux / macOS

# Seed database (creates 230 beds, 500 patients, demo users)
python scripts/seed_db.py

# Train ML models
python app/ml/train.py

# Start backend server
python -m uvicorn app.main:app --port 8000 --reload
```

- **API:** http://localhost:8000
- **Swagger UI (interactive docs):** http://localhost:8000/docs

---

### Frontend Setup

> **Important:** Start the backend server before running the frontend.

```bash
cd frontend
npm install
npm run dev
```

Open the URL shown by Vite — typically **http://localhost:5173**

---

### Run Experiments

```bash
cd experiments
python evaluation.py
```

Results saved to `experiments/results/evaluation_report.json` and `.csv`.

---

### Run Tests

```bash
# From project root
python -m pytest tests/ -v
```

---

## 8. Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| **Admin** (full access) | `admin@hospital.local` | `Admin@123` |
| Bed Manager | `bedmanager@hospital.local` | `BedMgr@123` |
| Clinical Staff | `doctor@hospital.local` | `Doctor@123` |
| Nurse | `nurse@hospital.local` | `Nurse@123` |
| Operations | `operations@hospital.local` | `Ops@123` |

> Start with **Admin** to access all 14 pages including the Failure Simulator, Audit Logs, and Settings.

---

## 9. Machine Learning

The ML component estimates operational time until safe bed availability.

**9 input features:** Department, bed type, hour of day, day of week, readiness-to-order gap, order-to-exit gap, cleaning duration, data quality score, delayed event flag.

**Trained on 3,000 synthetic samples:**

| Model | MAE | RMSE | R² |
|-------|-----|------|----|
| Random Forest | 8.78 min | 11.13 min | 0.882 |
| **XGBoost** | **8.70 min** | **11.02 min** | **0.885** |

XGBoost is used as the primary model. All results are based on synthetic data.

**Retrain models:**

```bash
cd backend
python app/ml/train.py
```

---

## 10. Experiment Results

**Metric:** Time between clinical discharge readiness and next safe bed availability.
**Sample size:** 2,000 baseline + 2,000 prototype.

| Metric | Baseline | Prototype |
|--------|----------|-----------|
| Mean turnover time | 163.29 min | 76.85 min |
| Median | 162.88 min | 76.66 min |
| P90 | 205.26 min | 105.61 min |
| **Improvement** | — | **86.44 min saved (52.94%)** |
| Configured target | — | ≥ 20% |
| **Target achieved** | — | ✅ **Yes** |

> **Important:** These are synthetic simulation results. They do not represent real-world hospital performance or clinical validation.

---

## 11. Testing

**Run from project root:**

```bash
python -m pytest tests/ -v
```

**Result: 11 / 11 tests passed**

| Test | What it validates |
|------|------------------|
| `test_acceptance` AT1 | `BED_READY` when all 5 conditions are met |
| `test_acceptance` AT2 | `ORDER_PENDING` when discharge order is missing |
| `test_acceptance` AT3 | `DATA_STALE` when bed data exceeds threshold |
| `test_acceptance` AT4 | `CONFLICT` when cleaning done but bed still occupied |
| `test_acceptance` AT5 | `DUPLICATE` event correctly deduplicated |
| `test_acceptance` AT6 | Future timestamp flagged as `INVALID` |
| `test_auth` | Password hashing and JWT token validation |
| `test_bed_logic` | Bed state event logic |
| `test_data_quality` | Data quality engine detection accuracy |
| `test_freshness` | FRESH / AGING / STALE threshold logic |
| `test_state_engine` | Readiness state machine transitions |

---

## 12. Failure and Edge Cases

### Case 1 — Missing Discharge Order
Patient appears ready but no discharge order received.
→ System shows `ORDER_PENDING`, raises alert. Does not assume the order exists.

### Case 2 — Stale Bed Data
Bed state information is older than the configured freshness threshold.
→ System shows `DATA_STALE`, blocks `BED_READY`. Does not treat old data as current.

### Case 3 — Conflicting Bed Data
Cleaning reported complete but bed state still shows occupied.
→ System shows `CONFLICT`. Does not automatically mark bed as available.

**Additional cases handled:** duplicate events · future timestamps · delayed events · missing fields · invalid state transitions.

Use the **Failure Simulator** page (Admin login) to inject and reset any of these during a demo.

---

## 13. Safety and Ethical Limitations

**The system does NOT:**
- Diagnose patients
- Recommend treatment or medication
- Autonomously approve or deny discharge
- Replace clinical staff or clinical judgment
- Make any medical decisions

Clinical discharge readiness must originate from an authorized clinical workflow or clinical staff member. The system records and displays confirmations but does not generate them.

Machine learning is restricted to operational time estimation only.

See [`docs/safety_and_limitations.md`](docs/safety_and_limitations.md) for the full safety specification.

---

## 14. Current Status and Future Work

### What Is Completed and Working

- Full-stack web application — React frontend + FastAPI backend
- JWT authentication, role-based access (5 roles, 14 pages)
- Discharge readiness board with 12 operational states
- Bed turnover coordination workflow (full lifecycle)
- Data quality engine — 6 detection categories
- Data freshness engine — 4 classification levels
- Operational alerts and audit logging
- Failure scenario simulator — 6 injectable scenarios
- ML prediction pipeline — Random Forest + XGBoost (R² = 0.885)
- Baseline and prototype experiments — 2,000 samples each, 52.94% improvement
- Synthetic data generation — 500 patients, 230 beds, 995+ events
- Automated test suite — 11/11 tests passing
- Project documentation — 9 documents
- Analytics dashboard with Recharts visualizations
- Real-time WebSocket updates
- Drill-down event evidence per patient

### Pending Work

- Stakeholder and user validation sessions
- Expanded end-to-end testing across multi-department concurrent workflows
- Additional missing, stale, and conflicting event test scenarios
- Deeper ML error analysis by department and data quality level
- Dashboard UI improvements 
- Integration and evaluation using real-world operational data and hospital workflows

---

## 15. Disclaimer

This project is a prototype developed to demonstrate hospital operational coordination using synthetic data.

The current implementation is intended for research and demonstration purposes only. Further development, validation, and evaluation are required before integration with real-world hospital data, systems, and operational workflows.

---