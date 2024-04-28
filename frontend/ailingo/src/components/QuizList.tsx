import { Quiz } from '../types';
import Link from 'next/link';

type QuizListProps = {
  quizzes: Quiz[];
};

export function QuizList({ quizzes }: QuizListProps) {
  return (
    <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {quizzes.map((quiz) => (
        <li key={quiz.id} className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">
              <Link href={`/quizzes/${quiz.id}`} className="text-blue-600 hover:text-blue-800">
                {quiz.title}
              </Link>
            </h2>
            <p className="text-gray-600 mb-4">{quiz.description}</p>
            <Link href={`/quizzes/${quiz.id}`}>
              <button className="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-600">
                Start Quiz
              </button>
            </Link>
          </div>
        </li>
      ))}
    </ul>
  );
}