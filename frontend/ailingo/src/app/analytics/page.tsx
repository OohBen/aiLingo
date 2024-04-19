'use client';

import { useAuth } from '../../lib/useAuth';
import { useEffect, useState } from 'react';
import { getUserAnalytics } from '../../lib/api';
import { AnalyticsChart } from '../../components/AnalyticsChart';

export default function Analytics() {
  const user = useAuth();
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const data = await getUserAnalytics(user.email);
        setAnalytics(data);
      } catch (error) {
        console.error('Failed to fetch analytics', error);
      }
    };

    if (user) {
      fetchAnalytics();
    }
  }, [user]);

  if (!user || !analytics) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Analytics</h1>
      <AnalyticsChart data={analytics} />
    </div>
  );
}