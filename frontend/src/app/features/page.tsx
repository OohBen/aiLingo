'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getLanguages } from '../services/api';

const Homepage = () => {
  const [languages, setLanguages] = useState([]);
  const router = useRouter();

  useEffect(() => {
    const fetchLanguages = async () => {
      const data = await getLanguages();
      setLanguages(data);
    };

    fetchLanguages();
  }, []);

  const handleLanguageClick = (languageId) => {
    // Navigate to the language page with the selected language ID
    router.push(`/languages/${languageId}`);
  };

  return (
    <div className="flex flex-col items-stretch bg-blue-600 min-h-screen">
      <h1 className="text-4xl font-bold mb-8 p-8 text-center text-white">
        Languages
      </h1>
      <div className="flex flex-col space-y-4 p-8">
        {languages.map((language) => (
          <button
            key={language.id}
            onClick={() => handleLanguageClick(language.id)}
            className="py-4 bg-blue-500 text-white text-xl font-semibold rounded-md hover:bg-blue-400 transition-colors duration-300"
          >
            {language.name}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Homepage;