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
