import React, { useState, useEffect } from "react";
import axios from "axios";

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

const btnOutline: React.CSSProperties = {
  padding: "10px 20px", borderRadius: "10px", border: "1.5px solid #e5e7eb",
  background: "white", cursor: "pointer", fontFamily: "inherit",
  fontSize: "13px", fontWeight: "600", color: "#6b7280",
};

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
    <div style={{
      position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
      background: "rgba(0,0,0,0.4)", backdropFilter: "blur(4px)",
      display: "flex", justifyContent: "center", alignItems: "center", zIndex: 1000,
      animation: "fadeIn 0.2s ease-out",
    }}>
      <div style={{
        background: "white", borderRadius: "16px", padding: "32px", width: "600px",
        maxHeight: "85vh", overflowY: "auto",
        boxShadow: "0 20px 60px rgba(0,0,0,0.15)",
        animation: "slideUp 0.25s ease-out",
      }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "20px" }}>
          <h2 style={{ margin: 0, color: "#1a1a2e", fontSize: "20px", fontWeight: "700", letterSpacing: "-0.3px" }}>Generate Email</h2>
          {step === "preview" && (
            <span style={{ background: "#ecfdf5", color: "#10b981", padding: "4px 12px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>Preview</span>
          )}
        </div>
        {error && (
          <div style={{ background: "#fef2f2", color: "#dc2626", padding: "10px 14px", borderRadius: "10px", marginBottom: "16px", fontSize: "13px", fontWeight: "500", border: "1px solid #fecaca" }}>{error}</div>
        )}

        {step === "configure" && (
          <>
            <div style={{ marginBottom: "18px" }}>
              <label style={labelStyle}>Template (optional)</label>
              <select value={templateId ?? ""} onChange={(e) => setTemplateId(e.target.value ? Number(e.target.value) : null)}
                style={fieldStyle} onFocus={focusHandler as any} onBlur={blurHandler as any}>
                <option value="">No template - generate freely</option>
                {templates.map((t: any) => (
                  <option key={t.id} value={t.id}>{t.name} ({t.category})</option>
                ))}
              </select>
            </div>
            <div style={{ marginBottom: "24px" }}>
              <label style={labelStyle}>Custom Instructions (optional)</label>
              <textarea value={instructions} onChange={(e) => setInstructions(e.target.value)} rows={3}
                placeholder="E.g., Mention our new product launch..."
                style={{ ...fieldStyle, resize: "vertical" }} onFocus={focusHandler as any} onBlur={blurHandler as any} />
            </div>
            <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
              <button onClick={onClose} style={btnOutline}>Cancel</button>
              <button onClick={handleGenerate} disabled={loading} style={{
                padding: "10px 20px", borderRadius: "10px", border: "none",
                background: loading ? "#a29bfe" : "linear-gradient(135deg, #6c5ce7, #5a4bd1)",
                color: "white", cursor: loading ? "not-allowed" : "pointer",
                fontFamily: "inherit", fontSize: "13px", fontWeight: "600",
                boxShadow: loading ? "none" : "0 4px 12px rgba(108,92,231,0.25)",
              }}>
                {loading ? "Generating..." : "Generate Email"}
              </button>
            </div>
          </>
        )}

        {step === "preview" && (
          <>
            <div style={{ marginBottom: "18px" }}>
              <label style={labelStyle}>Subject</label>
              <input type="text" value={subject} onChange={(e) => setSubject(e.target.value)}
                style={fieldStyle} onFocus={focusHandler} onBlur={blurHandler} />
            </div>
            <div style={{ marginBottom: "24px" }}>
              <label style={labelStyle}>Body</label>
              <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={10}
                style={{ ...fieldStyle, resize: "vertical", lineHeight: "1.6" }}
                onFocus={focusHandler as any} onBlur={blurHandler as any} />
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <button onClick={() => setStep("configure")} style={btnOutline}>Back</button>
              <div style={{ display: "flex", gap: "10px" }}>
                <button onClick={onClose} style={btnOutline}>Discard</button>
                <button onClick={handleSave} disabled={saving} style={{
                  padding: "10px 20px", borderRadius: "10px", border: "none",
                  background: saving ? "#6ee7b7" : "linear-gradient(135deg, #10b981, #059669)",
                  color: "white", cursor: saving ? "not-allowed" : "pointer",
                  fontFamily: "inherit", fontSize: "13px", fontWeight: "600",
                  boxShadow: saving ? "none" : "0 4px 12px rgba(16,185,129,0.25)",
                }}>
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
