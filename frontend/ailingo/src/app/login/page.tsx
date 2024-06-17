"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    try {
      const response = await axios.post(`${API_BASE_URL}/users/login/`, {
        email,
        password,
      });

      const { refresh, access, user } = response.data;

      if (access) {
        localStorage.setItem("refresh_token", refresh);
        localStorage.setItem("access_token", access);
        localStorage.setItem("user", JSON.stringify(user));
        router.push("/dashboard");
        // Pause for .5 seconds to allow the router to finish the push
        await new Promise((resolve) => setTimeout(resolve, 100));
        window.location.reload();
      } else {
        setError("Invalid email or password");
      }
    } catch (error) {
      if (error.response && error.response.status === 401) {
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        setError("Session expired. Please login again.");
      } else {
        setError("An error occurred during login");
      }
    }
  };

  return (
    <div className="max-w-md mx-auto mt-8">
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="email" className="block mb-1">
            Email
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded text-black"
          />
        </div>
        <div>
          <label htmlFor="password" className="block mb-1">
            Password
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded text-black"
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-500 text-white px-4 py-2 rounded"
        >
          Login
        </button>
      </form>
    </div>
  );
}
