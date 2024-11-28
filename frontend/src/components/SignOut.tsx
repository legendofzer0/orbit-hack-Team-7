import { useNavigate } from "react-router-dom";

export function SignOut() {
  const navigate = useNavigate();

  const handleSignOut = () => {
    localStorage.removeItem("token");
    navigate("/"); // Redirects to the home page
    window.location.reload(); // Reloads the application
  };

  return <button onClick={handleSignOut}>Sign Out</button>;
}
