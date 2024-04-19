import { getServerSession } from 'next-auth/next';
import { authOptions } from '../../lib/auth';
import { getUserDetails } from '../../lib/api';

export default async function Profile() {
  const session = await getServerSession(authOptions);

  if (!session) {
    return <div>Access Denied</div>;
  }

  const user = await getUserDetails(session.user.email);

  return (
    <div>
      <h1>Profile</h1>
      <p>Name: {user.name}</p>
      <p>Email: {user.email}</p>
      {/* Add more profile information */}
    </div>
  );
}