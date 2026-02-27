import React, { useState } from "react";
import axios from "axios";
import { useAuth } from "../contexts/AuthContext";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface Props {
  contactId: number;
  onClose: () => void;
  onSaved: () => void;
}

const labelStyle: React.CSSProperties = {
  display: "block", marginBottom: "6px", color: "#374151",
  fontSize: "13px", fontWeight: "600",
};

const fieldStyle: React.CSSProperties = {
  width: "100%", padding: "10px 14px", borderRadius: "10px",
  border: "1.5px solid #e5e7eb", fontSize: "14px", fontFamily: "inherit",
  outline: "none", boxSizing: "border-box",
  transition: "border-color 150ms, box-shadow 150ms",
};

const focusHandler = (e: React.FocusEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
  e.target.style.borderColor = "#6c5ce7";
  e.target.style.boxShadow = "0 0 0 3px rgba(108,92,231,0.1)";
};
const blurHandler = (e: React.FocusEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
  e.target.style.borderColor = "#e5e7eb";
  e.target.style.boxShadow = "none";
};

const AddInteractionModal: React.FC<Props> = ({ contactId, onClose, onSaved }) => {
  const { user } = useAuth();
  const [type, setType] = useState("CALL");
  const [direction, setDirection] = useState("OUTBOUND");
  const [subject, setSubject] = useState("");
  const [content, setContent] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const handleSave = async () => {
    if (!content.trim()) {
      setError("Content is required");
      return;
    }
    setSaving(true);
    setError("");
    try {
      const now = new Date().toISOString();
      await axios.post(`${API_URL}/interaction/`, {
        type,
        direction,
        subject: subject || null,
        content,
        occurred_at: now,
        created_at: now,
        id: 0,
        performed_by: user?.user_id || 1,
        contact: contactId,
      });
      onSaved();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to save interaction");
    }
    setSaving(false);
  };

  return (
    <div style={{
      position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
      background: "rgba(0,0,0,0.4)", backdropFilter: "blur(4px)",
      display: "flex", justifyContent: "center", alignItems: "center", zIndex: 1000,
      animation: "fadeIn 0.2s ease-out",
    }}>
      <div style={{
        background: "white", borderRadius: "16px", padding: "32px", width: "500px",
        maxHeight: "80vh", overflowY: "auto",
        boxShadow: "0 20px 60px rgba(0,0,0,0.15)",
        animation: "slideUp 0.25s ease-out",
      }}>
        <h2 style={{ marginTop: 0, marginBottom: "20px", color: "#1a1a2e", fontSize: "20px", fontWeight: "700", letterSpacing: "-0.3px" }}>Add Interaction</h2>
        {error && (
          <div style={{ background: "#fef2f2", color: "#dc2626", padding: "10px 14px", borderRadius: "10px", marginBottom: "16px", fontSize: "13px", fontWeight: "500", border: "1px solid #fecaca" }}>{error}</div>
        )}
        <div style={{ marginBottom: "18px" }}>
          <label style={labelStyle}>Type</label>
          <select value={type} onChange={(e) => setType(e.target.value)} style={fieldStyle} onFocus={focusHandler as any} onBlur={blurHandler as any}>
            <option value="CALL">Call</option>
            <option value="EMAIL">Email</option>
            <option value="MEETING">Meeting</option>
            <option value="NOTE">Note</option>
          </select>
        </div>
        <div style={{ marginBottom: "18px" }}>
          <label style={labelStyle}>Direction</label>
          <select value={direction} onChange={(e) => setDirection(e.target.value)} style={fieldStyle} onFocus={focusHandler as any} onBlur={blurHandler as any}>
            <option value="OUTBOUND">Outbound</option>
            <option value="INBOUND">Inbound</option>
          </select>
        </div>
        <div style={{ marginBottom: "18px" }}>
          <label style={labelStyle}>Subject</label>
          <input type="text" value={subject} onChange={(e) => setSubject(e.target.value)} placeholder="Optional subject" style={fieldStyle} onFocus={focusHandler} onBlur={blurHandler} />
        </div>
        <div style={{ marginBottom: "24px" }}>
          <label style={labelStyle}>Content</label>
          <textarea value={content} onChange={(e) => setContent(e.target.value)} rows={4} placeholder="Interaction details..."
            style={{ ...fieldStyle, resize: "vertical" }} onFocus={focusHandler as any} onBlur={blurHandler as any} />
        </div>
        <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
          <button onClick={onClose} style={{
            padding: "10px 20px", borderRadius: "10px", border: "1.5px solid #e5e7eb",
            background: "white", cursor: "pointer", fontFamily: "inherit",
            fontSize: "13px", fontWeight: "600", color: "#6b7280",
          }}>Cancel</button>
          <button onClick={handleSave} disabled={saving} style={{
            padding: "10px 20px", borderRadius: "10px", border: "none",
            background: saving ? "#a29bfe" : "linear-gradient(135deg, #6c5ce7, #5a4bd1)",
            color: "white", cursor: saving ? "not-allowed" : "pointer",
            fontFamily: "inherit", fontSize: "13px", fontWeight: "600",
            boxShadow: saving ? "none" : "0 4px 12px rgba(108,92,231,0.25)",
          }}>
            {saving ? "Saving..." : "Save"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddInteractionModal;
