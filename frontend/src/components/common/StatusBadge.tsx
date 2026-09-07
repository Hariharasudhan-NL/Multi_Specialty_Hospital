import React from 'react';
import { ReadinessState } from '../../types';
import { READINESS_COLORS } from '../../utils/colors';

interface StatusBadgeProps {
  status: string;
  type: 'readiness' | 'bed' | 'quality';
}

const BED_COLORS: Record<string, string> = {
  AVAILABLE: 'bg-green-100 text-green-800',
  OCCUPIED: 'bg-orange-100 text-orange-800',
  DISCHARGE_PENDING: 'bg-yellow-100 text-yellow-800',
  CLEANING: 'bg-blue-100 text-blue-800',
  BED_READY: 'bg-emerald-100 text-emerald-800',
  BLOCKED: 'bg-gray-100 text-gray-800',
  STALE: 'bg-red-50 text-red-800 border border-red-300',
  CONFLICT: 'bg-red-100 text-red-900 font-bold border border-red-500',
};

const QUALITY_COLORS: Record<string, string> = {
  VALID: 'bg-green-100 text-green-800',
  MISSING: 'bg-gray-100 text-gray-600',
  STALE: 'bg-yellow-100 text-yellow-800',
  DUPLICATE: 'bg-orange-100 text-orange-800',
  INVALID: 'bg-red-100 text-red-800',
  CONFLICT: 'bg-red-200 text-red-900',
  DELAYED: 'bg-purple-100 text-purple-800',
  UNCERTAIN: 'bg-orange-200 text-orange-900',
};

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, type }) => {
  let colorClass = 'bg-gray-100 text-gray-800';

  if (type === 'readiness') {
    const colorObj = READINESS_COLORS[status as ReadinessState];
    if (colorObj) colorClass = `${colorObj.bg} ${colorObj.text}`;
  } else if (type === 'bed') {
    colorClass = BED_COLORS[status] || colorClass;
  } else if (type === 'quality') {
    colorClass = QUALITY_COLORS[status] || colorClass;
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colorClass}`}>
      {status.replace(/_/g, ' ')}
    </span>
  );
};
