import React, { useEffect, useState } from 'react';
import axiosInstance from '../utils/axiosInstance';

function Languages() {
  const [languages, setLanguages] = useState([]);

  useEffect(() => {
    fetchLanguages();
  }, []);

  const fetchLanguages = async () => {
    try {
      const response = await axiosInstance.get('http://localhost:8000/api/languages/');
      setLanguages(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="container">
      <h2>Languages</h2>
      <ul>
        {languages.map((language) => (
          <li key={language.id}>{language.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default Languages;