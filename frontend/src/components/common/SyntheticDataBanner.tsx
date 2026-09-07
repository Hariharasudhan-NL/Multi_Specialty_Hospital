import React from 'react';
import { AlertTriangle } from 'lucide-react';

export const SyntheticDataBanner: React.FC = () => {
  return (
    <div className="bg-hospital-warning text-white px-4 py-2 flex items-center justify-center text-sm font-bold z-50">
      <AlertTriangle className="w-4 h-4 mr-2" />
      SYNTHETIC DATA — PROTOTYPE ONLY — Not for clinical use
    </div>
  );
};
