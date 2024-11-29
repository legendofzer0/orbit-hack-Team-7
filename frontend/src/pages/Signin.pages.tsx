import { useState } from "react";
import { isEmail } from "../utils/isEmail";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import "../css/form.css";

export function SignIn() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const validation = (data: { email: string; password: string }) => {
    console.log(data);
    if (!data.email && !data.password) {
      console.log("All data fields need to field");
      return 0;
    }
    if (!isEmail(data.email)) {
      console.log("Enter Valid Email");
      return 0;
    }

    console.log("all good");
    return 1;
  };

  const signIn = async (data: { email: string; password: string }) => {
    if (!validation(data)) {
      return;
    } else {
      try {
        const response = await axios.post("/api/auth/login", {
          email: data.email,
          plainPassword: data.password,
        });
        localStorage.setItem("token", response.data);
        navigate("/");
        window.location.reload();
      } catch (err) {
        console.log(err);
      }
    }
  };

  return (
    <div className="card">
      Sign Up
      <div className="form">
        <div>
          <label htmlFor="Email">Email:</label> <br />
          <input
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
            }}
            className="form-input"
          />
        </div>
        <div>
          <label htmlFor="Password">Password:</label> <br />
          <input
            type="password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
            }}
            className="form-input"
          />
        </div>
        <br />

        <button
          onClick={() =>
            signIn({
              email: email,
              password: password,
            })
          }
          className="success form-input"
        >
          Sign In
        </button>
      </div>
      <span className="center">
        I don't Have Account <Link to="/signup">Sign up </Link>
      </span>
    </div>
  );
}
