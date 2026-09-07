import React, { useEffect, useState } from 'react';
import client from '../api/client';
import { AlertTriangle } from 'lucide-react';

const STATE_STYLES: Record<string, { bg: string; border: string; text: string; label: string }> = {
  AVAILABLE: { bg: 'bg-green-50', border: 'border-green-400', text: 'text-green-800', label: 'Available' },
  OCCUPIED: { bg: 'bg-orange-50', border: 'border-orange-400', text: 'text-orange-800', label: 'Occupied' },
  DISCHARGE_PENDING: { bg: 'bg-yellow-50', border: 'border-yellow-400', text: 'text-yellow-800', label: 'Discharge Pending' },
  CLEANING: { bg: 'bg-blue-50', border: 'border-blue-400', text: 'text-blue-800', label: 'Cleaning' },
  BED_READY: { bg: 'bg-emerald-50', border: 'border-emerald-500', text: 'text-emerald-800', label: 'Bed Ready' },
  BLOCKED: { bg: 'bg-gray-100', border: 'border-gray-400', text: 'text-gray-600', label: 'Blocked' },
  CONFLICT: { bg: 'bg-red-50', border: 'border-red-500', text: 'text-red-800', label: 'Conflict' },
  STALE: { bg: 'bg-red-50', border: 'border-red-300', text: 'text-red-700', label: 'Stale' },
  UNKNOWN: { bg: 'bg-gray-50', border: 'border-gray-300', text: 'text-gray-600', label: 'Unknown' },
};

const FRESHNESS_BORDERS: Record<string, string> = {
  FRESH: 'ring-2 ring-green-400',
  AGING: 'ring-2 ring-yellow-400',
  STALE: 'ring-2 ring-red-500',
  MISSING: 'ring-1 ring-gray-300',
};

export const BedBoard: React.FC = () => {
  const [beds, setBeds] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({ department: '', ward: '', state: '', freshness: '' });
  const [selected, setSelected] = useState<any | null>(null);

  const fetchBeds = async () => {
    try {
      const params: any = {};
      if (filters.department) params.department = filters.department;
      if (filters.ward) params.ward = filters.ward;
      if (filters.state) params.state = filters.state;
      if (filters.freshness) params.freshness = filters.freshness;
      const res = await client.get('/beds', { params });
      setBeds(res.data);
      setError(null);
    } catch { setError('Unable to load bed status. Please retry.'); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetchBeds(); const t = setInterval(fetchBeds, 15000); return () => clearInterval(t); }, [filters]);

  const depts = [...new Set(beds.map(b => b.department))].sort();
  const wards = [...new Set(beds.filter(b => !filters.department || b.department === filters.department).map(b => b.ward))].sort();

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"/></div>;

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Bed Status Board</h1>
          <p className="text-sm text-gray-500">{beds.length} beds shown</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {[{ key: 'department', label: 'Department', opts: depts },
            { key: 'ward', label: 'Ward', opts: wards },
            { key: 'state', label: 'State', opts: Object.keys(STATE_STYLES) },
            { key: 'freshness', label: 'Freshness', opts: ['FRESH','AGING','STALE','MISSING'] },
          ].map(f => (
            <select key={f.key} value={(filters as any)[f.key]}
              onChange={e => setFilters(prev => ({ ...prev, [f.key]: e.target.value }))}
              className="border rounded-lg px-3 py-2 text-sm">
              <option value="">All {f.label}s</option>
              {f.opts.map(o => <option key={o} value={o}>{o}</option>)}
            </select>
          ))}
          <button onClick={() => setFilters({ department: '', ward: '', state: '', freshness: '' })}
            className="px-3 py-2 border rounded-lg text-sm hover:bg-gray-50">Clear</button>
        </div>
      </div>
      {error && <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 text-sm">{error}</div>}

      {/* Legend */}
      <div className="flex flex-wrap gap-2">
        {Object.entries(STATE_STYLES).map(([k, v]) => (
          <span key={k} className={`px-2 py-1 rounded text-xs border ${v.bg} ${v.border} ${v.text}`}>{v.label}</span>
        ))}
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3">
        {beds.map(bed => {
          const style = STATE_STYLES[bed.current_state] || STATE_STYLES.UNKNOWN;
          const freshnessRing = FRESHNESS_BORDERS[bed.freshness_status] || '';
          return (
            <div key={bed.id}
              onClick={() => setSelected(bed)}
              className={`cursor-pointer rounded-xl border-2 p-3 ${style.bg} ${style.border} ${freshnessRing} hover:shadow-md transition-all`}>
              <div className={`font-bold text-sm ${style.text}`}>{bed.bed_code}</div>
              <div className="text-xs text-gray-500 mt-0.5">{bed.ward}</div>
              <div className={`mt-2 inline-block px-1.5 py-0.5 rounded text-xs font-medium ${style.bg} ${style.text} border ${style.border}`}>
                {style.label}
              </div>
              {bed.patient_code && <div className="text-xs text-gray-600 mt-1 truncate">{bed.patient_code}</div>}
              {bed.freshness_status && (
                <div className="text-xs text-gray-400 mt-1">{bed.freshness_status}</div>
              )}
              {bed.current_state === 'CONFLICT' && (
                <AlertTriangle className="w-4 h-4 text-red-500 mt-1" aria-label="Conflict" />
              )}
            </div>
          );
        })}
        {beds.length === 0 && (
          <div className="col-span-full text-center text-gray-400 py-12">No beds match the selected filters.</div>
        )}
      </div>

      {selected && (
        <div className="fixed inset-0 z-50 flex justify-end">
          <div className="absolute inset-0 bg-black bg-opacity-40" onClick={() => setSelected(null)} />
          <div className="relative w-full max-w-md bg-white shadow-2xl overflow-y-auto">
            <div className="p-6 border-b bg-gray-800 text-white">
              <div className="flex justify-between">
                <div>
                  <h2 className="text-xl font-bold">{selected.bed_code}</h2>
                  <p className="text-gray-300 text-sm">{selected.department} · {selected.ward}</p>
                </div>
                <button onClick={() => setSelected(null)} className="text-white text-2xl leading-none">&times;</button>
              </div>
            </div>
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-3 text-sm">
                {[['State', selected.current_state], ['Bed Type', selected.bed_type],
                  ['Freshness', selected.freshness_status || 'UNKNOWN'],
                  ['Last Updated', selected.time_since_update_minutes != null ? `${Math.round(selected.time_since_update_minutes)} min ago` : 'Unknown'],
                  ['Patient', selected.patient_code || 'None'],
                  ['Cleaning', selected.cleaning_status || 'N/A'],
                ].map(([k, v]) => (
                  <div key={k} className="bg-gray-50 rounded p-2">
                    <div className="text-gray-400 text-xs">{k}</div>
                    <div className="font-medium text-gray-800">{v}</div>
                  </div>
                ))}
              </div>
              {selected.current_state === 'STALE' && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-700">
                  ⚠ Bed information is stale and requires verification. Do not show as safely available.
                </div>
              )}
              {selected.current_state === 'CONFLICT' && (
                <div className="bg-red-50 border border-red-300 rounded-lg p-3 text-sm text-red-800">
                  ⚠ CONFLICTING DATA: Cleaning and bed state reports contradict each other. Do not automatically mark bed safe.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
