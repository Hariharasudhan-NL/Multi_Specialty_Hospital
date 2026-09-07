import { useEffect, useRef, useState, useCallback } from 'react';

export function useWebSocket(url: string) {
  const ws = useRef<WebSocket | null>(null);
  const [lastMessage, setLastMessage] = useState<any>(null);
  const [isConnected, setIsConnected] = useState(false);

  const connect = useCallback(() => {
    const token = localStorage.getItem('access_token');
    ws.current = new WebSocket(`${url}?token=${token}`);
    ws.current.onopen = () => setIsConnected(true);
    ws.current.onmessage = (e) => setLastMessage(JSON.parse(e.data));
    ws.current.onclose = () => {
      setIsConnected(false);
      setTimeout(connect, 3000); // Reconnect
    };
  }, [url]);

  useEffect(() => { connect(); return () => ws.current?.close(); }, [connect]);
  return { lastMessage, isConnected };
}
