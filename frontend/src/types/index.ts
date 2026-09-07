export type UserRole = 'ADMIN' | 'BED_MANAGER' | 'CLINICAL_STAFF' | 'NURSE' | 'OPERATIONS';

export type FreshnessStatus = 'FRESH' | 'AGING' | 'STALE' | 'MISSING';

export type ReadinessState = 
  | 'NOT_READY' | 'POSSIBLY_READY' | 'READY_CONFIRMED'
  | 'ORDER_PENDING' | 'DISCHARGE_ORDERED' | 'PATIENT_EXIT_PENDING'
  | 'BED_CLEANING' | 'BED_READY' | 'DATA_MISSING' | 'DATA_STALE'
  | 'UNCERTAIN' | 'CONFLICT';

export type BedState = 
  | 'AVAILABLE' | 'OCCUPIED' | 'DISCHARGE_PENDING' | 'PATIENT_EXIT_PENDING'
  | 'CLEANING' | 'BED_READY' | 'BLOCKED' | 'UNKNOWN' | 'STALE' | 'CONFLICT';

export type AlertSeverity = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export type QualityStatus = 'VALID' | 'MISSING' | 'STALE' | 'DUPLICATE' | 'INVALID' | 'CONFLICT' | 'DELAYED' | 'UNCERTAIN';

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
}

export interface DashboardSummary {
  total_beds: number;
  occupied_beds: number;
  available_beds: number;
  cleaning_beds: number;
  discharge_ready: number;
  discharge_pending: number;
  stale_data_count: number;
  active_alerts: number;
  average_turnover_minutes: number;
  baseline_turnover_minutes: number;
  prototype_turnover_minutes: number;
  improvement_percentage: number;
  conflicting_events: number;
  missing_events: number;
  data_quality_percentage: number;
}

export interface Alert {
  id: number;
  entity_type: string;
  entity_id: string;
  alert_type: string;
  severity: AlertSeverity;
  message: string;
  created_at: string;
  resolved_at?: string;
  is_active: boolean;
}

export interface Bed {
  id: number;
  bed_code: string;
  department: string;
  ward: string;
  bed_type: string;
  current_state: BedState;
  last_updated: string;
  freshness_status: FreshnessStatus;
  time_since_update_minutes: number;
  patient_id?: number;
  patient_code?: string;
  expected_availability_minutes?: number;
  alert?: Alert;
  cleaning_status?: string;
}

export interface DischargeEvent {
  id: number;
  readiness_status: string;
  confirmed_by?: string;
  readiness_time?: string;
  order_status?: string;
  order_time?: string;
  event_time: string;
  quality_status: QualityStatus;
}

export interface PatientExitEvent {
  exit_status: string;
  event_time: string;
  quality_status: QualityStatus;
}

export interface CleaningEvent {
  cleaning_status: string;
  started_at?: string;
  completed_at?: string;
  event_time: string;
  quality_status: QualityStatus;
}

export interface TimelineEvent {
  event_type: string;
  event_time: string;
  status: string;
  source?: string;
  quality_status: QualityStatus;
  duration_from_previous_minutes?: number;
  data_type: 'OBSERVED' | 'PREDICTED' | 'MISSING' | 'STALE' | 'CONFLICTING';
}

export interface PredictionResult {
  estimated_minutes?: number;
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
  model: string;
  prediction_type: string;
  is_available: boolean;
  uncertainty_reason?: string;
}

export interface UncertaintyInfo {
  has_uncertainty: boolean;
  reason?: string;
  message?: string;
  recommended_action?: string;
}

export interface Patient {
  id: number;
  patient_code: string;
  department: string;
  ward: string;
  bed_id?: number;
  bed_code?: string;
  admission_time: string;
  status: string;
  readiness_state: ReadinessState;
  readiness_freshness: FreshnessStatus;
  discharge_event?: DischargeEvent;
  exit_event?: PatientExitEvent;
  prediction?: PredictionResult;
  uncertainty?: UncertaintyInfo;
  timeline?: TimelineEvent[];
}

export interface ExperimentComparison {
  baseline_mean: number;
  baseline_median: number;
  baseline_p90: number;
  baseline_std: number;
  prototype_mean: number;
  prototype_median: number;
  prototype_p90: number;
  prototype_std: number;
  absolute_improvement_mean: number;
  percentage_improvement: number;
  target_percentage: number;
  target_achieved: boolean;
  sample_size: number;
}

export interface FailureScenarioStatus {
  active_scenarios: string[];
  scenario_details: Record<string, {
    injected_at: string;
    expected_behavior: string;
    actual_behavior: string;
    pass_fail: 'PASS' | 'FAIL' | 'PENDING';
  }>;
}
