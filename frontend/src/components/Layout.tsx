import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

interface LayoutProps {
  children: React.ReactNode;
}

const navItems = [
  { path: "/dashboard", label: "Dashboard", icon: "\u25A6" },
  { path: "/contact", label: "Contacts", icon: "\u263A" },
  { path: "/company", label: "Companies", icon: "\u2302" },
  { path: "/opportunity", label: "Pipeline", icon: "\u2B21" },
  { path: "/task", label: "Tasks", icon: "\u2611" },
  { path: "/emailtemplate", label: "Templates", icon: "\u2709" },
];

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif" }}>
      {/* Sidebar */}
      <nav
        style={{
          width: sidebarCollapsed ? "72px" : "260px",
          background: "linear-gradient(180deg, #16132b 0%, #1e1b3a 40%, #2d2555 100%)",
          color: "white",
          padding: sidebarCollapsed ? "20px 10px" : "24px 16px",
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          transition: "width 250ms cubic-bezier(0.4, 0, 0.2, 1)",
          position: "relative",
          zIndex: 10,
        }}
      >
        {/* Logo */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            marginBottom: "32px",
            paddingLeft: sidebarCollapsed ? "4px" : "8px",
            cursor: "pointer",
          }}
          onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
        >
          <div style={{
            width: "36px",
            height: "36px",
            borderRadius: "10px",
            background: "linear-gradient(135deg, #6c5ce7, #a29bfe)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "18px",
            fontWeight: "800",
            flexShrink: 0,
          }}>
            N
          </div>
          {!sidebarCollapsed && (
            <span style={{ fontSize: "20px", fontWeight: "700", letterSpacing: "-0.5px" }}>NexaCRM</span>
          )}
        </div>

        {/* Nav Items */}
        <div style={{ display: "flex", flexDirection: "column", gap: "4px", flex: 1 }}>
          {navItems.map((item) => {
            const isActive = location.pathname === item.path ||
              (item.path === "/contact" && location.pathname.startsWith("/contact/")) ||
              (item.path === "/dashboard" && location.pathname === "/");
            return (
              <a
                key={item.path}
                onClick={(e) => { e.preventDefault(); navigate(item.path); }}
                href={item.path}
                style={{
                  color: isActive ? "#ffffff" : "rgba(255,255,255,0.55)",
                  textDecoration: "none",
                  padding: sidebarCollapsed ? "10px" : "10px 14px",
                  display: "flex",
                  alignItems: "center",
                  gap: "12px",
                  background: isActive ? "rgba(108, 92, 231, 0.25)" : "transparent",
                  borderRadius: "10px",
                  cursor: "pointer",
                  fontSize: "14px",
                  fontWeight: isActive ? "600" : "400",
                  transition: "all 150ms ease",
                  justifyContent: sidebarCollapsed ? "center" : "flex-start",
                  position: "relative",
                }}
                onMouseEnter={(e) => {
                  if (!isActive) e.currentTarget.style.background = "rgba(255,255,255,0.06)";
                  if (!isActive) e.currentTarget.style.color = "rgba(255,255,255,0.85)";
                }}
                onMouseLeave={(e) => {
                  if (!isActive) e.currentTarget.style.background = "transparent";
                  if (!isActive) e.currentTarget.style.color = "rgba(255,255,255,0.55)";
                }}
              >
                {isActive && (
                  <div style={{
                    position: "absolute",
                    left: sidebarCollapsed ? "-6px" : "-12px",
                    top: "50%",
                    transform: "translateY(-50%)",
                    width: "3px",
                    height: "20px",
                    borderRadius: "0 3px 3px 0",
                    background: "#6c5ce7",
                  }} />
                )}
                <span style={{ fontSize: "16px", width: "20px", textAlign: "center", flexShrink: 0 }}>{item.icon}</span>
                {!sidebarCollapsed && <span>{item.label}</span>}
              </a>
            );
          })}
        </div>

        {/* User Section */}
        {user && !sidebarCollapsed && (
          <div style={{
            borderTop: "1px solid rgba(255,255,255,0.08)",
            paddingTop: "16px",
            marginTop: "auto",
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
              <div style={{
                width: "34px",
                height: "34px",
                borderRadius: "10px",
                background: "linear-gradient(135deg, #6c5ce7, #a29bfe)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "13px",
                fontWeight: "700",
                flexShrink: 0,
              }}>
                {user.first_name?.[0]}{user.last_name?.[0]}
              </div>
              <div style={{ overflow: "hidden" }}>
                <div style={{ fontSize: "13px", fontWeight: "600", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                  {user.first_name} {user.last_name}
                </div>
                <div style={{ fontSize: "11px", opacity: 0.5, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                  {user.email}
                </div>
              </div>
            </div>
            <button
              onClick={handleLogout}
              style={{
                width: "100%",
                padding: "8px",
                background: "rgba(255,255,255,0.06)",
                color: "rgba(255,255,255,0.6)",
                border: "1px solid rgba(255,255,255,0.08)",
                borderRadius: "8px",
                cursor: "pointer",
                fontSize: "13px",
                fontFamily: "inherit",
                fontWeight: "500",
                transition: "all 150ms ease",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "rgba(239, 68, 68, 0.15)";
                e.currentTarget.style.borderColor = "rgba(239, 68, 68, 0.3)";
                e.currentTarget.style.color = "#fca5a5";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "rgba(255,255,255,0.06)";
                e.currentTarget.style.borderColor = "rgba(255,255,255,0.08)";
                e.currentTarget.style.color = "rgba(255,255,255,0.6)";
              }}
            >
              Sign Out
            </button>
          </div>
        )}
      </nav>

      {/* Main Content */}
      <main style={{
        flex: 1,
        padding: "32px 40px",
        overflowY: "auto",
        background: "#f0f2f5",
      }}>
        <div style={{ maxWidth: "1400px", animation: "fadeIn 0.3s ease-out" }}>
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;
