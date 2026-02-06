import {api} from "../api/api";

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export async function login(
  email: string,
  password: string
): Promise<string> {
  const response = await api.post<LoginResponse>("/auth/login", {
    email,
    password,
  });

  const { access_token } = response.data;

  localStorage.setItem("access_token", access_token);

  return access_token;
}

export function logout(): void {
  localStorage.removeItem("access_token");
}
