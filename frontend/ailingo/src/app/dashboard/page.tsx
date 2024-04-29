"use client";

import { useAuth } from "../../lib/useAuth";
import Link from "next/link";
import { useEffect, useState } from "react";
import { getQuizzes } from "../../lib/api";

export default function Dashboard() {
  const user = useAuth();
  const [quizzes, setQuizzes] = useState([]);

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        const data = await getQuizzes();
        setQuizzes(data);
      } catch (error) {
        console.error("Failed to fetch quizzes", error);
      }
    };

    if (user) {
      fetchQuizzes();
    }
  }, [user]);

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-2xl font-bold">Loading...</div>
      </div>
    );
  }

  const lastThreeQuizzes = quizzes.slice(-3).reverse();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Dashboard</h1>
      <p className="text-xl mb-8">Welcome, {user.name}!</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-blue-500 text-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-4">Quizzes</h2>
          <p className="mb-4">Test your language skills with quizzes.</p>
          <Link href="/lessons">
            <button className="bg-white text-blue-500 font-bold py-2 px-4 rounded">
              Go to Lessons
            </button>
          </Link>
        </div>

        <div className="bg-green-500 text-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-4">Lessons</h2>
          <p className="mb-4">Explore and learn new languages.</p>
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

      {lastThreeQuizzes.length > 0 && (
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4">Recently Attempted Quizzes</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {lastThreeQuizzes.map((quiz) => (
              <div
                key={quiz.id}
                className="bg-blue-500 text-white rounded-lg shadow-lg p-4"
              >
                <p className="text-lg mb-2">{quiz.title}</p>
                <Link href={`/quizzes/${quiz.id}`}>
                  <button className="bg-white text-blue-500 font-bold py-1 px-2 rounded">
                    Resume Quiz
                  </button>
                </Link>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}