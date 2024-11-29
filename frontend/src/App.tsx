import { useEffect, useState } from "react";
import { NoLoggedIn } from "./routes/NoLoggedIn.routes";
import { getTokenData } from "./utils/getTokenData"; // Assuming it returns a Promise
import { NoLoggedNav } from "./components/NoLoggedNav";
import { NormalNav } from "./components/NormalNav";
import { Normal } from "./routes/Normal.routes";
import "./css/root.css";
function App() {
  const [role, setRole] = useState(null); // Initialize role as null

  useEffect(() => {
    const fetchRole = async () => {
      const storedToken = localStorage.getItem("token");
      if (storedToken) {
        try {
          const tokenData = await getTokenData(storedToken); // Wait for the promise to resolve
          // console.log("Decoded token data:", tokenData.role_relation.name); // Debug token data
          setRole(tokenData.role_relation.name); // Update role state
        } catch (error) {
          console.error("Error decoding token:", error);
          setRole(null); // Reset role in case of error
        }
      } else {
        console.warn("No token found in localStorage."); // Debug missing token
      }
    };

    fetchRole();
  }, []);

  if (role === "normal") {
    return (
      <>
        <div className="nav">
          <NormalNav />
        </div>
        <Normal />
      </>
    );
  }

  if (role === "Admin") {
    return <>Admin</>;
  }

  // Default case for unauthenticated users
  return (
    <>
      <div>
        <NoLoggedNav />
      </div>
      <NoLoggedIn />
    </>
  );
}

export default App;
