import React, { useState } from 'react';
import { Session } from '../types';

interface SessionDetailProps {
  session: Session;
  actions: Array<{id: string, type: string, target: string, status: string, timestamp: string}>,
  thoughts: Array<{id: string, content: string, timestamp: string}>,
}

const SessionDetail: React.FC<SessionDetailProps> = ({ session, actions, thoughts }) => {
  return (
    <div className="space-y-4">
      {/* Status Card */}
      <div className="glass-card rounded-lg p-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-white">{session.task}</h2>
          <span
            className={`px-2 py-0.5 rounded text-xs ${
              session.status === 'running'
                ? 'bg-green-500/20 text-green-400'
                : session.status === 'completed'
                ? 'bg-blue-500/20 text-blue-400'
                : session.status === 'failed'
                ? 'bg-red-500/20 text-red-400'
                : session.status === 'paused'
                ? 'bg-yellow-500/20 text-yellow-400'
                : 'bg-cyan-500/20 text-cyan-400'
            }`}
          >
            {session.status}
          </span>
        </div>
        <div className="mt-2 text-sm text-slate-300">
          Mode: <span className="font-medium">{session.mode}</span>
        </div>
        <div className="mt-2 text-sm text-slate-300">
          Steps: <span className="font-medium">{session.steps}</span>
        </div>
      </div>

      {/* Actions Tab */}
      <div className="glass-card rounded-lg p-4">
        <h3 className="text-sm font-semibold text-slate-300 mb-3">Actions</h3>
        <div className="space-y-2">
          {actions.map((action) => (
            <div
              key={action.id}
              className="p-2 bg-neutral-900/50 rounded"
            >
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-xs font-medium text-cyan-400">{action.type}</span>
                  <span className="text-xs text-slate-400"> → {action.target}</span>
                </div>
                <span className="text-xs text-slate-500">
                  {new Date(action.timestamp).toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Thoughts Tab */}
      <div className="glass-card rounded-lg p-4">
        <h3 className="text-sm font-semibold text-slate-300 mb-3">Thoughts</h3>
        <div className="space-y-2">
          {thoughts.map((thought) => (
            <div
              key={thought.id}
              className="p-2 bg-neutral-900/50 rounded"
            >
              <div className="flex justify-between items-start">
                <span className="text-xs text-slate-300">{thought.content}</span>
                <span className="text-xs text-slate-500">
                  {new Date(thought.timestamp).toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="glass-card rounded-lg p-4">
        <h3 className="text-sm font-semibold text-slate-300 mb-3">Session Stats</h3>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-xl font-bold text-cyan-400">{session.tokensUsed}</div>
            <div className="text-xs text-slate-400">Tokens Used</div>
          </div>
          <div>
            <div className="text-xl font-bold text-yellow-400">${session.cost.toFixed(2)}</div>
            <div className="text-xs text-slate-400">Cost</div>
          </div>
          <div>
            <div className="text-xl font-bold text-green-400">{session.steps}</div>
            <div className="text-xs text-slate-400">Steps</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SessionDetail;export { SessionDetail };
