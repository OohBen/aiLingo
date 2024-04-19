import { getServerSession } from 'next-auth/next';
import { authOptions } from '../../lib/auth';
import { getUserAnalytics } from '../../lib/api';
import { AnalyticsChart } from '../../components/AnalyticsChart';

export default async function Analytics() {
  const session = await getServerSession(authOptions);

  if (!session) {
    return <div>Access Denied</div>;
  }

  const analytics = await getUserAnalytics(session.user.email);

  return (
    <div>
      <h1>Analytics</h1>
      <AnalyticsChart data={analytics} />
    </div>
  );
}