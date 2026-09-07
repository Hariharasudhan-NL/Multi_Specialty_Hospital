import { ReadinessState } from '../types';

export const FRESHNESS_COLORS = {
  FRESH: { bg: 'bg-green-100', text: 'text-green-800', border: 'border-green-300', dot: 'bg-green-500' },
  AGING: { bg: 'bg-yellow-100', text: 'text-yellow-800', border: 'border-yellow-300', dot: 'bg-yellow-500' },
  STALE: { bg: 'bg-red-100', text: 'text-red-800', border: 'border-red-300', dot: 'bg-red-500' },
  MISSING: { bg: 'bg-gray-100', text: 'text-gray-600', border: 'border-gray-300', dot: 'bg-gray-400' },
};

export const READINESS_COLORS: Record<ReadinessState, { bg: string, text: string }> = {
  NOT_READY: { bg: 'bg-gray-100', text: 'text-gray-700' },
  POSSIBLY_READY: { bg: 'bg-blue-100', text: 'text-blue-700' },
  READY_CONFIRMED: { bg: 'bg-green-100', text: 'text-green-700' },
  ORDER_PENDING: { bg: 'bg-yellow-100', text: 'text-yellow-700' },
  DISCHARGE_ORDERED: { bg: 'bg-indigo-100', text: 'text-indigo-700' },
  PATIENT_EXIT_PENDING: { bg: 'bg-purple-100', text: 'text-purple-700' },
  BED_CLEANING: { bg: 'bg-cyan-100', text: 'text-cyan-700' },
  BED_READY: { bg: 'bg-emerald-100', text: 'text-emerald-700' },
  DATA_MISSING: { bg: 'bg-gray-100', text: 'text-gray-500' },
  DATA_STALE: { bg: 'bg-red-100', text: 'text-red-700' },
  UNCERTAIN: { bg: 'bg-orange-100', text: 'text-orange-700' },
  CONFLICT: { bg: 'bg-red-200', text: 'text-red-900' },
};
