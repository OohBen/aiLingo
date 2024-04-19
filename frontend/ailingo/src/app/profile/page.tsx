'use client';

import { useAuth } from '../../lib/useAuth';

export default function Profile() {
  const user = useAuth();

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Profile</h1>
      <p>Name: {user.name}</p>
      <p>Email: {user.email}</p>
    </div>
  );
}