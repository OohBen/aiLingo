"use client";
import Image from "next/image";

import { useAuth } from "../../lib/useAuth";

export default function Profile() {
  const user = useAuth();

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto px-4 mt-8 max-w-md">
      <div className="bg-blue-500 text-white rounded-lg shadow-lg p-8 flex flex-col items-center">
        <h1 className="text-3xl font-bold mb-4">Profile</h1>
        <div className="rounded-full overflow-hidden border-2 border-white">
          {" "}
          {/* Added rounded-full and border classes */}
          <Image
            src="/contactImg.png" // Replace image here
            alt="Image Description"
            width={200}
            height={200}
          />
        </div>
        <div>
          <p className="text-center mt-8">Name: {user.name}</p>
          <p className="text-center">Email: {user.email}</p>
        </div>
      </div>
    </div>
  );
}
