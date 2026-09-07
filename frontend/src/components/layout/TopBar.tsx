import React, { useState, useEffect } from 'react';
import { Bell, Search } from 'lucide-react';
import { useWebSocketContext } from '../../context/WebSocketContext';
import { SyntheticDataBanner } from '../common/SyntheticDataBanner';

export const TopBar: React.FC = () => {
  const [time, setTime] = useState(new Date());
  const { isConnected } = useWebSocketContext();

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex flex-col w-full z-10 sticky top-0">
      <SyntheticDataBanner />
      <header className="bg-white border-b border-gray-200 h-16 flex items-center justify-between px-6">
        <div className="flex items-center">
          <h2 className="text-lg font-semibold text-gray-800 hidden md:block">Hospital Operations Command Center</h2>
        </div>

        <div className="flex items-center space-x-6">
          <div className="hidden md:flex items-center bg-gray-100 rounded-md px-3 py-1.5">
            <Search className="w-4 h-4 text-gray-500 mr-2" />
            <input type="text" placeholder="Search..." className="bg-transparent border-none focus:ring-0 text-sm text-gray-700 w-48" />
          </div>

          <div className="flex flex-col items-end">
            <span className="text-sm font-medium text-gray-700">{time.toLocaleTimeString()}</span>
            <span className="text-xs text-gray-500">{time.toLocaleDateString()}</span>
          </div>

          <div className="flex items-center" title={isConnected ? 'WebSocket Connected' : 'WebSocket Disconnected'}>
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-gray-400'}`}></div>
          </div>

          <button className="relative p-2 text-gray-400 hover:text-gray-500">
            <Bell className="w-6 h-6" />
            <span className="absolute top-1.5 right-1.5 block w-2 h-2 rounded-full bg-red-500 ring-2 ring-white"></span>
          </button>
        </div>
      </header>
    </div>
  );
};
