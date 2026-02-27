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

const inputStyle: React.CSSProperties = {
  padding: "7px 10px", borderRadius: "10px", border: "1.5px solid #e5e7eb",
  fontSize: "13px", fontFamily: "inherit", outline: "none",
  transition: "border-color 150ms, box-shadow 150ms",
};

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
    <div style={{
      background: "white", borderRadius: "14px", padding: "20px", marginBottom: "20px",
      boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)",
    }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "14px" }}>
        <h3 style={{ margin: 0, fontSize: "15px", fontWeight: "700", color: "#1a1a2e" }}>Filters</h3>
        <button onClick={clearFilters} style={{
          background: "none", border: "none", color: "#9ca3af", cursor: "pointer",
          fontSize: "13px", fontFamily: "inherit", fontWeight: "500",
        }}
          onMouseEnter={(e) => { e.currentTarget.style.color = "#6c5ce7"; }}
          onMouseLeave={(e) => { e.currentTarget.style.color = "#9ca3af"; }}
        >Clear All</button>
      </div>
      <div style={{ display: "flex", gap: "16px", flexWrap: "wrap", alignItems: "flex-end" }}>
        {/* Stage pills */}
        <div>
          <label style={{ display: "block", fontSize: "12px", color: "#9ca3af", marginBottom: "6px", fontWeight: "600" }}>Stages</label>
          <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
            {STAGES.map((s) => (
              <button
                key={s}
                onClick={() => toggleStage(s)}
                style={{
                  padding: "5px 12px", borderRadius: "20px",
                  border: filters.stages.includes(s) ? "1.5px solid #6c5ce7" : "1.5px solid #e5e7eb",
                  background: filters.stages.includes(s) ? "#6c5ce7" : "white",
                  color: filters.stages.includes(s) ? "white" : "#6b7280",
                  cursor: "pointer", fontSize: "12px", fontWeight: "600", fontFamily: "inherit",
                  transition: "all 150ms ease",
                }}
              >
                {s.replace(/_/g, " ")}
              </button>
            ))}
          </div>
        </div>

        {/* Value range */}
        <div style={{ display: "flex", gap: "8px", alignItems: "flex-end" }}>
          <div>
            <label style={{ display: "block", fontSize: "12px", color: "#9ca3af", marginBottom: "6px", fontWeight: "600" }}>Min Value</label>
            <input type="number" value={filters.minValue} onChange={(e) => setFilters({ ...filters, minValue: e.target.value })} placeholder="0"
              style={{ ...inputStyle, width: "85px" }}
              onFocus={(e) => { e.target.style.borderColor = "#6c5ce7"; e.target.style.boxShadow = "0 0 0 3px rgba(108,92,231,0.1)"; }}
              onBlur={(e) => { e.target.style.borderColor = "#e5e7eb"; e.target.style.boxShadow = "none"; }}
            />
          </div>
          <div>
            <label style={{ display: "block", fontSize: "12px", color: "#9ca3af", marginBottom: "6px", fontWeight: "600" }}>Max Value</label>
            <input type="number" value={filters.maxValue} onChange={(e) => setFilters({ ...filters, maxValue: e.target.value })} placeholder="any"
              style={{ ...inputStyle, width: "85px" }}
              onFocus={(e) => { e.target.style.borderColor = "#6c5ce7"; e.target.style.boxShadow = "0 0 0 3px rgba(108,92,231,0.1)"; }}
              onBlur={(e) => { e.target.style.borderColor = "#e5e7eb"; e.target.style.boxShadow = "none"; }}
            />
          </div>
        </div>

        {/* Probability range */}
        <div style={{ display: "flex", gap: "8px", alignItems: "flex-end" }}>
          <div>
            <label style={{ display: "block", fontSize: "12px", color: "#9ca3af", marginBottom: "6px", fontWeight: "600" }}>Min Prob%</label>
            <input type="number" value={filters.minProbability} onChange={(e) => setFilters({ ...filters, minProbability: e.target.value })} placeholder="0" min={0} max={100}
              style={{ ...inputStyle, width: "65px" }}
              onFocus={(e) => { e.target.style.borderColor = "#6c5ce7"; e.target.style.boxShadow = "0 0 0 3px rgba(108,92,231,0.1)"; }}
              onBlur={(e) => { e.target.style.borderColor = "#e5e7eb"; e.target.style.boxShadow = "none"; }}
            />
          </div>
          <div>
            <label style={{ display: "block", fontSize: "12px", color: "#9ca3af", marginBottom: "6px", fontWeight: "600" }}>Max Prob%</label>
            <input type="number" value={filters.maxProbability} onChange={(e) => setFilters({ ...filters, maxProbability: e.target.value })} placeholder="100" min={0} max={100}
              style={{ ...inputStyle, width: "65px" }}
              onFocus={(e) => { e.target.style.borderColor = "#6c5ce7"; e.target.style.boxShadow = "0 0 0 3px rgba(108,92,231,0.1)"; }}
              onBlur={(e) => { e.target.style.borderColor = "#e5e7eb"; e.target.style.boxShadow = "none"; }}
            />
          </div>
        </div>

        {/* Owner */}
        <div>
          <label style={{ display: "block", fontSize: "12px", color: "#9ca3af", marginBottom: "6px", fontWeight: "600" }}>Owner</label>
          <select value={filters.ownerId} onChange={(e) => setFilters({ ...filters, ownerId: e.target.value })}
            style={{ ...inputStyle, padding: "7px 10px" }}>
            <option value="">All</option>
            {users.map((u: any) => (
              <option key={u.id} value={u.id}>{u.first_name} {u.last_name}</option>
            ))}
          </select>
        </div>

        <button onClick={applyFilters} style={{
          padding: "8px 20px", borderRadius: "10px", border: "none",
          background: "linear-gradient(135deg, #6c5ce7, #5a4bd1)", color: "white",
          cursor: "pointer", fontSize: "13px", fontWeight: "600", fontFamily: "inherit",
          boxShadow: "0 4px 12px rgba(108,92,231,0.25)", transition: "all 150ms ease",
        }}
          onMouseEnter={(e) => { e.currentTarget.style.transform = "translateY(-1px)"; }}
          onMouseLeave={(e) => { e.currentTarget.style.transform = "translateY(0)"; }}
        >
          Apply
        </button>
      </div>
    </div>
  );
};

export default PipelineFilters;
