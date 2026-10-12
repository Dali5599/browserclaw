import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { socket } from '../services/socket';
import { LiveViewport } from '../components/LiveViewport';
import { ThoughtTerminal } from '../components/ThoughtTerminal';
import { ActionTimeline } from '../components/ActionTimeline';
import { TaskInput } from '../components/TaskInput';
import { Session, BoundingBox, ViewportSnapshot, Thought, Action, TokenStats, SessionListItem } from '../types';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [activeFrame, setActiveFrame] = useState<ViewportSnapshot | null>(null);
  const [boundingBoxes, setBoundingBoxes] = useState<BoundingBox[]>([]);
  const [thoughts, setThoughts] = useState<Thought[]>([]);
  const [actions, setActions] = useState<Action[]>([]);
  const [tokenStats, setTokenStats] = useState<TokenStats>({
    totalTokens: 0,
    promptTokens: 0,
    completionTokens: 0,
    totalCost: 0,
    sessionsCount: 0,
  });
  const [selectedSession, setSelectedSession] = useState<Session | null>(null);
  const [isSending, setIsSending] = useState(false);
  const [sessionStatus, setSessionStatus] = useState<string>('idle');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load sessions data (mock)
  useEffect(() => {
    const mockSessions: Session[] = [
      {
        id: '1',
        task: 'Find the best laptop prices on Amazon',
        status: 'completed',
        mode: 'strict',
        createdAt: new Date(Date.now() - 3600000).toISOString(),
        updatedAt: new Date(Date.now() - 3600000).toISOString(),
        completedAt: new Date(Date.now() - 3600000).toISOString(),
        tokensUsed: 1240,
        cost: 0.05,
        steps: 5,
        currentUrl: 'https://www.amazon.com',
        actions: [],
        thoughts: [],
      },
      {
        id: '2',
        task: 'Research AI trends for Q4 2024',
        status: 'running',
        mode: 'monitor',
        createdAt: new Date(Date.now() - 1800000).toISOString(),
        updatedAt: new Date(Date.now() - 1800000).toISOString(),
        startedAt: new Date(Date.now() - 1800000).toISOString(),
        tokensUsed: 450,
        cost: 0.02,
        steps: 2,
        currentUrl: 'https://news.ycombinator.com',
        actions: [],
        thoughts: [],
      },
    ];
    setActions(mockSessions.map((s) => ({
      id: s.id,
      sessionId: s.id,
      type: 'navigate',
      target: 'https://www.amazon.com',
      params: {},
      status: 'completed',
      startedAt: s.createdAt,
      completedAt: s.completedAt,
      duration: 1200,
      result: { success: true },
    })));
    setThoughts(mockSessions.map((s) => ({
      id: s.id,
      sessionId: s.id,
      content: `Started session for task: ${s.task}`,
      timestamp: s.createdAt,
      type: 'reasoning',
      step: 1,
    })));
  }, []);

  // Connect WebSocket
  useEffect(() => {
    const handleConnection = () => {
      setSessionStatus('connected');
      console.log('WebSocket connected to Dashboard');
    };

    const handleViewport = (frame: ViewportSnapshot) => {
      setActiveFrame(frame);
      setBoundingBoxes(frame.boundingBoxes || []);
    };

    const handleThought = (thought: Thought) => {
      setThoughts((prev) => [...prev, thought]);
    };

    const handleAction = (action: Action) => {
      setActions((prev) => [action, ...prev]);
    };

    const handleSessionUpdate = (session: Session) => {
      setSelectedSession(session);
      setSessionStatus(session.status);
    };

    const handleStats = (stats: TokenStats) => {
      setTokenStats(stats);
    };

    socket.on('connection', handleConnection);
    socket.on('viewport', handleViewport);
    socket.on('thought', handleThought);
    socket.on('action', handleAction);
    socket.on('session_update', handleSessionUpdate);
    socket.on('stats', handleStats);

    return () => {
      socket.off('connection', handleConnection);
      socket.off('viewport', handleViewport);
      socket.off('thought', handleThought);
      socket.off('action', handleAction);
      socket.off('session_update', handleSessionUpdate);
      socket.off('stats', handleStats);
    };
  }, []);

  // Auto-scroll to bottom of thought terminal
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [thoughts]);

  // Handle task submission
  const handleTaskSubmit = useCallback(
    async (taskText: string, mode: 'strict' | 'monitor' | 'permissive') => {
      if (!taskText.trim() || isSending) return;

      try {
        setIsSending(true);
        await socket.emit('start_session', { task: taskText, mode });
      } catch (error) {
        console.error('Error starting session:', error);
      } finally {
        setTimeout(() => {
          setIsSending(false);
        }, 3000);
      }
    },
    [isSending]
  );

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-cyber-card/90 backdrop-blur-md border-b border-cyber-border">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-cyber-neonCyan to-blue-600 flex items-center justify-center">
              <span className="text-xl font-bold text-cyber-bg">B</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white tracking-wider">BrowserClaw</h1>
              <p className="text-xs text-slate-400">Autonomous AI Browser Agent</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate('/sessions')}
              className="btn btn-secondary px-3 py-1.5 text-sm"
            >
              Sessions
            </button>
            <button className="btn btn-secondary px-3 py-1.5 text-sm">
              Settings
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 container mx-auto px-4 py-6 overflow-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Panel - Task Input & Stats */}
          <section className="lg:col-span-4 xl:col-span-3 space-y-6">
            <TaskInput onSelect={setSelectedSession} />

            {/* Session Status */}
            <div className="glass-card rounded-lg p-4">
              <h2 className="text-sm font-semibold text-slate-300 mb-3">Session Status</h2>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs text-slate-400">Status</span>
                <span
                  className={`px-2 py-0.5 rounded text-xs ${
                    sessionStatus === 'running'
                      ? 'bg-green-500/20 text-green-400'
                      : sessionStatus === 'idle'
                      ? 'bg-cyan-500/20 text-cyan-400'
                      : sessionStatus === 'completed'
                      ? 'bg-blue-500/20 text-blue-400'
                      : sessionStatus === 'failed'
                      ? 'bg-red-500/20 text-red-400'
                      : sessionStatus === 'paused'
                      ? 'bg-yellow-500/20 text-yellow-400'
                      : 'bg-slate-500/20 text-slate-400'
                  }`}
                >
                  {sessionStatus}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-400">Current URL</span>
                <span className="text-xs text-slate-300 truncate max-w-[150px]">
                  {activeFrame?.url || '-'}
                </span>
              </div>
            </div>

            {/* Token/Cost Stats */}
            <div className="glass-card rounded-lg p-4">
              <h2 className="text-sm font-semibold text-slate-300 mb-3">Usage Stats</h2>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 bg-cyber-bg/50 rounded-lg">
                  <span className="text-xs text-slate-400">Sessions</span>
                  <span className="text-xl font-bold text-cyber-neonCyan">{tokenStats.sessionsCount}</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-cyber-bg/50 rounded-lg">
                  <span className="text-xs text-slate-400">Total Tokens</span>
                  <span className="text-xl font-bold text-cyber-neonYellow">{tokenStats.totalTokens}</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-cyber-bg/50 rounded-lg">
                  <span className="text-xs text-slate-400">Prompt Tokens</span>
                  <span className="text-xl font-bold text-cyber-neonCyan">{tokenStats.promptTokens}</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-cyber-bg/50 rounded-lg">
                  <span className="text-xs text-slate-400">Completion Tokens</span>
                  <span className="text-xl font-bold text-cyber-neonCyan">{tokenStats.completionTokens}</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-cyber-bg/50 rounded-lg">
                  <span className="text-xs text-slate-400">Total Cost</span>
                  <span className="text-xl font-bold text-cyber-neonGreen">
                    ${tokenStats.totalCost.toFixed(3)}
                  </span>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="glass-card rounded-lg p-4">
              <h2 className="text-sm font-semibold text-slate-300 mb-3">Quick Actions</h2>
              <div className="flex flex-col gap-2">
                <button className="btn btn-secondary w-full justify-start text-sm" disabled>
                  Pause Session
                </button>
                <button className="btn btn-secondary w-full justify-start text-sm" disabled>
                  Resume Session
                </button>
                <button className="btn btn-secondary w-full justify-start text-sm" disabled>
                  Export Session
                </button>
              </div>
            </div>
          </section>

          {/* Center - Live Viewport */}
          <section className="lg:col-span-8 xl:col-span-9 space-y-6">
            {/* Live Browser Viewport */}
            <div className="glass-card rounded-xl overflow-hidden border border-cyber-neonCyan/30 shadow-neon">
              <div className="p-3 bg-cyber-bg/80 border-b border-cyber-border flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500" />
                  <div className="w-3 h-3 rounded-full bg-green-500" />
                </div>
                <div className="text-xs text-slate-400">
                  {activeFrame?.url || 'Waiting for session...'}
                </div>
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${sessionStatus === 'connected' ? 'bg-green-500' : 'bg-red-500'}`} />
                  <span className="text-xs text-slate-400">{sessionStatus === 'connected' ? 'WS: Connected' : 'WS: Connecting...'}</span>
                </div>
              </div>
              <div className="relative aspect-video bg-cyber-bg">
                {activeFrame ? (
                  <>
                    <img
                      src={activeFrame.frameBase64}
                      alt="Browser viewport"
                      className="w-full h-full object-contain"
                    />
                    {activeFrame.boundingBoxes &&
                      activeFrame.boundingBoxes.map((box) => (
                        <div
                          key={`${box.x}-${box.y}-${box.width}-${box.height}`}
                          className="absolute border-2 border-cyber-neonCyan rounded pointer-events-none transition-all duration-300"
                          style={{
                            left: `${box.x}px`,
                            top: `${box.y}px`,
                            width: `${box.width}px`,
                            height: `${box.height}px`,
                            boxShadow: '0 0 10px rgba(0, 240, 255, 0.3)',
                          }}
                        >
                          {box.isInteractive && (
                            <span className="absolute -top-5 left-0 text-xs bg-cyber-neonCyan text-cyber-bg px-1.5 rounded font-medium">
                              {box.tagName}
                            </span>
                          )}
                        </div>
                      ))}
                  </>
                ) : (
                  <div className="absolute inset-0 flex flex-col items-center justify-center gap-4">
                    <div className="w-16 h-16 rounded-full bg-gradient-to-br from-cyber-neonCyan/20 to-blue-600/20 flex items-center justify-center">
                      <div className="w-3 h-3 bg-cyber-neonCyan rounded-full animate-pulse" />
                    </div>
                    <p className="text-sm text-slate-400">Ready to start a session</p>
                    <p className="text-xs text-slate-500">Enter a task above to launch the AI browser agent</p>
                  </div>
                )}
              </div>
            </div>

            {/* Live Actions Timeline */}
            <div className="glass-card rounded-xl overflow-hidden border border-cyber-border">
              <div className="p-4 border-b border-cyber-border flex items-center justify-between">
                <h2 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
                  <span className="w-2 h-2 bg-cyber-neonCyan rounded-full" />
                  Live Action Log
                </h2>
                <span className="text-xs text-slate-400">{actions.length} actions</span>
              </div>
              <div className="max-h-64 overflow-y-auto p-2">
                {actions.length === 0 ? (
                  <div className="text-center py-8">
                    <p className="text-sm text-slate-500">No actions yet</p>
                    <p className="text-xs text-slate-600 mt-1">Actions will appear here as the agent works</p>
                  </div>
                ) : (
                  actions.slice(0, 20).map((action) => (
                    <div key={action.id} className="p-3 mb-2 bg-cyber-bg/50 rounded-lg border border-cyber-border/50">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-medium text-cyber-neonCyan">{action.type.toUpperCase()}</span>
                        <span
                          className={`text-xs px-2 py-0.5 rounded ${
                            action.status === 'running'
                              ? 'bg-green-500/20 text-green-400'
                              : action.status === 'completed'
                              ? 'bg-blue-500/20 text-blue-400'
                              : action.status === 'failed'
                              ? 'bg-red-500/20 text-red-400'
                              : 'bg-yellow-500/20 text-yellow-400'
                          }`}
                        >
                          {action.status}
                        </span>
                      </div>
                      <div className="text-xs text-slate-300">{action.target}</div>
                      <div className="text-xs text-slate-500 mt-1">
                        {new Date(action.startedAt).toLocaleTimeString()}
                        {action.duration && ` • ${action.duration}ms`}
                      </div>
                    </div>
                  ))
                )}
                <div ref={messagesEndRef} />
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;