"use client";

import { useAuth } from "../../lib/useAuth";
import { useEffect, useState } from "react";
import { getLanguages } from "../../lib/api";
import { LanguageList } from "../../components/LanguageList";

export default function Languages() {
  const user = useAuth();
  const [languages, setLanguages] = useState([]);

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const data = await getLanguages();
        setLanguages(data);
      } catch (error) {
        console.error("Failed to fetch languages", error);
      }
    };

    if (user) {
      fetchLanguages();
    }
  }, [user]);

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-2xl font-bold">Loading...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Languages</h1>
      <div className="bg-white rounded-lg shadow-lg p-8">
        <LanguageList languages={languages} />
      </div>
    </div>
  );
}