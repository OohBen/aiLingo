// src/app/quizzes/create/page.tsx
"use client";

import { useAuth } from "../../../lib/useAuth";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { createQuiz, getLanguages } from "../../../lib/api";

export default function CreateQuiz() {
  const user = useAuth();
  const [title, setTitle] = useState("");
  const [language, setLanguage] = useState("");
  const [languages, setLanguages] = useState([]);
  const [error, setError] = useState("");
  const router = useRouter();

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const data = await getLanguages();
        setLanguages(data);
      } catch (error) {
        console.error("Failed to fetch languages:", error);
      }
    };

    fetchLanguages();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await createQuiz({ title, language });
      router.push("/quizzes");
    } catch (error) {
      setError("An error occurred while creating the quiz. Please try again.");
    }
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Create Quiz</h1>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block mb-1">
            Title
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded text-black"
          />
        </div>
        <div>
          <label htmlFor="language" className="block mb-1">
            Language
          </label>
          <select
            id="language"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded text-black"
          >
            <option value="">Select Language</option>
            {languages.map((lang) => (
              <option key={lang.id} value={lang.id}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>
        <button
          type="submit"
          className="w-full bg-blue-500 text-white px-4 py-2 rounded"
        >
          Create
        </button>
      </form>
    </div>
  );
}
