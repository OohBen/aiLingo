'use client';

import React, { useEffect, useState } from 'react';
import { getLanguages } from '../services/api';

const Homepage = () => {
  const [languages, setLanguages] = useState([]);

  useEffect(() => {
    const fetchLanguages = async () => {
      const data = await getLanguages();
      setLanguages(data);
    };

    fetchLanguages();
  }, []);

  return (
    <div>
      <h1>Languages</h1>
      <ul>
        {languages.map((language) => (
          <li key={language.id}>{language.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default Homepage;
