import React, { useState } from 'react';
import { SessionListItem } from '../types';

interface SessionListProps {
  sessions: SessionListItem[];
  onSelect: (session: SessionListItem) => void;
}

const SessionList: React.FC<SessionListProps> = ({ sessions, onSelect }) => {
  const [sortBy, setSortBy] = useState<'date' | 'status'>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  const sortedSessions = [...sessions].sort((a, b) => {
    if (sortBy === 'date') {
      return sortOrder === 'asc'
        ? new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
        : new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
    }
    return sortOrder === 'asc'
      ? a.status.localeCompare(b.status)
      : b.status.localeCompare(a.status);
  });

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between mb-3 p-2 bg-neutral-800/50 rounded">
        <div className="text-xs text-slate-400">Sort by:</div>
        <div className="flex gap-2 text-xs">
          <button
            onClick={() => {
              setSortBy('date');
              setSortOrder(sortBy === 'date' && sortOrder === 'asc' ? 'desc' : 'asc');
            }}
            className={`px-2 py-1 rounded ${
              sortBy === 'date'
                ? 'bg-cyan-500/20 text-cyan-400'
                : 'bg-neutral-800/50 text-slate-400 hover:bg-neutral-700'
            }`}
          >
            Date
          </button>
          <button
            onClick={() => {
              setSortBy('status');
              setSortOrder(sortBy === 'status' && sortOrder === 'asc' ? 'desc' : 'asc');
            }}
            className={`px-2 py-1 rounded ${
              sortBy === 'status'
                ? 'bg-cyan-500/20 text-cyan-400'
                : 'bg-neutral-800/50 text-slate-400 hover:bg-neutral-700'
            }`}
          >
            Status
          </button>
        </div>
      </div>
      {sortedSessions.length === 0 ? (
        <div className="text-center py-8 text-slate-400">
          No sessions found
        </div>
      ) : (
        <div className="space-y-2">
          {sortedSessions.map((session) => (
            <div
              key={session.id}
              onClick={() => onSelect(session)}
              className="cursor-pointer p-3 rounded-lg border bg-neutral-900/50 hover:bg-neutral-800/50 transition-colors"
            >
              <div className="flex justify-between items-start mb-1">
                <div className="font-medium text-slate-100">{session.task}</div>
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
              <div className="flex items-center gap-3 text-xs text-slate-400">
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-cyan-400" />
                  <span>{session.mode}</span>
                </span>
                <span>
                  <span className="w-2 h-2 rounded-full bg-yellow-400" />
                  <span>{session.tokensUsed} tokens</span>
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-green-400" />
                  <span>${session.cost.toFixed(2)}</span>
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SessionList;export { SessionList };
