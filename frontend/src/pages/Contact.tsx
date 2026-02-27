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
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "10px" }}>
        <div>
          <h1 style={{ marginTop: "0", color: "#333", fontSize: "32px", marginBottom: "10px" }}>{"Contacts"}</h1>
          <p style={{ color: "#666", marginBottom: "0" }}>{"Manage your contacts and track lead scores"}</p>
        </div>
        <button
          onClick={() => setShowLinkedIn(!showLinkedIn)}
          style={{ padding: "10px 20px", borderRadius: "8px", border: "none", background: "#0077b5", color: "white", cursor: "pointer", fontWeight: "bold", fontSize: "14px", display: "flex", alignItems: "center", gap: "6px" }}
        >
          + New from LinkedIn
        </button>
      </div>

      {showLinkedIn && (
        <div style={{ background: "white", borderRadius: "8px", padding: "16px", marginBottom: "20px", boxShadow: "0 1px 4px rgba(0,0,0,0.1)" }}>
          <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
            <input
              type="text"
              value={linkedinUrl}
              onChange={(e) => setLinkedinUrl(e.target.value)}
              placeholder="https://linkedin.com/in/john-doe"
              style={{ flex: 1, padding: "10px", borderRadius: "6px", border: "1px solid #ddd", fontSize: "14px" }}
            />
            <button
              onClick={handleCreateFromLinkedIn}
              disabled={creating}
              style={{ padding: "10px 20px", borderRadius: "6px", border: "none", background: "#0077b5", color: "white", cursor: "pointer", fontWeight: "bold", whiteSpace: "nowrap" }}
            >
              {creating ? "Creating..." : "Create Contact"}
            </button>
            <button
              onClick={() => { setShowLinkedIn(false); setError(""); }}
              style={{ padding: "10px 14px", borderRadius: "6px", border: "1px solid #ddd", background: "white", cursor: "pointer", color: "#666" }}
            >
              Cancel
            </button>
          </div>
          {error && <p style={{ color: "#e74c3c", margin: "8px 0 0", fontSize: "13px" }}>{error}</p>}
        </div>
      )}

      <p style={{ color: "#888", fontSize: "13px", marginBottom: "15px", fontStyle: "italic" }}>{"Click a contact row to view details"}</p>
      <TableBlock id="table-contact-0" onRowClick={(row: any) => navigate(`/contact/${row.id}`)} styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Contacts" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "First Name", "column_type": "field", "field": "first_name", "type": "str", "required": true}, {"label": "Last Name", "column_type": "field", "field": "last_name", "type": "str", "required": true}, {"label": "Email", "column_type": "field", "field": "email", "type": "str", "required": true}, {"label": "Job Title", "column_type": "field", "field": "job_title", "type": "str", "required": true}, {"label": "Company", "column_type": "lookup", "path": "company", "entity": "Company", "field": "name", "type": "str", "required": false}, {"label": "Phone", "column_type": "field", "field": "phone", "type": "str", "required": true}, {"label": "Lead Score", "column_type": "field", "field": "lead_score", "type": "int", "required": true}, {"label": "Lead Score Level", "column_type": "field", "field": "lead_score_level", "type": "enum", "options": ["COLD", "HOT", "WARM"], "required": true}, {"label": "Is Enriched", "column_type": "field", "field": "is_enriched", "type": "bool", "required": true}, {"label": "Tags", "column_type": "lookup", "path": "tags", "entity": "Tag", "field": "name", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "updated_at", "label": "updated_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "phone", "label": "phone", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "lead_score_level", "label": "lead_score_level", "type": "enum", "required": true, "defaultValue": "COLD", "options": ["COLD", "HOT", "WARM"]}, {"column_type": "field", "field": "email", "label": "email", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "lead_score", "label": "lead_score", "type": "int", "required": true, "defaultValue": 0}, {"column_type": "field", "field": "last_name", "label": "last_name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "profile_picture_url", "label": "profile_picture_url", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "first_name", "label": "first_name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "created_at", "label": "created_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "linkedin_url", "label": "linkedin_url", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "notes", "label": "notes", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "job_title", "label": "job_title", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "is_enriched", "label": "is_enriched", "type": "bool", "required": true, "defaultValue": false}, {"column_type": "lookup", "path": "company", "field": "company", "lookup_field": "website", "entity": "Company", "type": "str", "required": false}, {"column_type": "lookup", "path": "enrichment_logs", "field": "enrichment_logs", "lookup_field": "id", "entity": "EnrichmentLog", "type": "list", "required": false}, {"column_type": "lookup", "path": "created_by", "field": "created_by", "lookup_field": "last_name", "entity": "User", "type": "str", "required": true}, {"column_type": "lookup", "path": "opportunities", "field": "opportunities", "lookup_field": "expected_close_date", "entity": "Opportunity", "type": "list", "required": false}, {"column_type": "lookup", "path": "generated_emails", "field": "generated_emails", "lookup_field": "created_at", "entity": "GeneratedEmail", "type": "list", "required": false}, {"column_type": "lookup", "path": "tags", "field": "tags", "lookup_field": "name", "entity": "Tag", "type": "list", "required": false}, {"column_type": "lookup", "path": "interactions", "field": "interactions", "lookup_field": "created_at", "entity": "Interaction", "type": "list", "required": false}, {"column_type": "lookup", "path": "tasks", "field": "tasks", "lookup_field": "description", "entity": "Task", "type": "list", "required": false}, {"column_type": "lookup", "path": "score_history", "field": "score_history", "lookup_field": "id", "entity": "ScoreHistory", "type": "list", "required": false}]}} dataBinding={{"entity": "Contact", "endpoint": "/contact/"}} />
    </Layout>
  );
};

export default Contact;
