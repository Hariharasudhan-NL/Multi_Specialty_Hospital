import React, { useEffect, useState } from 'react';
import client from '../api/client';

const STATUS_STYLES: Record<string, string> = {
  AVAILABLE: 'bg-green-100 text-green-700', IN_USE: 'bg-orange-100 text-orange-700',
  CLEANING: 'bg-blue-100 text-blue-700', BLOCKED: 'bg-gray-100 text-gray-600',
};

export const Theatres: React.FC = () => {
  const [theatres, setTheatres] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    client.get('/theatre').then(r => { setTheatres(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-2 text-gray-900">Operating Theatres</h1>
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4 text-sm text-yellow-700">
        ⚕ Operational coordination only. No surgical or clinical decisions.
      </div>
      {loading ? <div className="flex justify-center h-40 items-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"/></div> : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {theatres.map((t: any) => (
            <div key={t.id} className="bg-white rounded-xl shadow border p-5">
              <div className="flex items-center justify-between mb-3">
                <div><div className="font-bold">{t.theatre_code}</div><div className="text-sm text-gray-500">{t.department}</div></div>
                <span className={`px-2 py-1 rounded-lg text-xs font-semibold ${STATUS_STYLES[t.current_status]||'bg-gray-100'}`}>{t.current_status}</span>
              </div>
              <div className="space-y-2 text-sm">
                {[['Case',t.current_case_status],['Cleaning',t.cleaning_status],
                  ['Delay',t.delay_minutes>0?`${t.delay_minutes} min delay`:'On time']
                ].map(([k,v]) => (
                  <div key={k} className="flex justify-between">
                    <span className="text-gray-500">{k}</span>
                    <span className={`font-medium ${k==='Delay'&&t.delay_minutes>0?'text-red-600':''}`}>{v}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
