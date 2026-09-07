import React, { useEffect, useState } from 'react';
import client from '../api/client';
import { AlertTriangle, RefreshCw, CheckCircle } from 'lucide-react';
import { useAuthContext } from '../context/AuthContext';

const SCENARIOS = [
  { id: 'missing-order', label: 'Inject Missing Discharge Order', icon: '📋',
    description: 'Readiness=CONFIRMED, no order. Expected: ORDER_PENDING + uncertainty banner.',
    endpoint: '/failure/missing-order', color: 'bg-yellow-50 border-yellow-400 hover:bg-yellow-100' },
  { id: 'stale-bed', label: 'Inject Stale Bed Data', icon: '🕐',
    description: 'Bed last_updated set to 70 min ago. Expected: DATA_STALE.',
    endpoint: '/failure/stale-bed', color: 'bg-orange-50 border-orange-400 hover:bg-orange-100' },
  { id: 'conflict', label: 'Inject Conflicting Bed State', icon: '⚠️',
    description: 'Cleaning=COMPLETED, bed_state=OCCUPIED. Expected: CONFLICT.',
    endpoint: '/failure/conflict', color: 'bg-red-50 border-red-400 hover:bg-red-100' },
  { id: 'duplicate-event', label: 'Inject Duplicate Event', icon: '🔂',
    description: 'Same event twice. Expected: DUPLICATE flagged.',
    endpoint: '/failure/duplicate-event', color: 'bg-blue-50 border-blue-400 hover:bg-blue-100' },
  { id: 'invalid-timestamp', label: 'Inject Invalid Timestamp', icon: '📅',
    description: 'Future event_time. Expected: quality_status=INVALID.',
    endpoint: '/failure/invalid-timestamp', color: 'bg-purple-50 border-purple-400 hover:bg-purple-100' },
  { id: 'delayed-event', label: 'Inject Delayed Event', icon: '⏳',
    description: 'Received 120 min after event_time. Expected: DELAYED.',
    endpoint: '/failure/delayed-event', color: 'bg-gray-50 border-gray-400 hover:bg-gray-100' },
];

export const FailureSimulator: React.FC = () => {
  const auth = useAuthContext();
  const user = (auth as any)?.user;
  const [status, setStatus] = useState<any>({ active_scenarios: [], scenario_details: {} });
  const [busy, setBusy] = useState(false);
  const [toast, setToast] = useState<string|null>(null);

  const fetchStatus = async () => {
    try { const r = await client.get('/failure/status'); setStatus(r.data); } catch {}
  };

  useEffect(() => { fetchStatus(); const t = setInterval(fetchStatus, 5000); return () => clearInterval(t); }, []);

  const inject = async (endpoint: string, label: string) => {
    setBusy(true);
    try { await client.post(endpoint); setToast(`✅ ${label} injected.`); await fetchStatus(); }
    catch (e: any) { setToast(`❌ Failed: ${e.response?.data?.detail || 'Unknown error'}`); }
    finally { setBusy(false); setTimeout(() => setToast(null), 4000); }
  };

  const reset = async () => {
    setBusy(true);
    try { await client.post('/failure/reset'); setToast('✅ All scenarios reset.'); await fetchStatus(); }
    catch { setToast('❌ Reset failed.'); }
    finally { setBusy(false); setTimeout(() => setToast(null), 3000); }
  };

  if (user?.role !== 'ADMIN') return <div className="p-6 text-center text-gray-500">Admin access required.</div>;

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Failure Scenario Simulator</h1>
        <p className="text-sm text-gray-500">Inject and observe failure cases for demo and testing purposes.</p>
      </div>
      {toast && (
        <div className={`fixed top-4 right-4 z-50 px-4 py-3 rounded-lg shadow-lg text-sm font-medium ${toast.startsWith('✅')?'bg-green-100 text-green-800 border border-green-300':'bg-red-100 text-red-800 border border-red-300'}`}>{toast}</div>
      )}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-3">
          <h2 className="font-semibold text-gray-700">Inject Scenarios</h2>
          {SCENARIOS.map(s => (
            <button key={s.id} onClick={() => inject(s.endpoint, s.label)} disabled={busy}
              className={`w-full border-2 rounded-xl p-4 text-left transition-colors ${s.color} disabled:opacity-50`}>
              <div className="flex items-center gap-3">
                <span className="text-2xl" role="img" aria-label={s.id}>{s.icon}</span>
                <div>
                  <div className="font-semibold text-sm">{s.label}</div>
                  <div className="text-xs text-gray-600 mt-0.5">{s.description}</div>
                </div>
              </div>
            </button>
          ))}
          <button onClick={reset} disabled={busy}
            className="w-full border-2 border-emerald-400 bg-emerald-50 hover:bg-emerald-100 rounded-xl p-4 flex items-center gap-3 disabled:opacity-50">
            <RefreshCw className="w-6 h-6 text-emerald-600" aria-hidden/>
            <div>
              <div className="font-semibold text-sm text-emerald-800">Reset All Scenarios</div>
              <div className="text-xs text-gray-600">Remove all injected failure data</div>
            </div>
          </button>
        </div>
        <div>
          <h2 className="font-semibold text-gray-700 mb-3">Current Status</h2>
          <div className="bg-white rounded-xl shadow border overflow-hidden">
            {status.active_scenarios.length === 0 ? (
              <div className="p-8 text-center text-gray-400">
                <CheckCircle className="w-12 h-12 mx-auto mb-2 text-gray-300" aria-hidden/>
                No active failure scenarios
              </div>
            ) : (
              <div className="divide-y">
                {status.active_scenarios.map((sc: string) => {
                  const d = status.scenario_details[sc];
                  return (
                    <div key={sc} className="p-4">
                      <div className="flex items-center gap-2 mb-1">
                        <AlertTriangle className="w-4 h-4 text-orange-500" aria-hidden/>
                        <span className="font-semibold text-sm">{sc.replace(/_/g,' ')}</span>
                        <span className="ml-auto px-2 py-0.5 bg-orange-100 text-orange-700 rounded-full text-xs">ACTIVE</span>
                      </div>
                      {d && <div className="text-sm text-gray-600">{d.description}</div>}
                      {d && <div className="text-xs text-gray-400 mt-1">Expected: {d.expected_behavior}</div>}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
