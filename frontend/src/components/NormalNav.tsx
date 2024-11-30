import { Link } from "react-router-dom";

export function NormalNav() {
  return (
    <>
      <Link to="/" className="nav-item">
        AI
      </Link>
      <Link to="/profile" className="nav-item">
        Profile
      </Link>
    </>
  );
}
