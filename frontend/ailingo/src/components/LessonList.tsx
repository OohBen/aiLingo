import { Lesson } from '../types';

type LessonListProps = {
  lessons: Lesson[];
};

export function LessonList({ lessons }: LessonListProps) {
  return (
    <div className="space-y-4">
      {lessons.map((lesson) => (
        <div key={lesson.id} className="bg-white shadow-md rounded-lg p-4">
          <h2 className="text-xl font-semibold mb-2">{lesson.title}</h2>
          <p className="text-gray-600">{lesson.description}</p>
        </div>
      ))}
    </div>
  );
}