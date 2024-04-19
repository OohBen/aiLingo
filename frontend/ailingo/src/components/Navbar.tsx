'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function Navbar() {
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    router.push('/login');
  };

  return (
    <nav className="bg-gray-800 py-4">
      <div className="container mx-auto px-4 flex justify-between items-center">
        <Link href="/" className="text-white font-bold text-xl">
          aiLingo
        </Link>
        <ul className="flex space-x-4">
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
            <button
              onClick={handleLogout}
              className="text-gray-300 hover:text-white"
            >
              Logout
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
}