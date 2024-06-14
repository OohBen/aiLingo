// 'use client';

import exp from "constants";

// import { useAuth } from '../../lib/useAuth';
// import { useEffect, useState } from 'react';
// import { getLessons } from '../../lib/api';
// import { LessonList } from '../../components/LessonList';

// export default function Lessons() {
//   const user = useAuth();
//   const [lessons, setLessons] = useState([]);

//   useEffect(() => {
//     const fetchLessons = async () => {
//       try {
//         const data = await getLessons();
//         setLessons(data);
//       } catch (error) {
//         console.error('Failed to fetch lessons', error);
//       }
//     };

//     if (user) {
//       fetchLessons();
//     }
//   }, [user]);

//   if (!user) {
//     return <div>Loading...</div>;
//   }

//   return (
//     <div>
//       <h1 className="text-2xl font-bold mb-4">Lessons</h1>
//       <LessonList lessons={lessons} />
//     </div>
//   );
// }

// Make a nice looking not implemented page
export default function Lessons() {
  return (
    <div className="flex items-center justify-center h-screen">
      <h1 className="text-4xl font-bold">Not implemented yet</h1>
    </div>
  );
}