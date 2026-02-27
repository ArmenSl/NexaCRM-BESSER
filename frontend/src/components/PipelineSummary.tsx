import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const stageColors: Record<string, { color: string; bg: string }> = {
  PROSPECTING: { color: "#3b82f6", bg: "#eff6ff" },
  QUALIFICATION: { color: "#8b5cf6", bg: "#f5f3ff" },
  PROPOSAL: { color: "#f59e0b", bg: "#fffbeb" },
  NEGOTIATION: { color: "#d97706", bg: "#fef3c7" },
  CLOSED_WON: { color: "#10b981", bg: "#ecfdf5" },
  CLOSED_LOST: { color: "#ef4444", bg: "#fef2f2" },
};

interface StageSummary {
  stage: string;
  count: number;
  total_value: number;
  avg_probability: number;
}

const PipelineSummary: React.FC = () => {
  const [data, setData] = useState<StageSummary[]>([]);

  useEffect(() => {
    axios.get(`${API_URL}/opportunity/pipeline-summary/`).then((res) => {
      setData(Array.isArray(res.data) ? res.data : []);
    }).catch(() => {});
  }, []);

  if (data.length === 0) return null;

  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: "14px", marginBottom: "20px" }}>
      {data.map((s) => {
        const cfg = stageColors[s.stage] || { color: "#6b7280", bg: "#f3f4f6" };
        return (
          <div key={s.stage} style={{
            background: "white", borderRadius: "14px", padding: "18px",
            borderLeft: `4px solid ${cfg.color}`,
            boxShadow: "0 1px 3px rgba(0,0,0,0.04)",
          }}>
            <div style={{ fontSize: "11px", color: "#9ca3af", marginBottom: "6px", textTransform: "uppercase", fontWeight: "600", letterSpacing: "0.5px" }}>
              {s.stage.replace(/_/g, " ")}
            </div>
            <div style={{ fontSize: "26px", fontWeight: "800", color: cfg.color, lineHeight: 1 }}>{s.count}</div>
            <div style={{ fontSize: "13px", color: "#6b7280", marginTop: "6px", fontWeight: "500" }}>${Number(s.total_value).toLocaleString()}</div>
            <div style={{
              marginTop: "8px", display: "inline-block",
              background: cfg.bg, color: cfg.color,
              padding: "2px 10px", borderRadius: "20px",
              fontSize: "11px", fontWeight: "600",
            }}>
              {s.avg_probability}% avg
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default PipelineSummary;
