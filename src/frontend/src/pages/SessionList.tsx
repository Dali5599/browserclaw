import React from 'react';
import { SessionListItem } from '../types';
import { SessionList } from '../components/SessionList';

interface SessionListPageProps {
  sessions: SessionListItem[];
  onSelect: (session: SessionListItem) => void;
}

const SessionListPage: React.FC<SessionListPageProps> = ({ sessions, onSelect }) => {
  return (
    <div className="min-h-screen bg-cyber-bg">
      <header className="sticky top-0 z-50 bg-cyber-card/90 backdrop-blur-md border-b border-cyber-border">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-xl font-bold text-white tracking-wider">BrowserClaw Sessions</h1>
          <p className="text-sm text-slate-400 mt-1">Review and manage your agent sessions</p>
        </div>
      </header>
      <main className="container mx-auto px-4 py-6">
        <div className="glass-card rounded-xl overflow-hidden">
          <div className="p-6">
            <SessionList sessions={sessions} onSelect={onSelect} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default SessionListPage;