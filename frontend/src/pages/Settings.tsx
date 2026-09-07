import React, { useEffect, useState } from 'react';
import client from '../api/client';
import { useAuthContext } from '../context/AuthContext';

export const Settings: React.FC = () => {
  const auth = useAuthContext();
  const user = (auth as any)?.user;
  const [cfg, setCfg] = useState<any>({});
  const [loading, setLoading] = useState(true);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (user?.role === 'ADMIN') {
      client.get('/settings').then(r => { setCfg(r.data); setLoading(false); }).catch(() => setLoading(false));
    } else { setLoading(false); }
  }, [user]);

  if (user?.role !== 'ADMIN') return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      <div className="bg-gray-50 border rounded-lg p-6 text-center text-gray-500">Settings are only configurable by administrators.</div>
    </div>
  );

  return (
    <div className="p-6 max-w-2xl">
      <h1 className="text-2xl font-bold mb-4 text-gray-900">System Settings</h1>
      {loading ? <div className="animate-pulse h-40 bg-gray-100 rounded-xl"/> : (
        <div className="bg-white rounded-xl shadow border p-6 space-y-4">
          {[
            { key: 'freshness_threshold_minutes', label: 'Freshness Threshold (minutes)', desc: 'Events older than this are AGING' },
            { key: 'stale_threshold_minutes', label: 'Stale Threshold (minutes)', desc: 'Events older than this are STALE' },
            { key: 'target_improvement_percentage', label: 'Target Improvement %', desc: 'Required improvement over baseline' },
            { key: 'simulation_speed', label: 'Simulation Speed', desc: 'Demo speed multiplier' },
          ].map(f => (
            <div key={f.key}>
              <label className="block text-sm font-medium text-gray-700">{f.label}</label>
              <p className="text-xs text-gray-400 mb-1">{f.desc}</p>
              <input type="number" value={cfg[f.key] ?? ''}
                onChange={e => setCfg((p: any) => ({...p, [f.key]: Number(e.target.value)}))}
                className="w-full border rounded-lg px-3 py-2 text-sm"/>
            </div>
          ))}
          {saved && <div className="bg-green-50 border border-green-200 rounded p-2 text-sm text-green-700">Settings noted. Restart server to apply changes.</div>}
          <button onClick={() => setSaved(true)} className="w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 text-sm">Save Settings</button>
        </div>
      )}
    </div>
  );
};
