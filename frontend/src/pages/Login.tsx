import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { endpoints } from '../api/endpoints';
import { useAuthContext } from '../context/AuthContext';
import { Activity, AlertTriangle } from 'lucide-react';

export const Login: React.FC = () => {
  const [email, setEmail] = useState('admin@hospital.local');
  const [password, setPassword] = useState('Admin@123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuthContext();
  const navigate = useNavigate();
  const location = useLocation();

  const from = (location.state as any)?.from?.pathname || '/';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await endpoints.auth.login({ email, password });
      const { access_token, user } = res.data;
      login(access_token, user);
      navigate(from, { replace: true });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const setDemoCreds = (e: string, p: string) => {
    setEmail(e);
    setPassword(p);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center text-hospital-primary">
          <Activity className="h-12 w-12" />
        </div>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Hospital Operations Command Center
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-xl">
        <div className="bg-hospital-warning text-white p-4 rounded-t-lg flex items-start text-sm">
          <AlertTriangle className="h-5 w-5 mr-3 flex-shrink-0" />
          <p><strong>SYNTHETIC DATA PROTOTYPE</strong> — Not for clinical use. This system does not provide medical advice.</p>
        </div>
        
        <div className="bg-white py-8 px-4 shadow rounded-b-lg sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}
            <div>
              <label className="block text-sm font-medium text-gray-700">Email address</label>
              <div className="mt-1">
                <input
                  type="email" required
                  value={email} onChange={(e) => setEmail(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-hospital-primary focus:border-hospital-primary sm:text-sm"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Password</label>
              <div className="mt-1">
                <input
                  type="password" required
                  value={password} onChange={(e) => setPassword(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-hospital-primary focus:border-hospital-primary sm:text-sm"
                />
              </div>
            </div>

            <div>
              <button
                type="submit" disabled={loading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-hospital-primary hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-hospital-primary disabled:opacity-50"
              >
                {loading ? 'Signing in...' : 'Sign in'}
              </button>
            </div>
          </form>

          <div className="mt-8">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Demo Accounts</h3>
            <div className="overflow-hidden border border-gray-200 rounded-md text-sm">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-3 py-2 text-left font-medium text-gray-500">Role</th>
                    <th className="px-3 py-2 text-left font-medium text-gray-500">Email</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white">
                  {[
                    { role: 'Admin', e: 'admin@hospital.local', p: 'Admin@123' },
                    { role: 'Bed Manager', e: 'bedmanager@hospital.local', p: 'BedMgr@123' },
                    { role: 'Clinical Staff', e: 'doctor@hospital.local', p: 'Doctor@123' },
                    { role: 'Nurse', e: 'nurse@hospital.local', p: 'Nurse@123' },
                    { role: 'Operations', e: 'operations@hospital.local', p: 'Ops@123' },
                  ].map((acc) => (
                    <tr key={acc.role} className="cursor-pointer hover:bg-gray-50" onClick={() => setDemoCreds(acc.e, acc.p)}>
                      <td className="px-3 py-2 whitespace-nowrap font-medium text-hospital-info">{acc.role}</td>
                      <td className="px-3 py-2 whitespace-nowrap text-gray-500">{acc.e}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
