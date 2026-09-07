import React, { useEffect, useState } from 'react';
import { KPICard } from '../components/common/KPICard';
import { DashboardSummary } from '../types';
import { endpoints } from '../api/endpoints';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { useWebSocketContext } from '../context/WebSocketContext';
import { BedDouble, Users, Sparkles, ClipboardList, Clock, AlertTriangle, ShieldAlert, BarChart2 } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { lastMessage } = useWebSocketContext();

  const fetchDashboard = async () => {
    try {
      const res = await endpoints.dashboard.summary();
      setData(res.data);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  useEffect(() => {
    if (lastMessage) {
      // In a real app, you might update specific stats based on the WS event
      fetchDashboard();
    }
  }, [lastMessage]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!data) return null;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <KPICard title="Total Beds" value={data.total_beds} icon={BedDouble} colorClass="border-gray-500" />
        <KPICard title="Occupied Beds" value={data.occupied_beds} icon={Users} colorClass={data.occupied_beds / data.total_beds > 0.8 ? 'border-orange-500 text-orange-600' : 'border-blue-500'} />
        <KPICard title="Available Beds" value={data.available_beds} icon={BedDouble} colorClass="border-green-500" />
        <KPICard title="Cleaning Beds" value={data.cleaning_beds} icon={Sparkles} colorClass="border-blue-500" />
        <KPICard title="Discharge Ready" value={data.discharge_ready} icon={ClipboardList} colorClass="border-green-500" />
        <KPICard title="Orders Pending" value={data.discharge_pending} icon={Clock} colorClass="border-yellow-500" />
        <KPICard title="Stale Data" value={data.stale_data_count} icon={AlertTriangle} colorClass={data.stale_data_count > 0 ? 'border-red-500' : 'border-gray-300'} />
        <KPICard title="Active Alerts" value={data.active_alerts} icon={ShieldAlert} colorClass="border-red-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow col-span-1 lg:col-span-2">
          <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
            <BarChart2 className="w-5 h-5 mr-2 text-hospital-primary" />
            Turnover Performance
          </h3>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gray-50 p-4 rounded text-center">
              <div className="text-sm text-gray-500">Average Turnover</div>
              <div className="text-2xl font-bold text-gray-900 mt-1">{data.average_turnover_minutes}m</div>
            </div>
            <div className="bg-gray-50 p-4 rounded text-center">
              <div className="text-sm text-gray-500">Baseline vs Prototype</div>
              <div className="text-xl font-bold text-gray-900 mt-1">
                {data.baseline_turnover_minutes}m / {data.prototype_turnover_minutes}m
              </div>
            </div>
            <div className="bg-gray-50 p-4 rounded text-center">
              <div className="text-sm text-gray-500">Improvement</div>
              <div className="text-2xl font-bold text-green-600 mt-1">{data.improvement_percentage.toFixed(1)}%</div>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Data Quality</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Overall Quality</span>
              <span className="font-semibold">{data.data_quality_percentage.toFixed(1)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div className="bg-hospital-primary h-2.5 rounded-full" style={{ width: `${data.data_quality_percentage}%` }}></div>
            </div>
            <div className="flex justify-between items-center pt-2">
              <span className="text-sm text-gray-500">Conflicting Events</span>
              <span className="text-sm font-medium text-red-600">{data.conflicting_events}</span>
            </div>
            <div className="flex justify-between items-center pt-2">
              <span className="text-sm text-gray-500">Missing Events</span>
              <span className="text-sm font-medium text-yellow-600">{data.missing_events}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
