"use client";

import Image from "next/image";
import { useAuth } from "../../lib/useAuth";
import { useEffect, useState } from "react";
import { getLanguages } from "../../lib/api";

export default function Profile() {
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
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto px-4 mt-8 max-w-md">
      <div className="bg-blue-500 text-white rounded-lg shadow-lg p-8 flex flex-col items-center">
        <h1 className="text-3xl font-bold mb-4">Profile</h1>

        <div className="rounded-full overflow-hidden border-2 border-white">
          <Image
            src="/cartoon-dog.png"
            alt="Profile Image"
            width={200}
            height={200}
          />
        </div>

        <div className="mt-8 text-center ">
          <h2 className="text-2xl font-bold mb-4">Languages</h2>
          <div className="flex flex-wrap justify-center gap-4 ">
            {languages.map((language) => (
              <div
                key={language.id}
                className="bg-blue-600 rounded-lg px-4 py-2 text-center"
              >
                <span className="text-lg font-semibold">{language.name}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-8 text-center">
          <div className="mb-2">
            <span className="font-semibold">Name:</span>{" "}
            <span className="text-lg">{user.name}</span>
          </div>
          <div>
            <span className="font-semibold">Email:</span>{" "}
            <span className="text-lg">{user.email}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
