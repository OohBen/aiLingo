import { getLessons } from '../../lib/api';
import { LessonList } from '../../components/LessonList';

export default async function Lessons() {
  const lessons = await getLessons();

  return (
    <div>
      <h1>Lessons</h1>
      <LessonList lessons={lessons} />
    </div>
  );
}