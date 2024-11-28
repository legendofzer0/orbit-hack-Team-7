import axios from "axios";

export async function getTokenData(token: string) {
  const data = await axios.post("/api/auth/getData", { token });
  return data.data;
}
