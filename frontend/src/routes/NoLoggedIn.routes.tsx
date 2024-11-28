import { Route, Routes } from "react-router-dom";
import { PageNotFound } from "../pages/PageNotFound.pages";
import { Homepage } from "../pages/Homepage.pages";
import { SignUp } from "../pages/Signup.pages";
import { SignIn } from "../pages/Signin.pages";

export function NoLoggedIn() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/signin" element={<SignIn />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </>
  );
}
