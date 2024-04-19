'use client';

import { useAuth } from '../../lib/useAuth';

export default function Dashboard() {
  const user = useAuth();

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <p>Welcome, {user.name}!</p>
    </div>
  );
}