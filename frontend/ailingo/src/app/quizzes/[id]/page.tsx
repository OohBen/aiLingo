"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getQuizById } from "../../../lib/api";
import { QuizAttempt } from "../../../components/QuizAttempt";

export default function QuizPage({ params }: { params: { id: string } }) {
  const [user, setUser] = useState(null);
  const [quiz, setQuiz] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    } else {
      router.push("/login");
    }
  }, []);

  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const data = await getQuizById(params.id);
        setQuiz(data);
      } catch (error) {
        console.error("Failed to fetch quiz", error);
      }
    };

    if (user) {
      fetchQuiz();
    }
  }, [user, params.id]);

  if (!user || !quiz) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-2xl font-bold">Loading...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="bg-white text-black rounded-lg shadow-lg p-8">
        <h1 className=" text-4xl font-bold mb-8">{quiz.title}</h1>
        <QuizAttempt quiz={quiz} />
      </div>
    </div>
  );
}
