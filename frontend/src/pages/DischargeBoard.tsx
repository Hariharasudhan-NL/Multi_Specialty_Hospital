import React, { useEffect, useState } from 'react';
import client from '../api/client';
import { AlertTriangle } from 'lucide-react';

const COLUMNS = [
  { id: 'NOT_READY', label: 'Not Ready', color: 'bg-gray-100 border-gray-300' },
  { id: 'POSSIBLY_READY', label: 'Possibly Ready', color: 'bg-blue-50 border-blue-300' },
  { id: 'READY_CONFIRMED', label: 'Ready Confirmed', color: 'bg-green-50 border-green-300' },
  { id: 'ORDER_PENDING', label: 'Order Pending', color: 'bg-yellow-50 border-yellow-300' },
  { id: 'DISCHARGE_ORDERED', label: 'Discharge Ordered', color: 'bg-indigo-50 border-indigo-300' },
  { id: 'PATIENT_EXIT_PENDING', label: 'Exit Pending', color: 'bg-purple-50 border-purple-300' },
  { id: 'BED_CLEANING', label: 'Bed Cleaning', color: 'bg-cyan-50 border-cyan-300' },
  { id: 'BED_READY', label: 'Bed Ready', color: 'bg-emerald-50 border-emerald-300' },
];

const FRESHNESS_COLORS: Record<string, string> = {
  FRESH: 'bg-green-100 text-green-700',
  AGING: 'bg-yellow-100 text-yellow-700',
  STALE: 'bg-red-100 text-red-700',
  MISSING: 'bg-gray-100 text-gray-500',
};

