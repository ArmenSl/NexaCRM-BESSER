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

const typeConfig: Record<string, { color: string; icon: string }> = {
  CALL: { color: "#3498db", icon: "\u260E" },
  EMAIL: { color: "#27ae60", icon: "\u2709" },
  MEETING: { color: "#e67e22", icon: "\uD83D\uDCC5" },
  NOTE: { color: "#95a5a6", icon: "\uD83D\uDCDD" },
};

const InteractionTimeline: React.FC<{ interactions: Interaction[] }> = ({ interactions }) => {
  const [expandedId, setExpandedId] = useState<number | null>(null);

  if (!interactions || interactions.length === 0) {
    return <p style={{ color: "#999", fontStyle: "italic" }}>No interactions yet.</p>;
  }

  return (
    <div style={{ position: "relative", paddingLeft: "30px" }}>
      <div style={{ position: "absolute", left: "14px", top: "0", bottom: "0", width: "2px", background: "#e0e0e0" }} />
      {interactions.map((ix) => {
        const cfg = typeConfig[ix.type] || { color: "#999", icon: "?" };
        const isExpanded = expandedId === ix.id;
        return (
          <div key={ix.id} style={{ marginBottom: "20px", position: "relative" }}>
            <div
              style={{
                position: "absolute",
                left: "-22px",
                top: "4px",
                width: "24px",
                height: "24px",
                borderRadius: "50%",
                background: cfg.color,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "12px",
                color: "white",
                zIndex: 1,
              }}
            >
              {cfg.icon}
            </div>
            <div
              style={{ background: "white", borderRadius: "8px", padding: "12px 16px", boxShadow: "0 1px 3px rgba(0,0,0,0.08)", cursor: "pointer" }}
              onClick={() => setExpandedId(isExpanded ? null : ix.id)}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  <span style={{ fontWeight: "bold", fontSize: "14px", color: "#333" }}>{ix.subject || ix.type}</span>
                  <span style={{ background: cfg.color, color: "white", padding: "2px 8px", borderRadius: "10px", fontSize: "11px" }}>{ix.type}</span>
                  {ix.direction && (
                    <span style={{ background: "#f0f0f0", padding: "2px 8px", borderRadius: "10px", fontSize: "11px", color: "#666" }}>{ix.direction}</span>
                  )}
                </div>
                <span style={{ fontSize: "12px", color: "#999" }}>
                  {new Date(ix.occurred_at).toLocaleDateString()} {new Date(ix.occurred_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </span>
              </div>
              {ix.performed_by_name && <div style={{ fontSize: "12px", color: "#888", marginTop: "4px" }}>by {ix.performed_by_name}</div>}
              {isExpanded && (
                <div style={{ marginTop: "10px", paddingTop: "10px", borderTop: "1px solid #eee", fontSize: "14px", color: "#555", lineHeight: "1.5" }}>
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
