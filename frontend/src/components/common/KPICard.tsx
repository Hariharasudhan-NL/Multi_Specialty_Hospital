import React from 'react';
import { LucideIcon } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: string;
  colorClass: string;
}

export const KPICard: React.FC<KPICardProps> = ({ title, value, icon: Icon, trend, colorClass }) => {
  return (
    <div className={`bg-white rounded-lg shadow p-5 border-l-4 ${colorClass}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500 truncate">{title}</p>
          <div className="mt-1 text-3xl font-semibold text-gray-900">{value}</div>
        </div>
        <div className={`p-3 rounded-full ${colorClass.replace('border-', 'bg-').replace('-500', '-100')} ${colorClass.replace('border-', 'text-')}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
      {trend && (
        <div className="mt-4">
          <span className="text-sm text-gray-500">{trend}</span>
        </div>
      )}
    </div>
  );
};
