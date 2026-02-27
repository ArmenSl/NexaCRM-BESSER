import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { TableBlock } from "../components/runtime/TableBlock";
import Layout from "../components/Layout";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const Contact: React.FC = () => {
  const navigate = useNavigate();
  const [showLinkedIn, setShowLinkedIn] = useState(false);
  const [linkedinUrl, setLinkedinUrl] = useState("");
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");

  const handleCreateFromLinkedIn = async () => {
    if (!linkedinUrl.trim()) return;
    setCreating(true);
    setError("");
    try {
      const token = localStorage.getItem("token");
      const res = await axios.post(
        `${API_URL}/contact/create-from-linkedin/`,
        { linkedin_url: linkedinUrl },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setShowLinkedIn(false);
      setLinkedinUrl("");
      navigate(`/contact/${res.data.contact.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Enrichment failed");
    }
    setCreating(false);
  };

  return (
    <Layout>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "28px" }}>
        <div>
          <h1 style={{ marginTop: 0, fontSize: "28px", fontWeight: "700", color: "#1a1a2e", letterSpacing: "-0.5px", marginBottom: "6px" }}>Contacts</h1>
          <p style={{ fontSize: "15px", color: "#6b7280" }}>Manage your contacts and track lead scores</p>
        </div>
        <button
          onClick={() => setShowLinkedIn(!showLinkedIn)}
          style={{
            padding: "10px 20px", borderRadius: "10px", border: "none",
            background: "linear-gradient(135deg, #0a66c2, #0077b5)", color: "white",
            cursor: "pointer", fontWeight: "600", fontSize: "13px", fontFamily: "inherit",
            display: "flex", alignItems: "center", gap: "8px",
            boxShadow: "0 4px 12px rgba(10,102,194,0.25)", transition: "all 150ms ease",
          }}
          onMouseEnter={(e) => { e.currentTarget.style.transform = "translateY(-1px)"; }}
          onMouseLeave={(e) => { e.currentTarget.style.transform = "translateY(0)"; }}
        >
          + New from LinkedIn
        </button>
      </div>

      {showLinkedIn && (
        <div style={{
          background: "white", borderRadius: "14px", padding: "20px", marginBottom: "20px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.06)", border: "1px solid rgba(0,0,0,0.04)",
          animation: "fadeIn 0.25s ease-out",
        }}>
          <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
            <input
              type="text" value={linkedinUrl} onChange={(e) => setLinkedinUrl(e.target.value)}
              placeholder="https://linkedin.com/in/john-doe"
              style={{
                flex: 1, padding: "11px 14px", borderRadius: "10px", border: "1.5px solid #e5e7eb",
                fontSize: "14px", fontFamily: "inherit", outline: "none", transition: "border-color 150ms, box-shadow 150ms",
              }}
              onFocus={(e) => { e.target.style.borderColor = "#0a66c2"; e.target.style.boxShadow = "0 0 0 3px rgba(10,102,194,0.1)"; }}
              onBlur={(e) => { e.target.style.borderColor = "#e5e7eb"; e.target.style.boxShadow = "none"; }}
            />
            <button onClick={handleCreateFromLinkedIn} disabled={creating} style={{
              padding: "11px 22px", borderRadius: "10px", border: "none",
              background: "linear-gradient(135deg, #0a66c2, #0077b5)", color: "white",
              cursor: creating ? "not-allowed" : "pointer", fontWeight: "600", fontFamily: "inherit",
              whiteSpace: "nowrap", fontSize: "13px", opacity: creating ? 0.7 : 1,
            }}>
              {creating ? "Creating..." : "Create Contact"}
            </button>
            <button onClick={() => { setShowLinkedIn(false); setError(""); }} style={{
              padding: "11px 16px", borderRadius: "10px", border: "1.5px solid #e5e7eb",
              background: "white", cursor: "pointer", color: "#6b7280", fontFamily: "inherit", fontSize: "13px",
            }}>
              Cancel
            </button>
          </div>
          {error && <p style={{ color: "#ef4444", margin: "10px 0 0", fontSize: "13px", fontWeight: "500" }}>{error}</p>}
        </div>
      )}

      <p style={{ color: "#9ca3af", fontSize: "13px", marginBottom: "16px" }}>Click a contact row to view details</p>

      <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
        <TableBlock id="table-contact-0" onRowClick={(row: any) => navigate(`/contact/${row.id}`)} styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Contacts" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "First Name", "column_type": "field", "field": "first_name", "type": "str", "required": true}, {"label": "Last Name", "column_type": "field", "field": "last_name", "type": "str", "required": true}, {"label": "Email", "column_type": "field", "field": "email", "type": "str", "required": true}, {"label": "Job Title", "column_type": "field", "field": "job_title", "type": "str", "required": true}, {"label": "Company", "column_type": "lookup", "path": "company", "entity": "Company", "field": "name", "type": "str", "required": false}, {"label": "Phone", "column_type": "field", "field": "phone", "type": "str", "required": true}, {"label": "Lead Score", "column_type": "field", "field": "lead_score", "type": "int", "required": true}, {"label": "Lead Score Level", "column_type": "field", "field": "lead_score_level", "type": "enum", "options": ["COLD", "HOT", "WARM"], "required": true}, {"label": "Is Enriched", "column_type": "field", "field": "is_enriched", "type": "bool", "required": true}, {"label": "Tags", "column_type": "lookup", "path": "tags", "entity": "Tag", "field": "name", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "updated_at", "label": "updated_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "phone", "label": "phone", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "lead_score_level", "label": "lead_score_level", "type": "enum", "required": true, "defaultValue": "COLD", "options": ["COLD", "HOT", "WARM"]}, {"column_type": "field", "field": "email", "label": "email", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "lead_score", "label": "lead_score", "type": "int", "required": true, "defaultValue": 0}, {"column_type": "field", "field": "last_name", "label": "last_name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "profile_picture_url", "label": "profile_picture_url", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "first_name", "label": "first_name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "created_at", "label": "created_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "linkedin_url", "label": "linkedin_url", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "notes", "label": "notes", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "job_title", "label": "job_title", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "is_enriched", "label": "is_enriched", "type": "bool", "required": true, "defaultValue": false}, {"column_type": "lookup", "path": "company", "field": "company", "lookup_field": "website", "entity": "Company", "type": "str", "required": false}, {"column_type": "lookup", "path": "enrichment_logs", "field": "enrichment_logs", "lookup_field": "id", "entity": "EnrichmentLog", "type": "list", "required": false}, {"column_type": "lookup", "path": "created_by", "field": "created_by", "lookup_field": "last_name", "entity": "User", "type": "str", "required": true}, {"column_type": "lookup", "path": "opportunities", "field": "opportunities", "lookup_field": "expected_close_date", "entity": "Opportunity", "type": "list", "required": false}, {"column_type": "lookup", "path": "generated_emails", "field": "generated_emails", "lookup_field": "created_at", "entity": "GeneratedEmail", "type": "list", "required": false}, {"column_type": "lookup", "path": "tags", "field": "tags", "lookup_field": "name", "entity": "Tag", "type": "list", "required": false}, {"column_type": "lookup", "path": "interactions", "field": "interactions", "lookup_field": "created_at", "entity": "Interaction", "type": "list", "required": false}, {"column_type": "lookup", "path": "tasks", "field": "tasks", "lookup_field": "description", "entity": "Task", "type": "list", "required": false}, {"column_type": "lookup", "path": "score_history", "field": "score_history", "lookup_field": "id", "entity": "ScoreHistory", "type": "list", "required": false}]}} dataBinding={{"entity": "Contact", "endpoint": "/contact/"}} />
      </div>
    </Layout>
  );
};

export default Contact;
