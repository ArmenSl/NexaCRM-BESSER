import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const STAGES = ["PROSPECTING", "QUALIFICATION", "PROPOSAL", "NEGOTIATION", "CLOSED_WON", "CLOSED_LOST"];

interface Filters {
  stages: string[];
  minValue: string;
  maxValue: string;
  minProbability: string;
  maxProbability: string;
  ownerId: string;
}

interface Props {
  onFilterChange: (params: Record<string, string>) => void;
}

const PipelineFilters: React.FC<Props> = ({ onFilterChange }) => {
  const [filters, setFilters] = useState<Filters>({ stages: [], minValue: "", maxValue: "", minProbability: "", maxProbability: "", ownerId: "" });
  const [users, setUsers] = useState<any[]>([]);

  useEffect(() => {
    axios.get(`${API_URL}/user/`).then((res) => setUsers(Array.isArray(res.data) ? res.data : [])).catch(() => {});
  }, []);

  const applyFilters = () => {
    const params: Record<string, string> = {};
    if (filters.stages.length > 0) params.stage = filters.stages.join(",");
    if (filters.minValue) params.min_value = filters.minValue;
    if (filters.maxValue) params.max_value = filters.maxValue;
    if (filters.minProbability) params.min_probability = filters.minProbability;
    if (filters.maxProbability) params.max_probability = filters.maxProbability;
    if (filters.ownerId) params.owner_id = filters.ownerId;
    onFilterChange(params);
  };

  const clearFilters = () => {
    setFilters({ stages: [], minValue: "", maxValue: "", minProbability: "", maxProbability: "", ownerId: "" });
    onFilterChange({});
  };

  const toggleStage = (stage: string) => {
    setFilters((prev) => ({
      ...prev,
      stages: prev.stages.includes(stage) ? prev.stages.filter((s) => s !== stage) : [...prev.stages, stage],
    }));
  };

  return (
    <div style={{ background: "white", borderRadius: "8px", padding: "16px", marginBottom: "20px", boxShadow: "0 1px 3px rgba(0,0,0,0.06)" }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "12px" }}>
        <h3 style={{ margin: 0, fontSize: "16px", color: "#333" }}>Pipeline Filters</h3>
        <button onClick={clearFilters} style={{ background: "none", border: "none", color: "#999", cursor: "pointer", fontSize: "13px" }}>Clear All</button>
      </div>
      <div style={{ display: "flex", gap: "12px", flexWrap: "wrap", alignItems: "flex-end" }}>
        {/* Stage pills */}
        <div>
          <label style={{ display: "block", fontSize: "12px", color: "#666", marginBottom: "4px" }}>Stages</label>
          <div style={{ display: "flex", gap: "4px", flexWrap: "wrap" }}>
            {STAGES.map((s) => (
              <button
                key={s}
                onClick={() => toggleStage(s)}
                style={{
                  padding: "4px 10px",
                  borderRadius: "12px",
                  border: "1px solid #ddd",
                  background: filters.stages.includes(s) ? "#5a3d91" : "white",
                  color: filters.stages.includes(s) ? "white" : "#666",
                  cursor: "pointer",
                  fontSize: "12px",
                }}
              >
                {s.replace("_", " ")}
              </button>
            ))}
          </div>
        </div>

        {/* Value range */}
        <div style={{ display: "flex", gap: "6px", alignItems: "flex-end" }}>
          <div>
            <label style={{ display: "block", fontSize: "12px", color: "#666", marginBottom: "4px" }}>Min Value</label>
            <input type="number" value={filters.minValue} onChange={(e) => setFilters({ ...filters, minValue: e.target.value })} placeholder="0" style={{ width: "80px", padding: "4px 8px", borderRadius: "4px", border: "1px solid #ddd", fontSize: "13px" }} />
          </div>
          <div>
            <label style={{ display: "block", fontSize: "12px", color: "#666", marginBottom: "4px" }}>Max Value</label>
            <input type="number" value={filters.maxValue} onChange={(e) => setFilters({ ...filters, maxValue: e.target.value })} placeholder="any" style={{ width: "80px", padding: "4px 8px", borderRadius: "4px", border: "1px solid #ddd", fontSize: "13px" }} />
          </div>
        </div>

        {/* Probability range */}
        <div style={{ display: "flex", gap: "6px", alignItems: "flex-end" }}>
          <div>
            <label style={{ display: "block", fontSize: "12px", color: "#666", marginBottom: "4px" }}>Min Prob%</label>
            <input type="number" value={filters.minProbability} onChange={(e) => setFilters({ ...filters, minProbability: e.target.value })} placeholder="0" min={0} max={100} style={{ width: "60px", padding: "4px 8px", borderRadius: "4px", border: "1px solid #ddd", fontSize: "13px" }} />
          </div>
          <div>
            <label style={{ display: "block", fontSize: "12px", color: "#666", marginBottom: "4px" }}>Max Prob%</label>
            <input type="number" value={filters.maxProbability} onChange={(e) => setFilters({ ...filters, maxProbability: e.target.value })} placeholder="100" min={0} max={100} style={{ width: "60px", padding: "4px 8px", borderRadius: "4px", border: "1px solid #ddd", fontSize: "13px" }} />
          </div>
        </div>

        {/* Owner */}
        <div>
          <label style={{ display: "block", fontSize: "12px", color: "#666", marginBottom: "4px" }}>Owner</label>
          <select value={filters.ownerId} onChange={(e) => setFilters({ ...filters, ownerId: e.target.value })} style={{ padding: "4px 8px", borderRadius: "4px", border: "1px solid #ddd", fontSize: "13px" }}>
            <option value="">All</option>
            {users.map((u: any) => (
              <option key={u.id} value={u.id}>{u.first_name} {u.last_name}</option>
            ))}
          </select>
        </div>

        <button onClick={applyFilters} style={{ padding: "6px 16px", borderRadius: "6px", border: "none", background: "#5a3d91", color: "white", cursor: "pointer", fontSize: "13px", height: "30px" }}>
          Apply
        </button>
      </div>
    </div>
  );
};

export default PipelineFilters;
