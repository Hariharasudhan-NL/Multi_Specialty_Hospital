import React, { useEffect, useState } from 'react';
import client from '../api/client';
import { AlertTriangle, CheckCircle, XCircle, Info } from 'lucide-react';

const SEV: Record<string, { bg: string; text: string; icon: React.ReactNode }> = {
  CRITICAL: { bg: 'bg-red-50 border-red-300', text: 'text-red-800', icon: <XCircle className="w-5 h-5 text-red-600" aria-hidden/> },
  HIGH: { bg: 'bg-orange-50 border-orange-300', text: 'text-orange-800', icon: <AlertTriangle className="w-5 h-5 text-orange-600" aria-hidden/> },
  MEDIUM: { bg: 'bg-yellow-50 border-yellow-300', text: 'text-yellow-800', icon: <AlertTriangle className="w-5 h-5 text-yellow-600" aria-hidden/> },
  LOW: { bg: 'bg-blue-50 border-blue-300', text: 'text-blue-700', icon: <Info className="w-5 h-5 text-blue-500" aria-hidden/> },
};

export const Alerts: React.FC = () => {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [sevFilter, setSevFilter] = useState('');

  const fetch = async () => {
    try { const r = await client.get('/alerts'); setAlerts(r.data); }
    catch { } finally { setLoading(false); }
  };

  useEffect(() => { fetch(); const t = setInterval(fetch, 10000); return () => clearInterval(t); }, []);

  const resolve = async (id: number) => {
    await client.post(`/alerts/${id}/resolve`); fetch();
  };

  const filtered = alerts.filter(a => !sevFilter || a.severity === sevFilter);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4 flex-wrap gap-3">
        <h1 className="text-2xl font-bold text-gray-900">Operational Alerts</h1>
        <div className="flex gap-2">
          <select value={sevFilter} onChange={e => setSevFilter(e.target.value)} className="border rounded-lg px-3 py-2 text-sm">
            <option value="">All Severities</option>
            {['CRITICAL','HIGH','MEDIUM','LOW'].map(s => <option key={s} value={s}>{s}</option>)}
          </select>
          <button onClick={fetch} className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">Refresh</button>
        </div>
      </div>
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4 text-sm text-yellow-700">
        ℹ Operational coordination alerts only. These do not represent clinical alerts or medical recommendations.
      </div>
      {loading ? <div className="flex justify-center h-40 items-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"/></div> : (
        <div className="space-y-3">
          {filtered.length === 0 && <div className="text-center text-gray-400 py-12">No active alerts</div>}
          {filtered.map((a: any) => {
            const s = SEV[a.severity] || SEV.LOW;
            return (
              <div key={a.id} className={`border rounded-xl p-4 ${s.bg}`}>
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-start gap-3">
                    <span aria-label={`${a.severity} severity`}>{s.icon}</span>
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className={`font-semibold ${s.text}`}>{a.alert_type}</span>
                        <span className={`text-xs px-2 py-0.5 rounded-full font-medium border ${s.bg} ${s.text}`}>{a.severity}</span>
                        <span className="text-xs text-gray-500">{a.entity_type}: {a.entity_id}</span>
                      </div>
                      <p className="text-sm text-gray-700 mt-1">{a.message}</p>
                      <p className="text-xs text-gray-400 mt-1">{a.created_at ? new Date(a.created_at).toLocaleString() : ''}</p>
                    </div>
                  </div>
                  <button onClick={() => resolve(a.id)}
                    className="flex-shrink-0 px-3 py-1.5 bg-white border border-gray-300 rounded-lg text-sm hover:bg-gray-50 flex items-center gap-1.5">
                    <CheckCircle className="w-3.5 h-3.5 text-green-600"/>Resolve
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
