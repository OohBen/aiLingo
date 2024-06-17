// frontend/ailingo/src/app/profile/page.tsx
"use client";

import Image from "next/image";
import { useAuth } from "../../lib/useAuth";
import { useEffect, useState } from "react";
import { getUserDetails } from "../../lib/api";

export default function Profile() {
  const user = useAuth();
  const [homeLanguage, setHomeLanguage] = useState(null);

  useEffect(() => {
    const fetchUserDetails = async () => {
      try {
        const data = await getUserDetails(user.email);
        setHomeLanguage(data.home_language);
      } catch (error) {
        console.error("Failed to fetch user details", error);
      }
    };

    if (user) {
      fetchUserDetails();
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

        <div className="mt-8 text-center">
          <div className="mb-2">
            <span className="font-semibold">Name:</span>{" "}
            <span className="text-lg">{user.name}</span>
          </div>
          <div>
            <span className="font-semibold">Email:</span>{" "}
            <span className="text-lg">{user.email}</span>
          </div>
          {homeLanguage && (
            <div className="mb-2">
              <span className="font-semibold">Home Language:</span>{" "}
              <span className="text-lg">{homeLanguage.name}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}