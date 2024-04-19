import { getServerSession } from 'next-auth/next';
import { authOptions } from '../../lib/auth';
import { ChatInterface } from '../../components/ChatInterface';

export default async function Chat() {
  const session = await getServerSession(authOptions);

  if (!session) {
    return <div>Access Denied</div>;
  }

  return (
    <div>
      <h1>Chat</h1>
      <ChatInterface />
    </div>
  );
}