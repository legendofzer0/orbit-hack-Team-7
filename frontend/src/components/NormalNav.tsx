import { Link } from "react-router-dom";

export function NormalNav() {
  return (
    <>
      <Link to="/">Home</Link>
      <Link to="/Controls">Smart Home</Link>
      <Link to="/Chat">Chat with AI</Link>
      <Link to="/Notification">notification</Link>
      <Link to="/profile">Profile</Link>
    </>
  );
}
