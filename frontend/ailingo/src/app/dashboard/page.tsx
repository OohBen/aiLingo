"use client";

import { useAuth } from "../../lib/useAuth";
import Link from "next/link";

export default function Dashboard() {
  const user = useAuth();

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-2xl font-bold">Loading...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Dashboard</h1>
      <p className="text-xl mb-8">Welcome, {user.name}!</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-blue-500 text-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-4">Lessons</h2>
          <p className="mb-4">Explore and learn new languages.</p>
          <Link href="/lessons">
            <button className="bg-white text-blue-500 font-bold py-2 px-4 rounded">
              Go to Lessons
            </button>
          </Link>
        </div>

        <div className="bg-green-500 text-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-4">Quizzes</h2>
          <p className="mb-4">Test your language skills with quizzes.</p>
          <Link href="/quizzes">
            <button className="bg-white text-green-500 font-bold py-2 px-4 rounded">
              Go to Quizzes
            </button>
          </Link>
        </div>

        <div className="bg-yellow-500 text-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-4">Chat</h2>
          <p className="mb-4">Practice conversational skills with chat.</p>
          <Link href="/chat">
            <button className="bg-white text-yellow-500 font-bold py-2 px-4 rounded">
              Go to Chat
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}