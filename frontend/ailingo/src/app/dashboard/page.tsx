import { getServerSession } from 'next-auth/next';
import { authOptions } from '../../lib/auth';
import { getUserDetails } from '../../lib/api';

export default async function Dashboard() {
  const session = await getServerSession(authOptions);

  if (!session) {
    return <div>Access Denied</div>;
  }

  const user = await getUserDetails(session.user.email);

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {user.name}!</p>
      {/* Add more dashboard content */}
    </div>
  );
}