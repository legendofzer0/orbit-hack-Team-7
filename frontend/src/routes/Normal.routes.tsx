import { Route, Routes } from "react-router-dom";
import { PageNotFound } from "../pages/PageNotFound.pages";
import { Homepage } from "../pages/Homepage.pages";
import { Profile } from "../pages/Profile.pages";
import ChatBotClient from "../pages/ChatBot.pages";
import SmartHomeClient from "../pages/SmartHome.pages";

export function Normal() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/Controls" element={<SmartHomeClient />} />
        <Route path="/chat" element={<ChatBotClient />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </>
  );
}
