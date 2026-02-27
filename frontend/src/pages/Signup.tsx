import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const Signup: React.FC = () => {
  const { signup } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await signup(email, password, firstName, lastName);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Signup failed");
    }
    setLoading(false);
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", background: "linear-gradient(135deg, #4b3c82 0%, #5a3d91 50%, #6b4fa0 100%)", fontFamily: "Arial, sans-serif" }}>
      <div style={{ background: "white", borderRadius: "12px", padding: "40px", width: "400px", boxShadow: "0 20px 60px rgba(0,0,0,0.3)" }}>
        <h1 style={{ textAlign: "center", color: "#4b3c82", marginTop: 0, fontSize: "28px" }}>NexaCRM</h1>
        <p style={{ textAlign: "center", color: "#666", marginBottom: "30px" }}>Create your account</p>
        {error && <div style={{ background: "#fee", color: "#c00", padding: "10px", borderRadius: "6px", marginBottom: "15px", fontSize: "14px" }}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
            <div style={{ flex: 1 }}>
              <label style={{ display: "block", marginBottom: "5px", color: "#333", fontSize: "14px", fontWeight: "bold" }}>First Name</label>
              <input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} required style={{ width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "6px", fontSize: "14px", boxSizing: "border-box" }} />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ display: "block", marginBottom: "5px", color: "#333", fontSize: "14px", fontWeight: "bold" }}>Last Name</label>
              <input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} required style={{ width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "6px", fontSize: "14px", boxSizing: "border-box" }} />
            </div>
          </div>
          <div style={{ marginBottom: "15px" }}>
            <label style={{ display: "block", marginBottom: "5px", color: "#333", fontSize: "14px", fontWeight: "bold" }}>Email</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required style={{ width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "6px", fontSize: "14px", boxSizing: "border-box" }} />
          </div>
          <div style={{ marginBottom: "20px" }}>
            <label style={{ display: "block", marginBottom: "5px", color: "#333", fontSize: "14px", fontWeight: "bold" }}>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={6} style={{ width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "6px", fontSize: "14px", boxSizing: "border-box" }} />
          </div>
          <button type="submit" disabled={loading} style={{ width: "100%", padding: "12px", background: "linear-gradient(135deg, #4b3c82, #5a3d91)", color: "white", border: "none", borderRadius: "6px", fontSize: "16px", cursor: loading ? "not-allowed" : "pointer", opacity: loading ? 0.7 : 1 }}>
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>
        <p style={{ textAlign: "center", marginTop: "20px", color: "#666", fontSize: "14px" }}>
          Already have an account? <Link to="/login" style={{ color: "#5a3d91", textDecoration: "none", fontWeight: "bold" }}>Sign in</Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;
