'use client';
import Link from 'next/link';
import { useSession, signOut } from 'next-auth/react';

export function Navigation() {
  const { data: session } = useSession();

  const handleSignOut = async () => {
    await signOut();
  };

  return (
    <nav className="bg-gray-800 py-4">
      <div className="container mx-auto px-4">
        <ul className="flex space-x-4">
          <li>
            <Link href="/" className="text-white hover:text-gray-300">
              Home
            </Link>
          </li>
          {session ? (
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
                  onClick={handleSignOut}
                  className="text-white hover:text-gray-300"
                >
                  Sign Out
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