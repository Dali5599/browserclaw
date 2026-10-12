import React, { useState, useEffect, useRef } from 'react';
import { useWebSocket } from '../components/LiveViewport';

interface ActionTimelineProps {
  sessionId: string | null;
  onSelect: (id: string | null) => void;
}

const ActionTimeline: React.FC<ActionTimelineProps> = ({ sessionId, onSelect }) => {
  const [actions, setActions] = useState<Array<{id: string, type: string, target: string, timestamp: string, status: string, duration?: number, error?: string, result?: unknown}>>([]);
  const [selectedAction, setSelectedAction] = useState<{id: string, type: string, target: string, timestamp: string, status: string, duration?: number, error?: string, result?: unknown} | null>(null);
  const [isBusy, setIsBusy] = useState(false);
  const timelineRef = useRef<HTMLDivElement>(null);

  // Simulate action timeline
  useEffect(() => {
    const generateActions = () => {
      const now = new Date().toISOString();
      const newAction: {id: string, type: string, target: string, timestamp: string, status: string, duration?: number, error?: string, result?: unknown} = {
        id: `action-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        type: ['click', 'type', 'navigate', 'scroll', 'wait', 'extract', 'screenshot', 'evaluate'][Math.floor(Math.random() * 8)],
        target: `session-${sessionId || 'unknown'}`,
        timestamp: now,
        status: ['pending', 'running', 'completed', 'failed'][Math.floor(Math.random() * 4)],
        duration: Math.floor(Math.random() * 5000),
        error: Math.random() > 0.8 ? 'Timeout waiting for element' : undefined,
        result: { success: true, duration: Math.floor(Math.random() * 5000) },
      };
      setActions([newAction, ...actions]);
      setSelectedAction(newAction);
      setIsBusy(true);
      const timer = setTimeout(() => {
        setIsBusy(false);
      }, 2000);
      return () => clearTimeout(timer);
    };

    generateActions();
  }, [sessionId, actions]);

  const handleSelect = (id: string | null) => {
    if (id) {
      const action = actions.find(a => a.id === id);
      if (action) {
        setSelectedAction(action);
      }
    }
  };

  return (
    <div className="glass-card rounded-lg p-4">
      <h2 className="text-sm font-semibold text-slate-300 mb-4">Action Timeline</h2>
      {isBusy ? (
        <div className="flex items-center justify-between p-2 bg-neutral-800/50 rounded">
          <span>Generating actions...</span>
          <span className="text-xs text-cyan-400">Processing...</span>
        </div>
      ) : (
        <div className="prose prose-mono text-sm leading-relaxed">
          {actions.map((action, index) => (
            <div key={action.id} className="mb-3 p-2 bg-neutral-900/50 rounded-lg">
              <div className="flex justify-between items-start mb-1">
                <span className="text-xs text-slate-400">#{action.id}</span>
                <span className="text-xs text-cyan-400">{action.status}</span>
              </div>
              <div className="text-xs text-slate-300">{action.type}: {action.target}</div>
            </div>
          ))}
        </div>
      )}
      <div className="mt-4 pt-4 border-t border-cyan-500/30">
        <p className="text-xs text-slate-500">Last active action: {actions.length > 0 ? actions[0]?.type : 'No actions yet'}</p>
      </div>
    </div>
  );
};

export default ActionTimeline;export { ActionTimeline };
