import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

interface LayoutProps {
  children: React.ReactNode;
}

const navItems = [
  { path: "/dashboard", label: "Dashboard" },
  { path: "/contact", label: "Contacts" },
  { path: "/company", label: "Companies" },
  { path: "/opportunity", label: "Pipeline" },
  { path: "/task", label: "Tasks" },
  { path: "/emailtemplate", label: "Email Templates" },
];

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial, sans-serif" }}>
      <nav style={{ width: "250px", background: "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", color: "white", padding: "20px", overflowY: "auto", display: "flex", flexDirection: "column" }}>
        <h2 style={{ marginTop: "0", fontSize: "24px", marginBottom: "30px", fontWeight: "bold" }}>NexaCRM</h2>
        <div style={{ display: "flex", flexDirection: "column", flex: "1" }}>
          {navItems.map((item) => {
            const isActive = location.pathname === item.path || (item.path === "/contact" && location.pathname.startsWith("/contact/"));
            return (
              <a
                key={item.path}
                onClick={(e) => { e.preventDefault(); navigate(item.path); }}
                href={item.path}
                style={{
                  color: "white",
                  textDecoration: "none",
                  padding: "10px 15px",
                  display: "block",
                  background: isActive ? "rgba(255,255,255,0.2)" : "transparent",
                  borderRadius: "4px",
                  marginBottom: "5px",
                  cursor: "pointer",
                }}
              >
                {item.label}
              </a>
            );
          })}
        </div>
        {user && (
          <div style={{ borderTop: "1px solid rgba(255,255,255,0.2)", paddingTop: "15px", marginTop: "auto" }}>
            <div style={{ fontSize: "13px", marginBottom: "8px", opacity: 0.9 }}>
              {user.first_name} {user.last_name}
            </div>
            <div style={{ fontSize: "11px", marginBottom: "12px", opacity: 0.7 }}>{user.email}</div>
            <button
              onClick={handleLogout}
              style={{
                width: "100%",
                padding: "8px",
                background: "rgba(255,255,255,0.15)",
                color: "white",
                border: "1px solid rgba(255,255,255,0.3)",
                borderRadius: "4px",
                cursor: "pointer",
                fontSize: "13px",
              }}
            >
              Logout
            </button>
          </div>
        )}
        <p style={{ paddingTop: "15px", fontSize: "11px", opacity: "0.8", textAlign: "center" }}>
          &copy; 2026 NexaCRM. All rights reserved.
        </p>
      </nav>
      <main style={{ flex: "1", padding: "40px", overflowY: "auto", background: "#f5f5f5" }}>
        {children}
      </main>
    </div>
  );
};

export default Layout;
