import axios from "axios";

export const api = axios.create({
  baseURL: "https://projeto-automacao-email-sampaio-backend.onrender.com/", // backend FastAPI
});

