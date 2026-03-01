import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="bg-white shadow-md px-8 py-4 flex justify-between items-center">
      <h1
        className="text-xl font-semibold text-blue-600 cursor-pointer"
        onClick={() => navigate("/dashboard")}
      >
        LearnSphere RAG
      </h1>

      <button
        onClick={logout}
        className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm"
      >
        Logout
      </button>
    </div>
  );
}