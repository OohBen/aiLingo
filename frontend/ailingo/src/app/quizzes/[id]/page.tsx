import { getQuizById } from '../../../lib/api';
import { QuizAttempt } from '../../../components/QuizAttempt';

export default async function QuizPage({ params }: { params: { id: string } }) {
  const quiz = await getQuizById(params.id);

  return (
    <div>
      <h1>{quiz.title}</h1>
      <QuizAttempt quiz={quiz} />
    </div>
  );
}