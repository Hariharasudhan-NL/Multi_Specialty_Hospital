import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { WebSocketProvider } from './context/WebSocketContext';
import { Layout } from './components/layout/Layout';
import { ProtectedRoute } from './components/layout/ProtectedRoute';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { DischargeBoard } from './pages/DischargeBoard';
import { BedBoard } from './pages/BedBoard';
import { Patients } from './pages/Patients';
import { Alerts } from './pages/Alerts';
import { Analytics } from './pages/Analytics';
import { Experiments } from './pages/Experiments';
import { FailureSimulator } from './pages/FailureSimulator';
import { Validation } from './pages/Validation';
import { AuditLogs } from './pages/AuditLogs';
import { Cleaning } from './pages/Cleaning';
import { Theatres } from './pages/Theatres';
import { Settings } from './pages/Settings';

const App: React.FC = () => (
  <BrowserRouter>
    <AuthProvider>
      <WebSocketProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route index element={<Dashboard />} />
              <Route path="discharge" element={<DischargeBoard />} />
              <Route path="beds" element={<BedBoard />} />
              <Route path="patients" element={<Patients />} />
              <Route path="cleaning" element={<Cleaning />} />
              <Route path="theatres" element={<Theatres />} />
              <Route path="alerts" element={<Alerts />} />
              <Route path="analytics" element={<Analytics />} />
              <Route path="experiments" element={<Experiments />} />
              <Route path="failure-simulator" element={<FailureSimulator />} />
              <Route path="validation" element={<Validation />} />
              <Route path="audit" element={<AuditLogs />} />
              <Route path="settings" element={<Settings />} />
            </Route>
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </WebSocketProvider>
    </AuthProvider>
  </BrowserRouter>
);

export default App;
