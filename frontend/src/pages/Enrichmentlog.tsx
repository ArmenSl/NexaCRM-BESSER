import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import Layout from "../components/Layout";

const Enrichmentlog: React.FC = () => {
  return (
    <Layout>
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ marginTop: 0, fontSize: "28px", fontWeight: "700", color: "#1a1a2e", letterSpacing: "-0.5px", marginBottom: "6px" }}>Enrichment Logs</h1>
        <p style={{ fontSize: "15px", color: "#6b7280" }}>LinkedIn data enrichment history</p>
      </div>
      <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
      <TableBlock id="table-enrichmentlog-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Enrichment Logs" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "LinkedIn URL", "column_type": "field", "field": "linkedin_url", "type": "str", "required": true}, {"label": "Is Successful", "column_type": "field", "field": "is_successful", "type": "bool", "required": true}, {"label": "Error Message", "column_type": "field", "field": "error_message", "type": "str", "required": true}, {"label": "Enriched At", "column_type": "field", "field": "enriched_at", "type": "datetime", "required": true}, {"label": "Contact", "column_type": "lookup", "path": "contact", "entity": "Contact", "field": "last_name", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "error_message", "label": "error_message", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "is_successful", "label": "is_successful", "type": "bool", "required": true, "defaultValue": null}, {"column_type": "field", "field": "linkedin_url", "label": "linkedin_url", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "enriched_at", "label": "enriched_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "contact", "field": "contact", "lookup_field": "updated_at", "entity": "Contact", "type": "str", "required": true}]}} dataBinding={{"entity": "EnrichmentLog", "endpoint": "/enrichmentlog/"}} />
      </div>
    </Layout>
  );
};

export default Enrichmentlog;
