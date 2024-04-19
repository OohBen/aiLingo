import { Quiz } from '../types';
import Link from 'next/link';

type QuizListProps = {
  quizzes: Quiz[];
};

export function QuizList({ quizzes }: QuizListProps) {
  return (
    <div className="space-y-4">
      {quizzes.map((quiz) => (
        <div key={quiz.id} className="bg-white shadow-md rounded-lg p-4">
          <h2 className="text-xl font-semibold mb-2">
            <Link href={`/quizzes/${quiz.id}`} className="text-blue-600 hover:underline">
              {quiz.title}
            </Link>
          </h2>
          <p className="text-gray-600">{quiz.description}</p>
        </div>
      ))}
    </div>
  );
}