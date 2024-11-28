import { Link } from "react-router-dom";

export function NoLoggedNav() {
  return (
    <>
      <Link to="/signin">Sign In</Link>
      <Link to="/signup">Sign Up</Link>
    </>
  );
}
