import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { ActionTimeline } from '../components/ActionTimeline';
import { SessionDetail } from '../components/SessionDetail';

const SessionDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [session, setSession] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSession = async () => {
      setLoading(true);
      try {
        const res = await fetch(`/api/sessions/${id}`);
        if (res.ok) {
          const data = await res.json();
          setSession(data);
        } else {
          console.error('Session not found');
        }
      } catch (err) {
        console.error('Error fetching session:', err);
      }
      setLoading(false);
    };
    fetchSession();
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-500"></div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-slate-400">Session not found</p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <SessionDetail session={session} />
      <h2 className="text-xl font-bold text-white mb-4 mt-8">Action Timeline</h2>
      <ActionTimeline sessionId={id || ''} />
    </div>
  );
};

export default SessionDetailPage;