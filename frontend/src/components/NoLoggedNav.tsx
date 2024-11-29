import { Link } from "react-router-dom";

export function NoLoggedNav() {
  return (
    <>
      <Link to="/" className="nav-item">
        Sign In
      </Link>
      <Link to="/signup" className="nav-item">
        Sign Up
      </Link>
    </>
  );
}
