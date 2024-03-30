import Link from "next/link";
import Navbar from "../components/navbar";

const Signup = () => {
  return (
    <div>
      <Navbar />
      <div className="flex-grow flex items-center justify-center">
        <div className="mt-8 bg-[#212121] p-8 rounded shadow-md w-96">
          <h1 className="text-2xl text-center mt-4 mb-6">Sign Up:</h1>{" "}
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
              Sign Up!
            </button>
          </form>
          <Link
            className="block text-center text-blue-500 hover:underline mt-2"
            href="/login"
          >
            {" "}
            Have an account? Login
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Signup;
