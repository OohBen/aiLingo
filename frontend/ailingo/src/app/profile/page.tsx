'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export default function Profile() {
  const [user, setUser] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const fetchUserDetails = async () => {
      const access_token = localStorage.getItem('access_token');

      if (!access_token) {
        router.push('/login');
        return;
      }

      try {
        const response = await axios.get(`${API_BASE_URL}/users/profile/`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        setUser(response.data);
      } catch (error) {
        console.error('Failed to fetch user details', error);
        router.push('/login');
      }
    };

    fetchUserDetails();
  }, []);

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Profile</h1>
      <p>Name: {user.name}</p>
      <p>Email: {user.email}</p>
    </div>
  );
}