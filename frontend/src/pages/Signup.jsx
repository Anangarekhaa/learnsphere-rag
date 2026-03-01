import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");  
  const navigate = useNavigate();

  const handleSignup = async () => {
    setError("");

    try {
      await api.post("/signup", { email, password });
      navigate("/");
    } catch (err) {
      if (err.response && err.response.data.detail) {
        setError(err.response.data.detail); 
      } else {
        setError("Something went wrong. Please try again.");
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white w-96 p-8 rounded-2xl shadow-lg">
        <h2 className="text-2xl font-semibold mb-6 text-center">
          Create Account
        </h2>

        <input
          className="w-full border p-3 rounded-lg mb-4"
          placeholder="Email"
          onChange={(e) => {
            setEmail(e.target.value);
            setError(""); 
          }}
        />

        <input
          type="password"
          className="w-full border p-3 rounded-lg mb-4"
          placeholder="Password"
          onChange={(e) => {
            setPassword(e.target.value);
            setError("");
          }}
        />

     
        {error && (
          <p className="text-red-600 text-sm mb-4 text-center">
            {error}
          </p>
        )}

        <button
          onClick={handleSignup}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg transition"
        >
          Sign Up
        </button>

        <p className="text-sm text-center mt-4">
          Already have an account?{" "}
          <Link to="/" className="text-blue-600">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}