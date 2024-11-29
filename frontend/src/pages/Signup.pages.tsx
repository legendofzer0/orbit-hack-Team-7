import { useState } from "react";
import { isEmail } from "../utils/isEmail";
import axios from "axios";
import { Link } from "react-router-dom";
import "../css/form.css";

export function SignUp() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [cPassword, setCPassword] = useState("");

  const validation = (data: {
    name: string;
    email: string;
    password: string;
    cPassword: string;
  }) => {
    if (!data.name && !data.email && !data.password && !data.cPassword) {
      console.log("All data fields need to field");
      return 0;
    }
    if (data.name.length < 5) {
      console.log("Name Needs to be at least 5");
      return 0;
    }
    if (!isEmail(data.email)) {
      console.log("Enter Valid Email");
      return 0;
    }
    if (data.password !== data.cPassword && data.password.length >= 5) {
      console.log(
        "Password and Conform Password needs to be same and password needs to be at least 5 character"
      );
      return 0;
    }
    console.log("all good");
    return 1;
  };

  const signUp = async (data: {
    name: string;
    email: string;
    password: string;
    cPassword: string;
  }) => {
    if (!validation(data)) {
      return;
    } else {
      try {
        await axios.post("/api/users", {
          name: data.name,
          email: data.email,
          password: data.password,
          role_id: "5f36f7cd-13d9-478f-a8bf-8ce05e2cac04",
        });
      } catch (err) {
        console.log(err);
      }
    }
  };

  return (
    <div className="card">
      Sign Up <br />
      <br />
      <div className="form">
        <div>
          <label htmlFor="Name">Name:</label> <br />
          <input
            className="form-input"
            type="text"
            value={name}
            onChange={(e) => {
              setName(e.target.value);
            }}
          />
        </div>
        <div>
          <label htmlFor="Email">Email:</label> <br />
          <input
            className="form-input"
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
            }}
          />
        </div>
        <div>
          <label htmlFor="Password">Password:</label> <br />
          <input
            className="form-input"
            type="password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
            }}
          />
        </div>
        <div>
          <label htmlFor="cPassword">Conform Password:</label> <br />
          <input
            className="form-input"
            type="password"
            value={cPassword}
            onChange={(e) => {
              setCPassword(e.target.value);
            }}
          />
        </div>
        <br />
        <button
          onClick={() =>
            signUp({
              name: name,
              email: email,
              password: password,
              cPassword: cPassword,
            })
          }
          className="success form-input"
        >
          Sign Up
        </button>
      </div>
      <span className="center">
        Already Have an Account <Link to="/ "> Sign In</Link>
      </span>
    </div>
  );
}
