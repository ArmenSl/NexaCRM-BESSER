import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import Layout from "../components/Layout";
import PipelineFilters from "../components/PipelineFilters";
import PipelineSummary from "../components/PipelineSummary";

const Opportunity: React.FC = () => {
  return (
    <Layout>
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ marginTop: 0, fontSize: "28px", fontWeight: "700", color: "#1a1a2e", letterSpacing: "-0.5px", marginBottom: "6px" }}>Sales Pipeline</h1>
        <p style={{ fontSize: "15px", color: "#6b7280" }}>Track deals and manage your sales pipeline</p>
      </div>
      <PipelineSummary />
      <PipelineFilters onFilterChange={() => {}} />
      <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
        <TableBlock id="table-opportunity-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Sales Pipeline" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "Title", "column_type": "field", "field": "title", "type": "str", "required": true}, {"label": "Value", "column_type": "field", "field": "value", "type": "float", "required": true}, {"label": "Stage", "column_type": "field", "field": "stage", "type": "enum", "options": ["CLOSED_LOST", "CLOSED_WON", "NEGOTIATION", "PROPOSAL", "PROSPECTING", "QUALIFICATION"], "required": true}, {"label": "Probability", "column_type": "field", "field": "probability", "type": "int", "required": true}, {"label": "Expected Close Date", "column_type": "field", "field": "expected_close_date", "type": "date", "required": true}, {"label": "Owner", "column_type": "lookup", "path": "owner", "entity": "User", "field": "last_name", "type": "str", "required": true}, {"label": "Company", "column_type": "lookup", "path": "company", "entity": "Company", "field": "name", "type": "str", "required": false}, {"label": "Contacts", "column_type": "lookup", "path": "contacts", "entity": "Contact", "field": "last_name", "type": "list", "required": true}], "formColumns": [{"column_type": "field", "field": "expected_close_date", "label": "expected_close_date", "type": "date", "required": false, "defaultValue": null}, {"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "probability", "label": "probability", "type": "int", "required": false, "defaultValue": null}, {"column_type": "field", "field": "value", "label": "value", "type": "float", "required": false, "defaultValue": null}, {"column_type": "field", "field": "closed_at", "label": "closed_at", "type": "datetime", "required": false, "defaultValue": null}, {"column_type": "field", "field": "stage", "label": "stage", "type": "enum", "required": true, "defaultValue": "PROSPECTING", "options": ["CLOSED_LOST", "CLOSED_WON", "NEGOTIATION", "PROPOSAL", "PROSPECTING", "QUALIFICATION"]}, {"column_type": "field", "field": "updated_at", "label": "updated_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "description", "label": "description", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "created_at", "label": "created_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "title", "label": "title", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "tasks", "field": "tasks", "lookup_field": "description", "entity": "Task", "type": "list", "required": false}, {"column_type": "lookup", "path": "contacts", "field": "contacts", "lookup_field": "updated_at", "entity": "Contact", "type": "list", "required": true}, {"column_type": "lookup", "path": "owner", "field": "owner", "lookup_field": "last_name", "entity": "User", "type": "str", "required": true}, {"column_type": "lookup", "path": "company", "field": "company", "lookup_field": "website", "entity": "Company", "type": "str", "required": false}]}} dataBinding={{"entity": "Opportunity", "endpoint": "/opportunity/"}} />
      </div>
    </Layout>
  );
};

export default Opportunity;
