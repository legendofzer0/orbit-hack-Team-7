import { Route, Routes } from "react-router-dom";
import { PageNotFound } from "../pages/PageNotFound.pages";
import { Dictation } from "../components/Dictation";

export function Normal() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Dictation />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </>
  );
}
