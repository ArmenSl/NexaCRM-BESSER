import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import Layout from "../components/Layout";

const Emailtemplate: React.FC = () => {
  return (
    <Layout>
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ marginTop: 0, fontSize: "28px", fontWeight: "700", color: "#1a1a2e", letterSpacing: "-0.5px", marginBottom: "6px" }}>Email Templates</h1>
        <p style={{ fontSize: "15px", color: "#6b7280" }}>Reusable email templates for outreach</p>
      </div>
      <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
      <TableBlock id="table-emailtemplate-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Email Templates" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "Name", "column_type": "field", "field": "name", "type": "str", "required": true}, {"label": "Category", "column_type": "field", "field": "category", "type": "str", "required": true}, {"label": "Subject Template", "column_type": "field", "field": "subject_template", "type": "str", "required": true}, {"label": "Body Template", "column_type": "field", "field": "body_template", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "created_at", "label": "created_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "category", "label": "category", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "body_template", "label": "body_template", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "subject_template", "label": "subject_template", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "name", "label": "name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "created_by", "field": "created_by", "lookup_field": "last_name", "entity": "User", "type": "str", "required": true}, {"column_type": "lookup", "path": "generated_emails", "field": "generated_emails", "lookup_field": "created_at", "entity": "GeneratedEmail", "type": "list", "required": false}]}} dataBinding={{"entity": "EmailTemplate", "endpoint": "/emailtemplate/"}} />
      </div>
    </Layout>
  );
};

export default Emailtemplate;
