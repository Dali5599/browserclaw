import React, { useState } from 'react';

interface TaskInputProps {
  onSelect: (id: string | null) => void;
}

const TaskInput: React.FC<TaskInputProps> = ({ onSelect }) => {
  const [task, setTask] = useState('');
  const [mode, setMode] = useState<'strict' | 'monitor' | 'permissive'>('monitor');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = () => {
    if (!task.trim()) return;
    setIsGenerating(true);
    // Simulate generating a task
    setTimeout(() => {
      setIsGenerating(false);
      const newTask = {
        id: `task-${Date.now()}`,
        description: task,
        status: 'running',
      };
      // Add to active tasks
      const event = new CustomEvent('taskAdded', { detail: newTask });
      window.dispatchEvent(event);
      setTask('');
    }, 2000);
  };

  const handleStop = () => {
    const event = new CustomEvent('taskStopped');
    window.dispatchEvent(event);
  };

  return (
    <div className="bg-cyber-card rounded-lg p-3">
      <label htmlFor="task-input" className="block text-xs font-medium text-slate-300 mb-2">
        Your task (what should the AI agent do in the browser?)
      </label>
      <textarea
        id="task-input"
        rows={3}
        value={task}
        onChange={(e) => setTask(e.target.value)}
        placeholder="E.g., Find the best price for a laptop on Amazon and add it to my wishlist..."
        className="w-full bg-neutral-900 border border-cyber-border rounded-lg px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent resize-none"
      />
      <div className="mt-2">
        <span className="block text-xs font-medium text-slate-300 mb-1">Mode</span>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setMode('strict')}
            className={`flex-1 py-1.5 px-2 text-xs rounded-lg border transition-colors ${
              mode === 'strict'
                ? 'bg-cyber-neonCyan text-cyber-bg border-cyber-neonCyan'
                : 'bg-neutral-900 border-neutral-700 text-slate-400 hover:border-neutral-500'
            }`}
          >
            Strict
          </button>
          <button
            type="button"
            onClick={() => setMode('monitor')}
            className={`flex-1 py-1.5 px-2 text-xs rounded-lg border transition-colors ${
              mode === 'monitor'
                ? 'bg-cyber-neonCyan text-cyber-bg border-cyber-neonCyan'
                : 'bg-neutral-900 border-neutral-700 text-slate-400 hover:border-neutral-500'
            }`}
          >
            Monitor
          </button>
          <button
            type="button"
            onClick={() => setMode('permissive')}
            className={`flex-1 py-1.5 px-2 text-xs rounded-lg border transition-colors ${
              mode === 'permissive'
                ? 'bg-cyber-neonCyan text-cyber-bg border-cyber-neonCyan'
                : 'bg-neutral-900 border-neutral-700 text-slate-400 hover:border-neutral-500'
            }`}
          >
            Permissive
          </button>
        </div>
      </div>
      {isGenerating ? (
        <button
          type="button"
          onClick={handleStop}
          className="w-full mt-3 py-2 px-4 rounded-lg bg-red-500/20 text-red-400 border border-red-500/50 text-sm font-medium hover:bg-red-500/30 transition-colors"
        >
          Stop Agent
        </button>
      ) : (
        <button
          type="button"
          onClick={handleGenerate}
          disabled={!task.trim()}
          className="w-full mt-3 py-2 px-4 rounded-lg bg-cyber-neonCyan text-cyber-bg text-sm font-medium hover:bg-cyber-neonCyan/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Start Agent
        </button>
      )}
    </div>
  );
};

export default TaskInput;export { TaskInput };
