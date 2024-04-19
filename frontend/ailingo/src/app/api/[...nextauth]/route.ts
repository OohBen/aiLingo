import { authOptions } from '../../../lib/auth';
import { NextApiHandler } from 'next';
import NextAuth from 'next-auth';

const handler: NextApiHandler = (req, res) => NextAuth(req, res, authOptions);

export { handler as GET, handler as POST };