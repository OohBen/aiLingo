import Link from "next/link";
import Navbar from "../components/navbar";

const Login = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-grow bg-black flex items-center justify-center">
        <div className="mt-8 text-white bg-[#000000] p-8 rounded shadow-md w-96 border-2 border-blue-900">
          <h1 className="text-2xl text-center mt-4 mb-6">Log In</h1>{" "}
          {/* Added margin bottom to the heading */}
          <form>
            <input /* email */
              type="text"
              className="w-full border border-gray-300 text-black rounded px-3 py-2 mb-4 focus:outline-none focus:border-blue-400 focus:text-black"
              placeholder="Email"
              required
            />
            <input /* password */
              type="password"
              className="w-full border border-gray-300 text-black rounded px-3 py-2 mb-4 focus:outline-none focus:border-blue-400 focus:text-black"
              placeholder="Password"
              required
            />
            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
            >
              Login
            </button>
          </form>
          <Link
            className="block text-center text-blue-500 hover:underline mt-2"
            href="/signup"
          >
            {" "}
            Don't have an account? Sign Up
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
