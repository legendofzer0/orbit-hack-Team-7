import { useEffect, useState } from "react";
import { SignOut } from "../components/SignOut";
import { getId } from "../utils/getId";
import axios from "axios";
import { getTokenData } from "../utils/getTokenData";
import "../css/form.css";

export function Profile() {
  const id = getId();
  const token = localStorage.getItem("token");
  const [user, setUser] = useState(null); // Default state is null for a single user

  useEffect(() => {
    const fetchUser = async () => {
      const data = await getTokenData(token);
      setUser(data);
    };

    fetchUser();
  }, []);
  if (!user) {
    return <p>Loading...</p>; // Loading state while user data is being fetched
  }

  return (
    <div className="card">
      <h2>Welcome, {user.name}!</h2>
      <p>Email: {user.email}</p>
      <SignOut />
    </div>
  );
}
