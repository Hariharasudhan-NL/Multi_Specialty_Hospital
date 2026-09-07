import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, ClipboardList, BedDouble, Users, 
  Sparkles, Building2, Bell, BarChart2, FlaskConical, 
  AlertTriangle, CheckSquare, History, Settings, LogOut 
} from 'lucide-react';
import { useAuthContext } from '../../context/AuthContext';

export const Sidebar: React.FC = () => {
  const { user, logout } = useAuthContext();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { to: '/', icon: LayoutDashboard, label: 'Dashboard', roles: ['ADMIN', 'BED_MANAGER', 'CLINICAL_STAFF', 'NURSE', 'OPERATIONS'] },
    { to: '/discharge', icon: ClipboardList, label: 'Discharge Board', roles: ['ADMIN', 'BED_MANAGER', 'CLINICAL_STAFF', 'NURSE'] },
    { to: '/beds', icon: BedDouble, label: 'Bed Board', roles: ['ADMIN', 'BED_MANAGER', 'NURSE', 'OPERATIONS'] },
    { to: '/patients', icon: Users, label: 'Patients', roles: ['ADMIN', 'CLINICAL_STAFF', 'NURSE'] },
    { to: '/cleaning', icon: Sparkles, label: 'Cleaning', roles: ['ADMIN', 'OPERATIONS', 'NURSE'] },
    { to: '/theatres', icon: Building2, label: 'Operating Theatres', roles: ['ADMIN', 'CLINICAL_STAFF', 'OPERATIONS'] },
    { to: '/alerts', icon: Bell, label: 'Alerts', roles: ['ADMIN', 'BED_MANAGER', 'OPERATIONS'] },
    { to: '/analytics', icon: BarChart2, label: 'Analytics', roles: ['ADMIN', 'BED_MANAGER'] },
    { to: '/experiments', icon: FlaskConical, label: 'Experiments', roles: ['ADMIN', 'BED_MANAGER'] },
    { to: '/failure-simulator', icon: AlertTriangle, label: 'Failure Simulator', roles: ['ADMIN'] },
    { to: '/validation', icon: CheckSquare, label: 'Validation', roles: ['ADMIN', 'BED_MANAGER', 'CLINICAL_STAFF', 'NURSE', 'OPERATIONS'] },
    { to: '/audit', icon: History, label: 'Audit Logs', roles: ['ADMIN'] },
    { to: '/settings', icon: Settings, label: 'Settings', roles: ['ADMIN', 'BED_MANAGER'] },
  ];

  const visibleItems = navItems.filter(item => user?.role && item.roles.includes(user.role));

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col min-h-screen">
      <div className="p-4 flex items-center justify-center border-b border-gray-800">
        <h1 className="text-xl font-bold tracking-wider">HOSPITAL<span className="text-hospital-info">OS</span></h1>
      </div>
      
      {user && (
        <div className="p-4 border-b border-gray-800">
          <div className="text-sm font-medium">{user.full_name}</div>
          <div className="text-xs text-gray-400 mt-1 flex items-center">
            <span className="px-2 py-0.5 rounded bg-gray-800 text-gray-300 border border-gray-700">{user.role}</span>
          </div>
        </div>
      )}

      <nav className="flex-1 overflow-y-auto py-4">
        <ul className="space-y-1 px-2">
          {visibleItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive ? 'bg-hospital-primary text-white' : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                  }`
                }
              >
                <item.icon className="w-5 h-5 mr-3" />
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className="p-4 border-t border-gray-800">
        <button
          onClick={handleLogout}
          className="flex items-center w-full px-3 py-2 text-sm font-medium text-gray-300 rounded-md hover:bg-gray-800 hover:text-white transition-colors"
        >
          <LogOut className="w-5 h-5 mr-3" />
          Logout
        </button>
      </div>
    </div>
  );
};
