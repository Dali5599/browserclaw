import { Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import SessionList from './pages/SessionList';
import SessionDetail from './pages/SessionDetail';
import { useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { WSMessage } from './types';

function App() {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  // Initialize WebSocket connection
  const initSocket = () => {
    const socketInstance = io(import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001', {
      transports: ['websocket'],
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    socketInstance.on('connect', () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    });

    socketInstance.on('disconnect', () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    });

    socketInstance.on('connect_error', (err) => {
      console.error('WebSocket connection error:', err);
      setIsConnected(false);
    });

    setSocket(socketInstance);
  };

  // Cleanup socket on unmount
  // eslint-disable-next-line react-hooks/exhaustive-deps
  React.useEffect(() => {
    initSocket();
    return () => {
      socket?.disconnect();
    };
  }, []);

  return (
    <div className="min-h-screen bg-cyber-bg text-slate-100">
      <div className="relative">
        <div className="scanline"></div>
        <Routes>
          <Route path="/" element={<Dashboard socket={socket} isConnected={isConnected} />} />
          <Route path="/sessions" element={<SessionList socket={socket} isConnected={isConnected} />} />
          <Route path="/sessions/:id" element={<SessionDetail socket={socket} isConnected={isConnected} />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;