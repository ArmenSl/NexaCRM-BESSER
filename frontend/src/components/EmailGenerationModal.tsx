import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface Props {
  contactId: number;
  onClose: () => void;
  onSaved: () => void;
}

const EmailGenerationModal: React.FC<Props> = ({ contactId, onClose, onSaved }) => {
  const [step, setStep] = useState<"configure" | "preview">("configure");
  const [templates, setTemplates] = useState<any[]>([]);
  const [templateId, setTemplateId] = useState<number | null>(null);
  const [instructions, setInstructions] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    axios.get(`${API_URL}/emailtemplate/`).then((res) => {
      setTemplates(Array.isArray(res.data) ? res.data : []);
    }).catch(() => {});
  }, []);

  const handleGenerate = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await axios.post(`${API_URL}/contact/${contactId}/generate-email/`, {
        template_id: templateId,
        custom_instructions: instructions || null,
      });
      setSubject(res.data.subject);
      setBody(res.data.body);
      setStep("preview");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Generation failed");
    }
    setLoading(false);
  };

  const handleSave = async () => {
    setSaving(true);
    setError("");
    try {
      await axios.post(`${API_URL}/contact/${contactId}/save-generated-email/`, {
        subject,
        body,
        template_id: templateId,
      });
      onSaved();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to save");
    }
    setSaving(false);
  };

  return (
    <div style={{ position: "fixed", top: 0, left: 0, right: 0, bottom: 0, background: "rgba(0,0,0,0.5)", display: "flex", justifyContent: "center", alignItems: "center", zIndex: 1000 }}>
      <div style={{ background: "white", borderRadius: "12px", padding: "30px", width: "600px", maxHeight: "85vh", overflowY: "auto" }}>
        <h2 style={{ marginTop: 0, color: "#333" }}>Generate Email</h2>
        {error && <div style={{ background: "#fee", color: "#c00", padding: "8px", borderRadius: "6px", marginBottom: "12px", fontSize: "14px" }}>{error}</div>}

        {step === "configure" && (
          <>
            <div style={{ marginBottom: "15px" }}>
              <label style={{ display: "block", marginBottom: "5px", fontWeight: "bold", fontSize: "14px" }}>Template (optional)</label>
              <select value={templateId ?? ""} onChange={(e) => setTemplateId(e.target.value ? Number(e.target.value) : null)} style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #ddd" }}>
                <option value="">No template - generate freely</option>
                {templates.map((t: any) => (
                  <option key={t.id} value={t.id}>{t.name} ({t.category})</option>
                ))}
              </select>
            </div>
            <div style={{ marginBottom: "20px" }}>
              <label style={{ display: "block", marginBottom: "5px", fontWeight: "bold", fontSize: "14px" }}>Custom Instructions (optional)</label>
              <textarea value={instructions} onChange={(e) => setInstructions(e.target.value)} rows={3} placeholder="E.g., Mention our new product launch..." style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #ddd", boxSizing: "border-box", resize: "vertical" }} />
            </div>
            <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
              <button onClick={onClose} style={{ padding: "8px 20px", borderRadius: "6px", border: "1px solid #ddd", background: "white", cursor: "pointer" }}>Cancel</button>
              <button onClick={handleGenerate} disabled={loading} style={{ padding: "8px 20px", borderRadius: "6px", border: "none", background: "#5a3d91", color: "white", cursor: loading ? "not-allowed" : "pointer", opacity: loading ? 0.7 : 1 }}>
                {loading ? "Generating..." : "Generate Email"}
              </button>
            </div>
          </>
        )}

        {step === "preview" && (
          <>
            <div style={{ marginBottom: "15px" }}>
              <label style={{ display: "block", marginBottom: "5px", fontWeight: "bold", fontSize: "14px" }}>Subject</label>
              <input type="text" value={subject} onChange={(e) => setSubject(e.target.value)} style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #ddd", boxSizing: "border-box" }} />
            </div>
            <div style={{ marginBottom: "20px" }}>
              <label style={{ display: "block", marginBottom: "5px", fontWeight: "bold", fontSize: "14px" }}>Body</label>
              <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={10} style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #ddd", boxSizing: "border-box", resize: "vertical", fontFamily: "inherit", lineHeight: "1.5" }} />
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <button onClick={() => setStep("configure")} style={{ padding: "8px 20px", borderRadius: "6px", border: "1px solid #ddd", background: "white", cursor: "pointer" }}>Back</button>
              <div style={{ display: "flex", gap: "10px" }}>
                <button onClick={onClose} style={{ padding: "8px 20px", borderRadius: "6px", border: "1px solid #ddd", background: "white", cursor: "pointer" }}>Discard</button>
                <button onClick={handleSave} disabled={saving} style={{ padding: "8px 20px", borderRadius: "6px", border: "none", background: "#27ae60", color: "white", cursor: saving ? "not-allowed" : "pointer", opacity: saving ? 0.7 : 1 }}>
                  {saving ? "Saving..." : "Save Email"}
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default EmailGenerationModal;
