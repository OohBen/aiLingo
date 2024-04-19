import { getQuizzes } from '../../lib/api';
import { QuizList } from '../../components/QuizList';

export default async function Quizzes() {
  const quizzes = await getQuizzes();

  return (
    <div>
      <h1>Quizzes</h1>
      <QuizList quizzes={quizzes} />
    </div>
  );
}