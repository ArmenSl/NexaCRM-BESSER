import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const Login: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed");
    }
    setLoading(false);
  };

  const inputStyle: React.CSSProperties = {
    width: "100%", padding: "12px 14px", border: "1.5px solid #e5e7eb", borderRadius: "10px",
    fontSize: "14px", fontFamily: "inherit", outline: "none", transition: "border-color 150ms, box-shadow 150ms", boxSizing: "border-box",
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif" }}>
      {/* Left — branding */}
      <div style={{
        flex: 1, background: "linear-gradient(135deg, #16132b 0%, #2d2555 50%, #6c5ce7 100%)",
        display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center",
        padding: "60px", position: "relative", overflow: "hidden",
      }}>
        <div style={{ position: "absolute", top: "-100px", right: "-100px", width: "400px", height: "400px", borderRadius: "50%", background: "rgba(108,92,231,0.15)" }} />
        <div style={{ position: "absolute", bottom: "-80px", left: "-80px", width: "300px", height: "300px", borderRadius: "50%", background: "rgba(162,155,254,0.1)" }} />
        <div style={{ position: "relative", zIndex: 1, textAlign: "center" }}>
          <div style={{ width: "64px", height: "64px", borderRadius: "18px", background: "linear-gradient(135deg, #6c5ce7, #a29bfe)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "28px", fontWeight: "800", color: "white", margin: "0 auto 20px" }}>N</div>
          <h1 style={{ color: "white", fontSize: "36px", fontWeight: "800", letterSpacing: "-1px", marginBottom: "12px" }}>NexaCRM</h1>
          <p style={{ color: "rgba(255,255,255,0.6)", fontSize: "16px", maxWidth: "320px", lineHeight: "1.6" }}>
            Your AI-powered sales command center. Manage contacts, enrich leads, and close deals faster.
          </p>
        </div>
      </div>

      {/* Right — form */}
      <div style={{ flex: 1, display: "flex", justifyContent: "center", alignItems: "center", padding: "60px", background: "#fff" }}>
        <div style={{ width: "100%", maxWidth: "400px" }}>
          <h2 style={{ fontSize: "26px", fontWeight: "700", color: "#1a1a2e", marginBottom: "8px", letterSpacing: "-0.5px" }}>Welcome back</h2>
          <p style={{ color: "#6b7280", marginBottom: "32px", fontSize: "15px" }}>Sign in to your account to continue</p>

          {error && (
            <div style={{ background: "#fef2f2", color: "#dc2626", padding: "12px 16px", borderRadius: "10px", marginBottom: "20px", fontSize: "13px", fontWeight: "500", border: "1px solid #fecaca" }}>{error}</div>
          )}

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: "20px" }}>
              <label style={{ display: "block", marginBottom: "6px", color: "#374151", fontSize: "13px", fontWeight: "600" }}>Email address</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required placeholder="you@company.com" style={inputStyle}
                onFocus={(e) => { e.target.style.borderColor = "#6c5ce7"; e.target.style.boxShadow = "0 0 0 3px rgba(108,92,231,0.1)"; }}
                onBlur={(e) => { e.target.style.borderColor = "#e5e7eb"; e.target.style.boxShadow = "none"; }}
              />
            </div>
            <div style={{ marginBottom: "28px" }}>
              <label style={{ display: "block", marginBottom: "6px", color: "#374151", fontSize: "13px", fontWeight: "600" }}>Password</label>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required placeholder="Enter your password" style={inputStyle}
                onFocus={(e) => { e.target.style.borderColor = "#6c5ce7"; e.target.style.boxShadow = "0 0 0 3px rgba(108,92,231,0.1)"; }}
                onBlur={(e) => { e.target.style.borderColor = "#e5e7eb"; e.target.style.boxShadow = "none"; }}
              />
            </div>
            <button type="submit" disabled={loading} style={{
              width: "100%", padding: "13px", background: loading ? "#a29bfe" : "linear-gradient(135deg, #6c5ce7, #5a4bd1)",
              color: "white", border: "none", borderRadius: "10px", fontSize: "15px", fontWeight: "600", fontFamily: "inherit",
              cursor: loading ? "not-allowed" : "pointer", transition: "all 150ms ease",
              boxShadow: loading ? "none" : "0 4px 14px rgba(108,92,231,0.35)",
            }}
              onMouseEnter={(e) => { if (!loading) e.currentTarget.style.transform = "translateY(-1px)"; }}
              onMouseLeave={(e) => { e.currentTarget.style.transform = "translateY(0)"; }}
            >
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>

          <p style={{ textAlign: "center", marginTop: "28px", color: "#6b7280", fontSize: "14px" }}>
            Don't have an account?{" "}
            <Link to="/signup" style={{ color: "#6c5ce7", textDecoration: "none", fontWeight: "600" }}>Create one</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
