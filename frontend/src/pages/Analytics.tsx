import React, { useEffect, useState } from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import client from '../api/client';

const COLORS = ['#2563eb','#16a34a','#d97706','#dc2626','#7c3aed','#0891b2','#be185d','#059669'];

export const Analytics: React.FC = () => {
  const [turnover, setTurnover] = useState<any[]>([]);
  const [bedStates, setBedStates] = useState<any[]>([]);
  const [quality, setQuality] = useState<any>({});
  const [freshness, setFreshness] = useState<any[]>([]);
  const [mlMetrics, setMlMetrics] = useState<any>({});
  const [cleaning, setCleaning] = useState<any>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      client.get('/analytics/turnover').then(r => setTurnover(r.data)),
      client.get('/analytics/bed-states').then(r => setBedStates(r.data)),
      client.get('/analytics/data-quality').then(r => setQuality(r.data)),
      client.get('/analytics/freshness').then(r => setFreshness(r.data)),
      client.get('/analytics/prediction-performance').then(r => setMlMetrics(r.data)),
      client.get('/analytics/cleaning').then(r => setCleaning(r.data)),
    ]).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const qualityData = ['valid','missing','stale','duplicate','invalid','conflict','delayed']
    .map(k => ({ name: k.charAt(0).toUpperCase()+k.slice(1), value: quality[k] || 0 }))
    .filter(d => d.value > 0);

  if (loading) return <div className="flex justify-center h-64 items-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"/></div>;

  return (
    <div className="p-6 space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
        <p className="text-sm text-gray-500">All charts use live data. SYNTHETIC DATA — PROTOTYPE ONLY.</p>
      </div>
      <div className="bg-white rounded-xl shadow border p-6">
        <h2 className="text-lg font-semibold mb-4">Average Turnover by Department (minutes)</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={turnover}>
            <CartesianGrid strokeDasharray="3 3"/>
            <XAxis dataKey="department" tick={{ fontSize: 10 }} angle={-15} textAnchor="end" height={60}/>
            <YAxis label={{ value: 'Minutes', angle: -90, position: 'insideLeft', fontSize: 12 }}/>
            <Tooltip formatter={(v: number) => [`${v} min`]}/>
            <Bar dataKey="avg_turnover_minutes" fill="#2563eb" radius={[4,4,0,0]}/>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow border p-6">
          <h2 className="text-lg font-semibold mb-4">Bed State Distribution</h2>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={bedStates} dataKey="count" nameKey="state" cx="50%" cy="50%" outerRadius={90} label={({state, percent}: any) => `${state} ${(percent*100).toFixed(0)}%`}>
                {bedStates.map((_: any, i: number) => <Cell key={i} fill={COLORS[i%COLORS.length]}/>)}
              </Pie>
              <Tooltip/><Legend/>
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl shadow border p-6">
          <h2 className="text-lg font-semibold mb-4">Data Quality</h2>
          <div className="text-center mb-3">
            <span className="text-3xl font-bold text-green-700">{quality.quality_pct || 0}%</span>
            <span className="text-sm text-gray-500 ml-2">events valid</span>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={qualityData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80}>
                {qualityData.map((_: any, i: number) => <Cell key={i} fill={COLORS[i%COLORS.length]}/>)}
              </Pie>
              <Tooltip/><Legend/>
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="bg-white rounded-xl shadow border p-6">
        <h2 className="text-lg font-semibold mb-4">Data Freshness Distribution</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={freshness}>
            <CartesianGrid strokeDasharray="3 3"/>
            <XAxis dataKey="status"/><YAxis/><Tooltip/>
            <Bar dataKey="count" fill="#0891b2" radius={[4,4,0,0]}/>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="bg-white rounded-xl shadow border p-6">
        <h2 className="text-lg font-semibold mb-4">ML Prediction Performance</h2>
        {mlMetrics.error ? <p className="text-gray-500 text-sm">{mlMetrics.error}</p> : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {['random_forest','xgboost'].map(m => { const mt = mlMetrics[m]; if (!mt) return null; return (
              <div key={m} className="bg-gray-50 rounded-lg p-4 border">
                <h3 className="font-semibold capitalize mb-3">{mt.model}</h3>
                <div className="grid grid-cols-3 gap-2 text-center">
                  {[['MAE',`${mt.mae?.toFixed(1)} min`],['RMSE',`${mt.rmse?.toFixed(1)} min`],['R²',mt.r2?.toFixed(3)]].map(([k,v]) => (
                    <div key={k} className="bg-white rounded p-2"><div className="text-xs text-gray-400">{k}</div><div className="font-bold">{v}</div></div>
                  ))}
                </div>
                <p className="text-xs text-gray-400 mt-2">Target: minutes until safe bed available. Operational estimate only.</p>
              </div>
            )})}
          </div>
        )}
      </div>
      <div className="bg-white rounded-xl shadow border p-6">
        <h2 className="text-lg font-semibold mb-3">Cleaning Duration Statistics</h2>
        <div className="grid grid-cols-3 gap-4 text-center">
          {[['Average',`${cleaning.avg_minutes||0} min`],['Min',`${cleaning.min||0} min`],['Max',`${cleaning.max||0} min`]].map(([k,v]) => (
            <div key={k} className="bg-cyan-50 rounded-lg p-4">
              <div className="text-2xl font-bold text-cyan-700">{v}</div>
              <div className="text-sm text-gray-500">{k}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
