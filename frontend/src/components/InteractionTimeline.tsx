import React, { useState } from "react";

interface Interaction {
  id: number;
  type: string;
  direction?: string;
  subject?: string;
  content: string;
  occurred_at: string;
  performed_by_name?: string;
}

const typeConfig: Record<string, { color: string; bg: string; icon: string }> = {
  CALL: { color: "#3b82f6", bg: "#eff6ff", icon: "\u260E" },
  EMAIL: { color: "#10b981", bg: "#ecfdf5", icon: "\u2709" },
  MEETING: { color: "#f59e0b", bg: "#fffbeb", icon: "\uD83D\uDCC5" },
  NOTE: { color: "#9ca3af", bg: "#f3f4f6", icon: "\uD83D\uDCDD" },
};

const InteractionTimeline: React.FC<{ interactions: Interaction[] }> = ({ interactions }) => {
  const [expandedId, setExpandedId] = useState<number | null>(null);

  if (!interactions || interactions.length === 0) {
    return <p style={{ color: "#9ca3af", fontStyle: "italic", fontSize: "14px" }}>No interactions yet.</p>;
  }

  return (
    <div style={{ position: "relative", paddingLeft: "32px" }}>
      <div style={{ position: "absolute", left: "14px", top: "0", bottom: "0", width: "2px", background: "#e5e7eb", borderRadius: "1px" }} />
      {interactions.map((ix) => {
        const cfg = typeConfig[ix.type] || { color: "#9ca3af", bg: "#f3f4f6", icon: "?" };
        const isExpanded = expandedId === ix.id;
        return (
          <div key={ix.id} style={{ marginBottom: "16px", position: "relative" }}>
            <div style={{
              position: "absolute", left: "-24px", top: "6px",
              width: "24px", height: "24px", borderRadius: "50%",
              background: cfg.color,
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: "11px", color: "white", zIndex: 1,
              boxShadow: `0 0 0 3px ${cfg.bg}`,
            }}>
              {cfg.icon}
            </div>
            <div
              style={{
                background: "white", borderRadius: "12px", padding: "14px 18px",
                boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)",
                cursor: "pointer", transition: "box-shadow 150ms ease",
              }}
              onClick={() => setExpandedId(isExpanded ? null : ix.id)}
              onMouseEnter={(e) => { e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.08)"; }}
              onMouseLeave={(e) => { e.currentTarget.style.boxShadow = "0 1px 3px rgba(0,0,0,0.04)"; }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  <span style={{ fontWeight: "600", fontSize: "14px", color: "#1a1a2e" }}>{ix.subject || ix.type}</span>
                  <span style={{ background: cfg.bg, color: cfg.color, padding: "2px 10px", borderRadius: "20px", fontSize: "11px", fontWeight: "600" }}>{ix.type}</span>
                  {ix.direction && (
                    <span style={{ background: "#f3f4f6", padding: "2px 10px", borderRadius: "20px", fontSize: "11px", color: "#6b7280", fontWeight: "500" }}>{ix.direction}</span>
                  )}
                </div>
                <span style={{ fontSize: "12px", color: "#9ca3af" }}>
                  {new Date(ix.occurred_at).toLocaleDateString()} {new Date(ix.occurred_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </span>
              </div>
              {ix.performed_by_name && <div style={{ fontSize: "12px", color: "#9ca3af", marginTop: "4px" }}>by {ix.performed_by_name}</div>}
              {isExpanded && (
                <div style={{
                  marginTop: "12px", paddingTop: "12px", borderTop: "1px solid #f3f4f6",
                  fontSize: "14px", color: "#4b5563", lineHeight: "1.6",
                }}>
                  {ix.content}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default InteractionTimeline;
