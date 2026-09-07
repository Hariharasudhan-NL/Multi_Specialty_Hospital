import React from 'react';
import { PredictionResult } from '../../types';
import { BrainCircuit } from 'lucide-react';

interface PredictionBadgeProps {
  prediction: PredictionResult;
}

export const PredictionBadge: React.FC<PredictionBadgeProps> = ({ prediction }) => {
  if (!prediction.is_available) return null;

  const confidenceColors = {
    HIGH: 'text-green-600 bg-green-50 border-green-200',
    MEDIUM: 'text-yellow-600 bg-yellow-50 border-yellow-200',
    LOW: 'text-red-600 bg-red-50 border-red-200',
  };

  const colorClass = confidenceColors[prediction.confidence] || 'text-gray-600 bg-gray-50 border-gray-200';

  return (
    <div className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium border ${colorClass}`} title={`Model: ${prediction.model}`}>
      <BrainCircuit className="w-3 h-3 mr-1" />
      {prediction.estimated_minutes ? `Est. ${prediction.estimated_minutes}m` : prediction.prediction_type}
      <span className="ml-1 opacity-75">({prediction.confidence})</span>
    </div>
  );
};
