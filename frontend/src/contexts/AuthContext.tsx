import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface AuthUser {
  user_id: number;
  email: string;
  role: string;
  first_name: string;
  last_name: string;
}

interface AuthContextValue {
  user: AuthUser | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, firstName: string, lastName: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

// Helper to set/clear the axios header immediately
function setAxiosAuth(t: string | null) {
  if (t) {
    axios.defaults.headers.common["Authorization"] = `Bearer ${t}`;
  } else {
    delete axios.defaults.headers.common["Authorization"];
  }
}

// Set header immediately on module load if token exists in localStorage
const initialToken = localStorage.getItem("nexacrm_token");
setAxiosAuth(initialToken);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [token, setToken] = useState<string | null>(initialToken);
  const [loading, setLoading] = useState(true);

  // Verify token on mount only (not on every token change)
  useEffect(() => {
    const verifyToken = async () => {
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        const res = await axios.get(`${API_URL}/auth/me`);
        setUser({
          user_id: res.data.id,
          email: res.data.email,
          role: res.data.role,
          first_name: res.data.first_name,
          last_name: res.data.last_name,
        });
      } catch {
        localStorage.removeItem("nexacrm_token");
        setAxiosAuth(null);
        setToken(null);
        setUser(null);
      }
      setLoading(false);
    };
    verifyToken();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const res = await axios.post(`${API_URL}/auth/login`, { email, password });
    const data = res.data;
    localStorage.setItem("nexacrm_token", data.access_token);
    setAxiosAuth(data.access_token);
    setToken(data.access_token);
    setUser({
      user_id: data.user_id,
      email: data.email,
      role: data.role,
      first_name: data.first_name,
      last_name: data.last_name,
    });
    setLoading(false);
  }, []);

  const signup = useCallback(async (email: string, password: string, firstName: string, lastName: string) => {
    const res = await axios.post(`${API_URL}/auth/signup`, {
      email,
      password,
      first_name: firstName,
      last_name: lastName,
    });
    const data = res.data;
    localStorage.setItem("nexacrm_token", data.access_token);
    setAxiosAuth(data.access_token);
    setToken(data.access_token);
    setUser({
      user_id: data.user_id,
      email: data.email,
      role: data.role,
      first_name: data.first_name,
      last_name: data.last_name,
    });
    setLoading(false);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("nexacrm_token");
    setAxiosAuth(null);
    setToken(null);
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, token, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
