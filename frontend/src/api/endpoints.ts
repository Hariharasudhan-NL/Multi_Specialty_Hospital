import client from './client';
import { User, DashboardSummary, Bed, Patient, Alert, ExperimentComparison, FailureScenarioStatus } from '../types';

export const endpoints = {
  auth: {
    login: (data: any) => client.post('/auth/login', data),
    me: () => client.get<User>('/auth/me'),
  },
  dashboard: {
    summary: () => client.get<DashboardSummary>('/dashboard/summary'),
  },
  beds: {
    list: (params?: any) => client.get<Bed[]>('/beds', { params }),
    get: (id: string | number) => client.get<Bed>(`/beds/${id}`),
  },
  patients: {
    list: (params?: any) => client.get<Patient[]>('/patients', { params }),
    get: (id: string | number) => client.get<Patient>(`/patients/${id}`),
  },
  alerts: {
    list: (params?: any) => client.get<Alert[]>('/alerts', { params }),
    resolve: (id: string | number) => client.post(`/alerts/${id}/resolve`),
  },
  experiments: {
    comparison: () => client.get<ExperimentComparison>('/experiments/comparison'),
  },
  failure: {
    missingOrder: () => client.post('/failure/missing-order'),
    staleBed: () => client.post('/failure/stale-bed'),
    conflict: () => client.post('/failure/conflict'),
    duplicateEvent: () => client.post('/failure/duplicate-event'),
    invalidTimestamp: () => client.post('/failure/invalid-timestamp'),
    delayedEvent: () => client.post('/failure/delayed-event'),
    reset: () => client.post('/failure/reset'),
    status: () => client.get<FailureScenarioStatus>('/failure/status'),
  },
  validation: {
    submit: (data: any) => client.post('/validation/submit', data),
  },
  settings: {
    get: () => client.get('/settings'),
    update: (data: any) => client.put('/settings', data),
  },
  search: {
    query: (q: string) => client.get('/search', { params: { q } }),
  }
};
