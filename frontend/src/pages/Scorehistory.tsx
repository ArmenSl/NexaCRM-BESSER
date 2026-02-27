import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import Layout from "../components/Layout";

const Scorehistory: React.FC = () => {
  return (
    <Layout>
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ marginTop: 0, fontSize: "28px", fontWeight: "700", color: "#1a1a2e", letterSpacing: "-0.5px", marginBottom: "6px" }}>Score History</h1>
        <p style={{ fontSize: "15px", color: "#6b7280" }}>Lead score change tracking</p>
      </div>
      <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
      <TableBlock id="table-scorehistory-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Score History" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "Old Score", "column_type": "field", "field": "old_score", "type": "int", "required": true}, {"label": "New Score", "column_type": "field", "field": "new_score", "type": "int", "required": true}, {"label": "Reason", "column_type": "field", "field": "reason", "type": "str", "required": true}, {"label": "Calculated At", "column_type": "field", "field": "calculated_at", "type": "datetime", "required": true}, {"label": "Contact", "column_type": "lookup", "path": "contact", "entity": "Contact", "field": "last_name", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "calculated_at", "label": "calculated_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "reason", "label": "reason", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "new_score", "label": "new_score", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "old_score", "label": "old_score", "type": "int", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "contact", "field": "contact", "lookup_field": "updated_at", "entity": "Contact", "type": "str", "required": true}]}} dataBinding={{"entity": "ScoreHistory", "endpoint": "/scorehistory/"}} />
      </div>
    </Layout>
  );
};

export default Scorehistory;
