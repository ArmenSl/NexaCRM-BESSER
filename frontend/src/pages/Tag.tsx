import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import Layout from "../components/Layout";

const Tag: React.FC = () => {
  return (
    <Layout>
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ marginTop: 0, fontSize: "28px", fontWeight: "700", color: "#1a1a2e", letterSpacing: "-0.5px", marginBottom: "6px" }}>Tags</h1>
        <p style={{ fontSize: "15px", color: "#6b7280" }}>Organize contacts and companies with tags</p>
      </div>
      <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
      <TableBlock id="table-tag-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Tags" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "Name", "column_type": "field", "field": "name", "type": "str", "required": true}, {"label": "Color", "column_type": "field", "field": "color", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "name", "label": "name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "color", "label": "color", "type": "str", "required": true, "defaultValue": "#3B82F6"}, {"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "tagged_contacts", "field": "tagged_contacts", "lookup_field": "updated_at", "entity": "Contact", "type": "list", "required": false}, {"column_type": "lookup", "path": "tagged_companies", "field": "tagged_companies", "lookup_field": "website", "entity": "Company", "type": "list", "required": false}]}} dataBinding={{"entity": "Tag", "endpoint": "/tag/"}} />
      </div>
    </Layout>
  );
};

export default Tag;
