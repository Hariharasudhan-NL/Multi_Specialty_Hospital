import React, { useEffect, useState } from 'react';
import client from '../api/client';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const QUESTIONS = [
  { key: 'q1', param: 'q1', label: 'Was the bed status easy to understand?' },
  { key: 'q2', param: 'q2', label: 'Could you identify stale information?' },
  { key: 'q3', param: 'q3', label: 'Could you understand why a bed was not considered available?' },
  { key: 'q4', param: 'q4', label: 'Could you find supporting evidence?' },
  { key: 'q5', param: 'q5', label: 'Did the dashboard help coordinate discharge and bed turnover?' },
  { key: 'q6', param: 'q6', label: 'Would you use this system in a hospital operations workflow?' },
];
const AVG_KEYS = ['q1_bed_status','q2_stale_info','q3_unavailability_reason','q4_evidence','q5_coordination_help','q6_would_use'];

export const Validation: React.FC = () => {
  const [ratings, setRatings] = useState<Record<string,number>>({});
  const [comments, setComments] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [err, setErr] = useState<string|null>(null);

  useEffect(() => { client.get('/validation/results').then(r => setResults(r.data)).catch(() => {}); }, []);

  const submit = async () => {
    if (Object.keys(ratings).length < 6) { setErr('Please rate all 6 questions.'); return; }
    try {
      await client.post('/validation/submit', null, {
        params: { q1: ratings.q1, q2: ratings.q2, q3: ratings.q3, q4: ratings.q4, q5: ratings.q5, q6: ratings.q6, comments }
      });
      setSubmitted(true);
      const r = await client.get('/validation/results'); setResults(r.data);
    } catch { setErr('Failed to submit. Please retry.'); }
  };

  const chartData = results?.averages ? QUESTIONS.map((_, i) => ({
    name: `Q${i+1}`, score: results.averages[AVG_KEYS[i]] || 0
  })) : [];

  return (
    <div className="p-6 max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Stakeholder Validation</h1>
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mt-2 text-sm text-yellow-700">
          ℹ Prototype stakeholder validation responses only. Not clinical validation.
        </div>
      </div>
      {!submitted ? (
        <div className="bg-white rounded-xl shadow border p-6 space-y-6">
          <p className="text-sm text-gray-600">Rate each item from 1 (Strongly Disagree) to 5 (Strongly Agree).</p>
          {QUESTIONS.map((q, i) => (
            <div key={q.key}>
              <label className="block text-sm font-medium text-gray-700 mb-2">{i+1}. {q.label}</label>
              <div className="flex gap-3">
                {[1,2,3,4,5].map(n => (
                  <button key={n} onClick={() => setRatings(p => ({...p,[q.key]:n}))}
                    aria-label={`Rate ${n}`}
                    className={`w-10 h-10 rounded-full border-2 font-bold text-sm transition-colors ${ratings[q.key]===n?'bg-blue-600 border-blue-600 text-white':'border-gray-300 hover:border-blue-400'}`}>{n}</button>
                ))}
                <span className="self-center text-xs text-gray-400">{ratings[q.key] ? `✓ ${ratings[q.key]}` : 'Not rated'}</span>
              </div>
            </div>
          ))}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Comments (optional)</label>
            <textarea value={comments} onChange={e => setComments(e.target.value)}
              className="w-full border rounded-lg px-3 py-2 text-sm h-24 resize-none" placeholder="Any feedback..."/>
          </div>
          {err && <p className="text-red-600 text-sm">{err}</p>}
          <button onClick={submit} className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700">
            Submit Validation Response
          </button>
        </div>
      ) : (
        <div className="bg-green-50 border border-green-300 rounded-xl p-6 text-center">
          <div className="text-4xl mb-2">✅</div>
          <h2 className="text-lg font-semibold text-green-800">Thank you!</h2>
          <p className="text-sm text-green-700">Your response has been recorded.</p>
        </div>
      )}
      {results && results.total_responses > 0 && (
        <div className="bg-white rounded-xl shadow border p-6">
          <h2 className="text-lg font-semibold mb-1">Aggregated Results</h2>
          <p className="text-xs text-gray-400 mb-4">{results.total_responses} response(s). {results.disclaimer}</p>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="name"/>
              <YAxis domain={[0,5]}/><Tooltip formatter={(v: number) => [v.toFixed(2),'Avg Score']}/>
              <Bar dataKey="score" fill="#2563eb" radius={[4,4,0,0]}/>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};
