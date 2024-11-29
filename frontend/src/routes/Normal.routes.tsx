import { Route, Routes } from "react-router-dom";
import { PageNotFound } from "../pages/PageNotFound.pages";
import Dictation from "../components/Dictation";
import { Profile } from "../pages/Profile.pages";

export function Normal() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Dictation />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </>
  );
}
