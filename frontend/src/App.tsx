import { useEffect } from "react";
import { NoLoggedIn } from "./routes/NoLoggedIn.routes";
import { getTokenData } from "./utils/getTokenData";
import { NoLoggedNav } from "./components/NoLoggedNav";

function App() {
  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      getTokenData(storedToken);
    }
  }, []);
  return (
    <>
      <NoLoggedNav />
      <NoLoggedIn />
    </>
  );
}

export default App;
