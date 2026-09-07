import React from 'react';
import { UncertaintyInfo } from '../../types';
import { AlertTriangle } from 'lucide-react';

interface UncertaintyBannerProps {
  uncertainty: UncertaintyInfo;
}

export const UncertaintyBanner: React.FC<UncertaintyBannerProps> = ({ uncertainty }) => {
  if (!uncertainty.has_uncertainty) return null;

  return (
    <div className="bg-orange-50 border-l-4 border-orange-400 p-4 mb-4 rounded-r-md">
      <div className="flex">
        <div className="flex-shrink-0">
          <AlertTriangle className="h-5 w-5 text-orange-400" aria-hidden="true" />
        </div>
        <div className="ml-3">
          <h3 className="text-sm font-medium text-orange-800">
            UNCERTAINTY: {uncertainty.reason || 'Data Discrepancy'}
          </h3>
          <div className="mt-2 text-sm text-orange-700">
            <p>{uncertainty.message}</p>
          </div>
          {uncertainty.recommended_action && (
            <div className="mt-4">
              <div className="-mx-2 -my-1.5 flex">
                <button type="button" className="px-2 py-1.5 rounded-md text-sm font-medium text-orange-800 hover:bg-orange-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-orange-50 focus:ring-orange-600">
                  Action: {uncertainty.recommended_action}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
