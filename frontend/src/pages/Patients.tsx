import React, { useEffect, useState } from 'react';
import client from '../api/client';
import { Search, ChevronRight } from 'lucide-react';

const READINESS_COLORS: Record<string, string> = {
  NOT_READY: 'bg-gray-100 text-gray-700', POSSIBLY_READY: 'bg-blue-100 text-blue-700',
  READY_CONFIRMED: 'bg-green-100 text-green-700', ORDER_PENDING: 'bg-yellow-100 text-yellow-700',
  DISCHARGE_ORDERED: 'bg-indigo-100 text-indigo-700', PATIENT_EXIT_PENDING: 'bg-purple-100 text-purple-700',
  BED_CLEANING: 'bg-cyan-100 text-cyan-700', BED_READY: 'bg-emerald-100 text-emerald-700',
  DATA_MISSING: 'bg-gray-50 text-gray-400', DATA_STALE: 'bg-red-100 text-red-700',
  UNCERTAIN: 'bg-orange-100 text-orange-700', CONFLICT: 'bg-red-200 text-red-900',
};

export const Patients: React.FC = () => {
  const [patients, setPatients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string|null>(null);
  const [search, setSearch] = useState('');
  const [dept, setDept] = useState('');
  const [selected, setSelected] = useState<any|null>(null);

  const fetchPatients = () => {
    setLoading(true);
    client.get('/patients', { params: dept ? { department: dept } : {} })
      .then(r => { setPatients(r.data); setError(null); })
      .catch(() => setError('Unable to load patients. Please retry.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchPatients(); }, [dept]);

  const filtered = patients.filter(p =>
    !search || p.patient_code?.toLowerCase().includes(search.toLowerCase()) ||
    p.department?.toLowerCase().includes(search.toLowerCase()));
  const depts = [...new Set(patients.map((p: any) => p.department))].sort() as string[];

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4 text-gray-900">Patients</h1>
      <div className="flex gap-3 mb-4 flex-wrap">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400"/>
          <input value={search} onChange={e => setSearch(e.target.value)}
            placeholder="Search by patient ID..." className="pl-9 pr-4 py-2 border rounded-lg text-sm w-64"/>
        </div>
        <select value={dept} onChange={e => setDept(e.target.value)} className="border rounded-lg px-3 py-2 text-sm">
          <option value="">All Departments</option>
          {depts.map((d: string) => <option key={d} value={d}>{d}</option>)}
        </select>
        <button onClick={fetchPatients} className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">Refresh</button>
      </div>
      {error && <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 text-sm mb-4">{error}</div>}
      {loading ? (
        <div className="flex justify-center h-40 items-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"/></div>
      ) : (
        <div className="bg-white rounded-xl shadow border overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-gray-600 text-xs uppercase">
              <tr>{['Patient ID','Department','Ward','Bed','Admission','Readiness','Freshness',''].map(h => (
                <th key={h} className="px-4 py-3 text-left font-semibold">{h}</th>
              ))}</tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filtered.slice(0,100).map((p: any) => (
                <tr key={p.id} className="hover:bg-gray-50 cursor-pointer" onClick={() => setSelected(p)}>
                  <td className="px-4 py-3 font-mono font-bold text-blue-700">{p.patient_code}</td>
                  <td className="px-4 py-3">{p.department}</td>
                  <td className="px-4 py-3">{p.ward}</td>
                  <td className="px-4 py-3">{p.bed_code || '-'}</td>
                  <td className="px-4 py-3 text-gray-500">{p.admission_time ? new Date(p.admission_time).toLocaleDateString() : '-'}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${READINESS_COLORS[p.readiness_state] || 'bg-gray-100 text-gray-600'}`}>
                      {p.readiness_state?.replace(/_/g,' ') || '-'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-xs">
                    <span className={p.freshness_status === 'STALE' ? 'text-red-600 font-semibold' : 'text-gray-500'}>
                      {p.freshness_status || '-'}
                    </span>
                  </td>
                  <td className="px-4 py-3"><ChevronRight className="w-4 h-4 text-gray-400"/></td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr><td colSpan={8} className="text-center py-8 text-gray-400">No patients found</td></tr>
              )}
            </tbody>
          </table>
          {filtered.length > 100 && <p className="p-3 text-center text-sm text-gray-400">Showing 100 of {filtered.length}. Use filters to narrow.</p>}
        </div>
      )}
      {selected && (
        <div className="fixed inset-0 z-50 flex justify-end">
          <div className="absolute inset-0 bg-black bg-opacity-40" onClick={() => setSelected(null)}/>
          <div className="relative w-full max-w-lg bg-white shadow-2xl p-6 overflow-y-auto">
            <div className="flex justify-between items-start mb-4">
              <div><h2 className="text-xl font-bold">{selected.patient_code}</h2>
                <p className="text-gray-500">{selected.department} · {selected.ward}</p></div>
              <button onClick={() => setSelected(null)} className="text-2xl text-gray-400">&times;</button>
            </div>
            <div className="grid grid-cols-2 gap-3 text-sm">
              {[['Readiness', selected.readiness_state],['Freshness', selected.freshness_status],
                ['Admission', selected.admission_time ? new Date(selected.admission_time).toLocaleString() : '-'],
                ['Bed', selected.bed_code || '-'],['Status', selected.status || '-']
              ].map(([k,v]) => (
                <div key={k} className="bg-gray-50 rounded-lg p-3">
                  <div className="text-gray-400 text-xs mb-1">{k}</div>
                  <div className="font-semibold">{v}</div>
                </div>
              ))}
            </div>
            <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-3 text-xs text-blue-700">
              ⚕ Clinical decisions are not made by this system. All identifiers are synthetic.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
