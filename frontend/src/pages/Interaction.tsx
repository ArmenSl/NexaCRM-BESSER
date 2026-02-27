import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import Layout from "../components/Layout";

const Interaction: React.FC = () => {
  return (
    <Layout>
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ marginTop: 0, fontSize: "28px", fontWeight: "700", color: "#1a1a2e", letterSpacing: "-0.5px", marginBottom: "6px" }}>Interactions</h1>
        <p style={{ fontSize: "15px", color: "#6b7280" }}>Communication history with contacts</p>
      </div>
      <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
      <TableBlock id="table-interaction-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Interactions" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "Type", "column_type": "field", "field": "type", "type": "enum", "options": ["CALL", "EMAIL", "MEETING", "NOTE"], "required": true}, {"label": "Direction", "column_type": "field", "field": "direction", "type": "enum", "options": ["INBOUND", "OUTBOUND"], "required": true}, {"label": "Subject", "column_type": "field", "field": "subject", "type": "str", "required": true}, {"label": "Content", "column_type": "field", "field": "content", "type": "str", "required": true}, {"label": "Occurred At", "column_type": "field", "field": "occurred_at", "type": "datetime", "required": true}, {"label": "Contact", "column_type": "lookup", "path": "contact", "entity": "Contact", "field": "last_name", "type": "str", "required": true}, {"label": "Performed By", "column_type": "lookup", "path": "performed_by", "entity": "User", "field": "last_name", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "created_at", "label": "created_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "subject", "label": "subject", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "type", "label": "type", "type": "enum", "required": true, "defaultValue": null, "options": ["CALL", "EMAIL", "MEETING", "NOTE"]}, {"column_type": "field", "field": "content", "label": "content", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "occurred_at", "label": "occurred_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "direction", "label": "direction", "type": "enum", "required": false, "defaultValue": null, "options": ["INBOUND", "OUTBOUND"]}, {"column_type": "lookup", "path": "contact", "field": "contact", "lookup_field": "updated_at", "entity": "Contact", "type": "str", "required": true}, {"column_type": "lookup", "path": "performed_by", "field": "performed_by", "lookup_field": "last_name", "entity": "User", "type": "str", "required": true}]}} dataBinding={{"entity": "Interaction", "endpoint": "/interaction/"}} />
      </div>
    </Layout>
  );
};

export default Interaction;
