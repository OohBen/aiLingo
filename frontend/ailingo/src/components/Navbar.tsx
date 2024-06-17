// frontend/ailingo/src/components/Navbar.tsx
"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getUserDetails } from "../lib/api";

export default function Navbar() {
  const router = useRouter();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUserDetails = async () => {
      const accessToken = localStorage.getItem("access_token");
      if (accessToken) {
        try {
          const userDetails = await getUserDetails();
          setUser(userDetails);
        } catch (error) {
          console.error("Failed to fetch user details:", error);
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          router.push("/login");
        }
      }
    };

    fetchUserDetails();
  }, []);

  useEffect(() => {
    const handleStorageChange = () => {
      const accessToken = localStorage.getItem("access_token");
      if (accessToken) {
        getUserDetails();
      } else {
        setUser(null);
      }
    };

    window.addEventListener("storage", handleStorageChange);

    return () => {
      window.removeEventListener("storage", handleStorageChange);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("access_token");
    setUser(null);
    router.push("/login");
  };

  return (
    <nav className="bg-blue-900 text-white p-6">
      <div className="container mx-auto px-4 flex justify-between items-center">
        <Link href="/" className="text-white font-bold text-xl">
          aiLingo
        </Link>
        <ul className="flex space-x-4">
          {user ? (
            <>
              <li>
                <Link href="/dashboard" className="text-blue-200 hover:text-white">
                  Dashboard
                </Link>
              </li>
              <li>
                <Link href="/profile" className="text-blue-200 hover:text-white">
                  Profile
                </Link>
              </li>
              <li>
                <Link href="/languages" className="text-blue-200 hover:text-white">
                  Languages
                </Link>
              </li>
              <li>
                <Link href="/lessons" className="text-blue-200 hover:text-white">
                  Lessons
                </Link>
              </li>
              <li>
                <Link href="/quizzes" className="text-blue-200 hover:text-white">
                  Quizzes
                </Link>
              </li>
              <li>
                <Link href="/quizzes/create" className="text-blue-200 hover:text-white">
                  Create Quiz
                </Link>
              </li>
              <li>
                <Link href="/chat" className="text-blue-200 hover:text-white">
                  Chat
                </Link>
              </li>
              <li>
                <Link href="/analytics" className="text-blue-200 hover:text-white">
                  Analytics
                </Link>
              </li>
              <li>
                <button onClick={handleLogout} className="text-blue-200 hover:text-white">
                  Logout
                </button>
              </li>
            </>
          ) : (
            <>
              <li>
                <Link href="/login" className="text-blue-200 hover:text-white">
                  Login
                </Link>
              </li>
              <li>
                <Link href="/register" className="text-blue-200 hover:text-white">
                  Register
                </Link>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
}