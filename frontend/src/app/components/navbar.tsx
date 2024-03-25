import Link from 'next/link';

const Navbar = () => {
    return (
      <nav className="bg-blue-500 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        {/* The Link component wraps the text without an <a> tag */}
        <Link href="/">
          <a className="text-lg font-bold">aiLingo</a>
        </Link>
        <div className="flex space-x-4">
          {/* Apply the class to the <a> tag directly */}
          <Link href="/about">
            <a className="hover:text-gray-200">About</a>
          </Link>
          <Link href="/features">
            <a className="hover:text-gray-200">Features</a>
          </Link>
          <Link href="/contact">
            <a className="hover:text-gray-200">Contact</a>
          </Link>
        </div>
      </div>
    </nav>
    );
  };
  
  export default Navbar;