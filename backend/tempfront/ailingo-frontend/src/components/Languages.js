import React, { useEffect, useState } from 'react';
import axiosInstance from '../utils/axiosInstance';
import { Button } from 'react-bootstrap';
function Languages() {
  const [languages, setLanguages] = useState([]);

  useEffect(() => {
    fetchLanguages();
  }, []);

  const fetchLanguages = async () => {
    try {
      const response = await axiosInstance.get('languages/');
      setLanguages(response.data);
      
    } catch (error) {
      console.error(error);
    }
  };
  const handleAddLanguage = async (e) => {
    e.preventDefault();
    const languageName = prompt('Enter the name of the new language:');
    const languageCode = prompt('Enter the code for the new language:');
    if (languageName && languageCode) {
      try {
        const response = await axiosInstance.post('languages/', {
          name: languageName,
          code: languageCode,
        });
        setLanguages([...languages, response.data]);
      } catch (error) {
        console.error('Error adding new language:', error);
      }
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
      <Button variant="primary" onClick={handleAddLanguage}>
        Add Language
      </Button>
    </div>
  );}

export default Languages;