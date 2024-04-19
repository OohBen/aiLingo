'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Navbar() {
  const router = useRouter();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');

    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
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
                <Link href="/dashboard" className="text-white hover:text-gray-300">
                  Dashboard
                </Link>
              </li>
              <li>
                <Link href="/profile" className="text-white hover:text-gray-300">
                  Profile
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
                <Link href="/login" className="text-white hover:text-gray-300">
                  Login
                </Link>
              </li>
              <li>
                <Link href="/register" className="text-white hover:text-gray-300">
                  Register
                </Link>
              </li>
            </>
          )}
          <li>
            <Link href="/languages" className="text-white hover:text-gray-300">
              Languages
            </Link>
          </li>
          <li>
            <Link href="/lessons" className="text-white hover:text-gray-300">
              Lessons
            </Link>
          </li>
          <li>
            <Link href="/quizzes" className="text-white hover:text-gray-300">
              Quizzes
            </Link>
          </li>
          <li>
            <Link href="/chat" className="text-white hover:text-gray-300">
              Chat
            </Link>
          </li>
          <li>
            <Link href="/analytics" className="text-white hover:text-gray-300">
              Analytics
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}