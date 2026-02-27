import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const stageColors: Record<string, string> = {
  PROSPECTING: "#3498db",
  QUALIFICATION: "#9b59b6",
  PROPOSAL: "#e67e22",
  NEGOTIATION: "#f39c12",
  CLOSED_WON: "#27ae60",
  CLOSED_LOST: "#e74c3c",
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
    <div style={{ display: "flex", gap: "12px", marginBottom: "20px", flexWrap: "wrap" }}>
      {data.map((s) => (
        <div key={s.stage} style={{ flex: "1", minWidth: "150px", background: "white", borderRadius: "8px", padding: "16px", borderTop: `3px solid ${stageColors[s.stage] || "#999"}`, boxShadow: "0 1px 3px rgba(0,0,0,0.06)" }}>
          <div style={{ fontSize: "12px", color: "#888", marginBottom: "4px", textTransform: "uppercase" }}>{s.stage.replace("_", " ")}</div>
          <div style={{ fontSize: "22px", fontWeight: "bold", color: "#333" }}>{s.count}</div>
          <div style={{ fontSize: "13px", color: "#666", marginTop: "4px" }}>${Number(s.total_value).toLocaleString()}</div>
          <div style={{ fontSize: "11px", color: "#999" }}>{s.avg_probability}% avg prob.</div>
        </div>
      ))}
    </div>
  );
};

export default PipelineSummary;
