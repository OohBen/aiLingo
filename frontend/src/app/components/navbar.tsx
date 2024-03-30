import Link from "next/link";

const Navbar = () => {
  return (
    <nav className="bg-blue-500 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        {/* The Link component wraps the text without an <a> tag */}
        <Link href="/" className="text-lg font-bold">
          aiLingo
        </Link>
        <div className="flex space-x-4">
          {/* Apply the class to the <a> tag directly */}
          <Link href="/features" className="hover:text-gray-200">
            Features
          </Link>
          <Link href="/contact" className="hover:text-gray-200">
            Contact
          </Link>
          <Link href="/login" className="hover:text-gray-200">
            Login
          </Link>
          <Link href="/signup" className="hover:text-gray-200">
            Sign Up
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
