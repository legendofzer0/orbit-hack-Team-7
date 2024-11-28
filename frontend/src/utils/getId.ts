import axios from "axios";

export async function getId() {
  const token = localStorage.getItem("token");
  const data = await axios.post("/api/auth/getData", { token });
  return data.data.id;
}
