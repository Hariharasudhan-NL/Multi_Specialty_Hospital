import React, { useEffect, useState } from 'react';
import client from '../api/client';

export const Cleaning: React.FC = () => {
  const [beds, setBeds] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [stateFilter, setStateFilter] = useState('CLEANING');

  useEffect(() => {
    setLoading(true);
    const params: any = {};
    if (stateFilter) params.state = stateFilter;
    client.get('/beds', { params }).then(r => { setBeds(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, [stateFilter]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4 text-gray-900">Cleaning Queue</h1>
      <div className="flex gap-2 mb-4">
        {['','CLEANING','BED_CLEANING','AVAILABLE','OCCUPIED'].map(s => (
          <button key={s} onClick={() => setStateFilter(s)}
            className={`px-3 py-1.5 rounded-lg text-sm ${stateFilter===s?'bg-blue-600 text-white':'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}>
            {s || 'All Beds'}
          </button>
        ))}
      </div>
      {loading ? <div className="flex justify-center h-40 items-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"/></div> : (
        <div className="bg-white rounded-xl shadow border overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-gray-600 text-xs uppercase">
              <tr>{['Bed','Department','Ward','State','Freshness','Last Updated','Patient'].map(h => <th key={h} className="px-4 py-3 text-left font-semibold">{h}</th>)}</tr>
            </thead>
            <tbody className="divide-y">
              {beds.map((b: any) => (
                <tr key={b.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-bold text-blue-700">{b.bed_code}</td>
                  <td className="px-4 py-3">{b.department}</td>
                  <td className="px-4 py-3">{b.ward}</td>
                  <td className="px-4 py-3"><span className={`px-2 py-1 rounded text-xs ${b.current_state==='CLEANING'?'bg-blue-100 text-blue-700':'bg-gray-100 text-gray-600'}`}>{b.current_state}</span></td>
                  <td className="px-4 py-3"><span className={`text-xs px-2 py-1 rounded ${b.freshness_status==='STALE'?'bg-red-100 text-red-700':b.freshness_status==='AGING'?'bg-yellow-100 text-yellow-700':'bg-green-100 text-green-700'}`}>{b.freshness_status||'UNKNOWN'}</span></td>
                  <td className="px-4 py-3 text-gray-500 text-xs">{b.time_since_update_minutes!=null?`${Math.round(b.time_since_update_minutes)} min ago`:'-'}</td>
                  <td className="px-4 py-3 text-gray-500">{b.patient_code||'-'}</td>
                </tr>
              ))}
              {beds.length===0 && <tr><td colSpan={7} className="text-center py-8 text-gray-400">No beds match the selected filter.</td></tr>}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
