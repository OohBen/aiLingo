import Link from 'next/link';

export default function Home() {
  return (
    <div>
      <h1>Welcome to aiLingo</h1>
      <p>Learn languages with AI-powered lessons and quizzes.</p>
      <Link href="/register">
        <button>Get Started</button>
      </Link>
    </div>
  );
}