export const DischargeBoard: React.FC = () => {
  const [patients, setPatients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<any | null>(null);
  const [deptFilter, setDeptFilter] = useState('');

  const fetchData = async () => {
    try {
      const params = deptFilter ? { department: deptFilter } : {};
      const res = await client.get('/discharge/readiness', { params });
      setPatients(res.data);
      setError(null);
    } catch (e: any) {
      setError('Unable to load discharge readiness data. Please retry.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); const t = setInterval(fetchData, 15000); return () => clearInterval(t); }, [deptFilter]);

  const byColumn = (col: string) => patients.filter(p => p.readiness_state === col);
  const depts = [...new Set(patients.map(p => p.department))].sort();

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"/></div>;

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Discharge Coordination Board</h1>
          <p className="text-sm text-gray-500 mt-1">Real-time discharge readiness pipeline. Operational coordination only.</p>
        </div>
        <div className="flex gap-3">
          <select value={deptFilter} onChange={e => setDeptFilter(e.target.value)} className="border rounded-lg px-3 py-2 text-sm">
            <option value="">All Departments</option>
            {depts.map(d => <option key={d} value={d}>{d}</option>)}
          </select>
          <button onClick={fetchData} className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">Refresh</button>
        </div>
      </div>
      {error && <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 text-sm">{error}</div>}
      
      <div className="flex gap-4 overflow-x-auto pb-4" style={{ minHeight: '70vh' }}>
        {COLUMNS.map(col => {
          const colPatients = byColumn(col.id);
          return (
            <div key={col.id} className={`flex-shrink-0 w-64 border-2 rounded-xl ${col.color}`} style={{ minWidth: 240 }}>
              <div className="p-3 border-b border-current border-opacity-20">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-sm">{col.label}</span>
                  <span className="bg-white rounded-full px-2 py-0.5 text-xs font-bold shadow-sm">{colPatients.length}</span>
                </div>
              </div>
              <div className="p-2 space-y-2 overflow-y-auto" style={{ maxHeight: '65vh' }}>
                {colPatients.length === 0 && (
                  <div className="text-center text-gray-400 text-xs py-4">No patients</div>
                )}
                {colPatients.map(p => (
                  <PatientCard key={p.patient_id} patient={p} onClick={() => setSelected(p)} />
                ))}
              </div>
            </div>
          );
        })}
      </div>
      
      {selected && <PatientDrawer patient={selected} onClose={() => setSelected(null)} />}
    </div>
  );
};

const PatientCard: React.FC<{ patient: any; onClick: () => void }> = ({ patient, onClick }) => {
  const hasUncertainty = patient.uncertainty?.has_uncertainty;
  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-lg p-3 shadow-sm border cursor-pointer hover:shadow-md transition-shadow ${hasUncertainty ? 'border-orange-300' : 'border-gray-200'}`}
    >
      <div className="flex items-center justify-between mb-1">
        <span className="font-bold text-xs text-blue-800">{patient.patient_code}</span>
        {hasUncertainty && <AlertTriangle className="w-3 h-3 text-orange-500" aria-label="Uncertainty" />}
      </div>
      <div className="text-xs text-gray-600">{patient.department}</div>
      <div className="text-xs text-gray-500">{patient.ward} · {patient.bed_code || 'No bed'}</div>
      {patient.freshness_status && (
        <span className={`inline-block mt-1 px-1.5 py-0.5 rounded text-xs font-medium ${FRESHNESS_COLORS[patient.freshness_status] || 'bg-gray-100 text-gray-500'}`}>
          {patient.freshness_status}
        </span>
      )}
      {hasUncertainty && (
        <div className="mt-1 p-1.5 bg-orange-50 rounded border border-orange-200 text-xs text-orange-700">
          ⚠ {patient.uncertainty.reason}
        </div>
      )}
    </div>
  );
};

const PatientDrawer: React.FC<{ patient: any; onClose: () => void }> = ({ patient, onClose }) => {
  const [_detail, setDetail] = useState<any>(null);
  useEffect(() => {
    client.get(`/discharge/${patient.patient_id}`).then(r => setDetail(r.data)).catch(() => {});
  }, [patient.patient_id]);

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      <div className="absolute inset-0 bg-black bg-opacity-40" onClick={onClose} />
      <div className="relative w-full max-w-lg bg-white shadow-2xl overflow-y-auto">
        <div className="p-6 border-b bg-blue-700 text-white">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-xl font-bold">{patient.patient_code}</h2>
              <p className="text-blue-200 text-sm">{patient.department} · {patient.ward} · {patient.bed_code}</p>
            </div>
            <button onClick={onClose} className="text-white hover:text-blue-200 text-2xl leading-none">&times;</button>
          </div>
          <div className="mt-3">
            <span className="bg-white bg-opacity-20 px-3 py-1 rounded-full text-sm font-semibold">
              {patient.readiness_state}
            </span>
          </div>
        </div>
        <div className="p-6 space-y-4">
          {patient.uncertainty?.has_uncertainty && (
            <div className="bg-orange-50 border border-orange-300 rounded-lg p-4">
              <div className="flex items-start gap-2">
                <AlertTriangle className="w-5 h-5 text-orange-600 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-orange-800">{patient.uncertainty.reason}</p>
                  <p className="text-sm text-orange-700 mt-1">{patient.uncertainty.message}</p>
                  {patient.uncertainty.recommended_action && (
                    <p className="text-sm text-orange-600 mt-2 font-medium">→ {patient.uncertainty.recommended_action}</p>
                  )}
                </div>
              </div>
            </div>
          )}
          
          <div>
            <h3 className="font-semibold text-gray-700 mb-2">Evidence Timeline</h3>
            <TimelineSection patient={patient} />
          </div>

          <div>
            <h3 className="font-semibold text-gray-700 mb-2">Data Freshness</h3>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="bg-gray-50 rounded p-2">
                <span className="text-gray-500">Discharge Event</span>
                <span className={`ml-2 px-2 py-0.5 rounded text-xs ${FRESHNESS_COLORS[patient.freshness_status] || ''}`}>
                  {patient.freshness_status || 'MISSING'}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-xs text-blue-700">
            <strong>⚕ Clinical Safety Notice:</strong> Discharge readiness must be confirmed by authorized clinical staff. 
            This system provides operational coordination only and does not make clinical decisions.
          </div>
        </div>
      </div>
    </div>
  );
};

const TimelineSection: React.FC<{ patient: any }> = ({ patient }) => {
  const steps = [
    { label: 'Readiness Status', value: patient.readiness_state, type: patient.readiness_state === 'DATA_MISSING' ? 'MISSING' : 'OBSERVED' },
    { label: 'Discharge Order', value: patient.discharge_order_status || 'NOT RECEIVED', type: patient.discharge_order_status ? 'OBSERVED' : 'MISSING' },
    { label: 'Patient Exit', value: patient.exit_status || 'PENDING', type: patient.exit_status === 'COMPLETED' ? 'OBSERVED' : 'MISSING' },
    { label: 'Bed Cleaning', value: patient.cleaning_status || 'NOT STARTED', type: patient.cleaning_status === 'COMPLETED' ? 'OBSERVED' : 'MISSING' },
  ];
  const typeColor: Record<string, string> = {
    OBSERVED: 'bg-green-100 border-green-300 text-green-800',
    MISSING: 'bg-gray-100 border-gray-300 text-gray-600',
    STALE: 'bg-red-100 border-red-300 text-red-800',
    CONFLICTING: 'bg-red-200 border-red-400 text-red-900',
  };
  return (
    <div className="space-y-2">
      {steps.map((step, i) => (
        <div key={i} className={`border rounded-lg p-3 ${typeColor[step.type] || typeColor.OBSERVED}`}>
          <div className="flex justify-between">
            <span className="font-medium text-sm">{step.label}</span>
            <span className="text-xs bg-white bg-opacity-50 px-2 py-0.5 rounded">{step.type}</span>
          </div>
          <div className="text-sm mt-1">{step.value}</div>
        </div>
      ))}
    </div>
  );
};
