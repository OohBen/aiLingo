'use client';

import { useAuth } from '../../../lib/useAuth';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createQuiz } from '../../../lib/api';

export default function CreateQuiz() {
  const user = useAuth();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    try {
      await createQuiz({ title, description });
      router.push('/quizzes');
    } catch (error) {
      setError('An error occurred while creating the quiz. Please try again.');
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
            className="w-full px-3 py-2 border border-gray-300 rounded"
          />
        </div>
        <div>
          <label htmlFor="description" className="block mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded"
          ></textarea>
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