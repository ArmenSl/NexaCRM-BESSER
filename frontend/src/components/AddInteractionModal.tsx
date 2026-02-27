import React, { useState } from "react";
import axios from "axios";
import { useAuth } from "../contexts/AuthContext";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface Props {
  contactId: number;
  onClose: () => void;
  onSaved: () => void;
}

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
    <div style={{ position: "fixed", top: 0, left: 0, right: 0, bottom: 0, background: "rgba(0,0,0,0.5)", display: "flex", justifyContent: "center", alignItems: "center", zIndex: 1000 }}>
      <div style={{ background: "white", borderRadius: "12px", padding: "30px", width: "500px", maxHeight: "80vh", overflowY: "auto" }}>
        <h2 style={{ marginTop: 0, color: "#333" }}>Add Interaction</h2>
        {error && <div style={{ background: "#fee", color: "#c00", padding: "8px", borderRadius: "6px", marginBottom: "12px", fontSize: "14px" }}>{error}</div>}
        <div style={{ marginBottom: "15px" }}>
          <label style={{ display: "block", marginBottom: "5px", fontWeight: "bold", fontSize: "14px" }}>Type</label>
          <select value={type} onChange={(e) => setType(e.target.value)} style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #ddd" }}>
            <option value="CALL">Call</option>
            <option value="EMAIL">Email</option>
            <option value="MEETING">Meeting</option>
            <option value="NOTE">Note</option>
          </select>
        </div>
        <div style={{ marginBottom: "15px" }}>
          <label style={{ display: "block", marginBottom: "5px", fontWeight: "bold", fontSize: "14px" }}>Direction</label>
          <select value={direction} onChange={(e) => setDirection(e.target.value)} style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #ddd" }}>
            <option value="OUTBOUND">Outbound</option>
            <option value="INBOUND">Inbound</option>
          </select>
        </div>
        <div style={{ marginBottom: "15px" }}>
          <label style={{ display: "block", marginBottom: "5px", fontWeight: "bold", fontSize: "14px" }}>Subject</label>
          <input type="text" value={subject} onChange={(e) => setSubject(e.target.value)} placeholder="Optional subject" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #ddd", boxSizing: "border-box" }} />
        </div>
        <div style={{ marginBottom: "20px" }}>
          <label style={{ display: "block", marginBottom: "5px", fontWeight: "bold", fontSize: "14px" }}>Content</label>
          <textarea value={content} onChange={(e) => setContent(e.target.value)} rows={4} placeholder="Interaction details..." style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #ddd", boxSizing: "border-box", resize: "vertical" }} />
        </div>
        <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
          <button onClick={onClose} style={{ padding: "8px 20px", borderRadius: "6px", border: "1px solid #ddd", background: "white", cursor: "pointer" }}>Cancel</button>
          <button onClick={handleSave} disabled={saving} style={{ padding: "8px 20px", borderRadius: "6px", border: "none", background: "#5a3d91", color: "white", cursor: saving ? "not-allowed" : "pointer", opacity: saving ? 0.7 : 1 }}>
            {saving ? "Saving..." : "Save"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddInteractionModal;
