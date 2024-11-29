import { Route, Routes } from "react-router-dom";
import { PageNotFound } from "../pages/PageNotFound.pages";
import Dictation from "../components/Dictation";
import { Profile } from "../pages/Profile.pages";
import { Notification } from "../pages/Notification.pages";

export function Normal() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Dictation />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/Notification" element={<Notification />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </>
  );
}
