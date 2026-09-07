import React, { useEffect, useState } from 'react';
import client from '../api/client';
import { useAuthContext } from '../context/AuthContext';

export const AuditLogs: React.FC = () => {
  const auth = useAuthContext();
  const user = (auth as any)?.user;
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user?.role !== 'ADMIN') { setLoading(false); return; }
    client.get('/audit').then(r => { setLogs(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, [user]);

  if (user?.role !== 'ADMIN') return <div className="p-6 text-center text-gray-500">Audit logs are only accessible to administrators.</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4 text-gray-900">Audit Logs</h1>
      <p className="text-sm text-gray-500 mb-4">All important actions are recorded. Admin access only.</p>
      {loading ? <div className="flex justify-center h-40 items-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"/></div> : (
        <div className="bg-white rounded-xl shadow border overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-gray-600 text-xs uppercase">
              <tr>{['Timestamp','User','Action','Entity','Entity ID','Details'].map(h => <th key={h} className="px-4 py-3 text-left font-semibold">{h}</th>)}</tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {logs.length===0 && <tr><td colSpan={6} className="text-center py-8 text-gray-400">No audit entries yet</td></tr>}
              {logs.map((l: any) => (
                <tr key={l.id} className="hover:bg-gray-50">
                  <td className="px-4 py-2 text-gray-500 text-xs whitespace-nowrap">{l.timestamp?new Date(l.timestamp).toLocaleString():'-'}</td>
                  <td className="px-4 py-2 text-blue-600 text-xs">{l.user_email||'System'}</td>
                  <td className="px-4 py-2 font-medium text-xs">{l.action}</td>
                  <td className="px-4 py-2 text-xs text-gray-500">{l.entity_type}</td>
                  <td className="px-4 py-2 text-xs text-gray-500">{l.entity_id||'-'}</td>
                  <td className="px-4 py-2 text-xs text-gray-400 max-w-xs truncate">{l.details||'-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
