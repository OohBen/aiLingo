'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { getUserDetails } from '../lib/api';

export default function Navbar() {
  const router = useRouter();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUserDetails = async () => {
      const storedUser = localStorage.getItem('user');

      if (storedUser) {
        try {
          const parsedUser = JSON.parse(storedUser);
          const userDetails = await getUserDetails(parsedUser.email);
          setUser(userDetails);
        } catch (error) {
          console.error('Failed to fetch user details:', error);
          localStorage.removeItem('user');
          router.push('/login');
        }
      }
    };

    fetchUserDetails();
  }, []);

  useEffect(() => {
    const handleStorageChange = () => {
      const storedUser = localStorage.getItem('user');
      setUser(storedUser ? JSON.parse(storedUser) : null);
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);


  const handleLogout = () => {
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
    router.push('/login');
  };

  return (
    <nav className="bg-gray-800 py-4">
      <div className="container mx-auto px-4 flex justify-between items-center">
        <Link href="/" className="text-white font-bold text-xl">
          aiLingo
        </Link>
        <ul className="flex space-x-4">
          {user ? (
            <>
              <li>
                <Link href="/dashboard" className="text-gray-300 hover:text-white">
                  Dashboard
                </Link>
              </li>
              <li>
                <Link href="/profile" className="text-gray-300 hover:text-white">
                  Profile
                </Link>
              </li>
              <li>
                <Link href="/languages" className="text-gray-300 hover:text-white">
                  Languages
                </Link>
              </li>
              <li>
                <Link href="/lessons" className="text-gray-300 hover:text-white">
                  Lessons
                </Link>
              </li>
              <li>
                <Link href="/quizzes" className="text-gray-300 hover:text-white">
                  Quizzes
                </Link>
              </li>
              <li>
                <Link href="/quizzes/create" className="text-gray-300 hover:text-white">
                  Create Quiz
                </Link>
              </li>
              <li>
                <Link href="/chat" className="text-gray-300 hover:text-white">
                  Chat
                </Link>
              </li>
              <li>
                <Link href="/analytics" className="text-gray-300 hover:text-white">
                  Analytics
                </Link>
              </li>
              <li>
                <button
                  onClick={handleLogout}
                  className="text-gray-300 hover:text-white"
                >
                  Logout
                </button>
              </li>
            </>
          ) : (
            <>
              <li>
                <Link href="/login" className="text-gray-300 hover:text-white">
                  Login
                </Link>
              </li>
              <li>
                <Link href="/register" className="text-gray-300 hover:text-white">
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