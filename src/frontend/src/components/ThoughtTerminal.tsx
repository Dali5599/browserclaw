import React, { useState, useEffect, useRef } from 'react';
import { useWebSocket } from '../components/LiveViewport';

interface ThoughtTerminalProps {
  sessionId: string | null;
  onSelect: (id: string | null) => void;
}

const ThoughtTerminal: React.FC<ThoughtTerminalProps> = ({ sessionId, onSelect }) => {
  const [thoughts, setThoughts] = useState<Array<{id: string, content: string, timestamp: string, type: string, step: number}>>([]);
  const [currentThought, setCurrentThought] = useState<{id: string, content: string, timestamp: string, type: string, step: number} | null>(null);
  const [isBusy, setIsBusy] = useState(false);
  const thoughtRef = useRef<HTMLDivElement>(null);

  // Simulate thought generation
  useEffect(() => {
    const generateThoughts = () => {
      const now = new Date().toISOString();
      const newThought: {id: string, content: string, timestamp: string, type: string, step: number} = {
        id: `thought-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        content: `Step ${currentThought ? currentThought.step + 1 : 1}: Analyzing session ${sessionId || 'unknown'} for potential optimizations.`,
        timestamp: now,
        type: 'reasoning',
        step: currentThought ? currentThought.step + 1 : 1,
      };
      setThoughts([newThought, ...thoughts]);
      setCurrentThought(newThought);
      setIsBusy(true);
      // Simulate delay
      const timer = setTimeout(() => {
        setIsBusy(false);
      }, 1500);
      return () => clearTimeout(timer);
    };

    generateThoughts();
  }, [sessionId, currentThought]);

  const handleSelect = (id: string | null) => {
    if (id) {
      setCurrentThought(id);
      setThoughts([]);
    }
  };

  return (
    <div className="glass-card rounded-lg p-4">
      <h2 className="text-sm font-semibold text-slate-300 mb-4">Agent Thought Terminal</h2>
      {isBusy ? (
        <div className="flex items-center justify-between p-2 bg-neutral-800/50 rounded">
          <span>Generating thoughts...</span>
          <span className="text-xs text-cyan-400">Processing...</span>
        </div>
      ) : (
        <div className="prose prose-mono text-sm leading-relaxed">
          {thoughts.map((thought, index) => (
            <div key={thought.id} className="mb-3 p-2 bg-neutral-900/50 rounded-lg">
              <div className="flex justify-between items-start mb-1">
                <span className="text-xs text-slate-400">#{thought.id}</span>
                <span className="text-xs text-cyan-400">Step {thought.step}</span>
              </div>
              <div className="text-xs text-slate-300">{thought.content}</div>
            </div>
          ))}
        </div>
      )}
      <div className="mt-4 pt-4 border-t border-cyan-500/30">
        <p className="text-xs text-slate-500">Last active thought: {thoughts.length > 0 ? thoughts[0]?.content : 'No thoughts yet'}</p>
      </div>
    </div>
  );
};

export default ThoughtTerminal;