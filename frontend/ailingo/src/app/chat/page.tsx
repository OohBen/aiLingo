'use client';

import { useAuth } from '../../lib/useAuth';
import { ChatInterface } from '../../components/ChatInterface';

export default function Chat() {
  const user = useAuth();

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Chat</h1>
      <ChatInterface />
    </div>
  );
}