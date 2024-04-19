'use client';

import { useAuth } from '../../lib/useAuth';
import { useEffect, useState } from 'react';
import { getLanguages } from '../../lib/api';
import { LanguageList } from '../../components/LanguageList';

export default function Languages() {
  const user = useAuth();
  const [languages, setLanguages] = useState([]);

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const data = await getLanguages();
        setLanguages(data);
      } catch (error) {
        console.error('Failed to fetch languages', error);
      }
    };

    if (user) {
      fetchLanguages();
    }
  }, [user]);

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Languages</h1>
      <LanguageList languages={languages} />
    </div>
  );
}