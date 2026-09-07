import React from 'react';
import { FreshnessStatus } from '../../types';
import { FRESHNESS_COLORS } from '../../utils/colors';

interface FreshnessIndicatorProps {
  lastUpdated: string;
  freshnessStatus: FreshnessStatus;
  compact?: boolean;
}

export const FreshnessIndicator: React.FC<FreshnessIndicatorProps> = ({ lastUpdated, freshnessStatus, compact }) => {
  const colors = FRESHNESS_COLORS[freshnessStatus] || FRESHNESS_COLORS.MISSING;
  
  return (
    <div className={`inline-flex items-center gap-2 px-2 py-1 rounded text-xs font-medium border ${colors.bg} ${colors.text} ${colors.border}`}>
      <div className={`w-2 h-2 rounded-full ${colors.dot}`}></div>
      {!compact && <span>Updated {new Date(lastUpdated).toLocaleTimeString()} — {freshnessStatus}</span>}
      {compact && <span>{freshnessStatus}</span>}
    </div>
  );
};
