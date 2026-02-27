import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import Layout from "../components/Layout";

const Task: React.FC = () => {
  return (
    <Layout>
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ marginTop: 0, fontSize: "28px", fontWeight: "700", color: "#1a1a2e", letterSpacing: "-0.5px", marginBottom: "6px" }}>Tasks</h1>
        <p style={{ fontSize: "15px", color: "#6b7280" }}>Follow-up actions and reminders</p>
      </div>
      <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
      <TableBlock id="table-task-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Tasks" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "Title", "column_type": "field", "field": "title", "type": "str", "required": true}, {"label": "Description", "column_type": "field", "field": "description", "type": "str", "required": true}, {"label": "Due Date", "column_type": "field", "field": "due_date", "type": "datetime", "required": true}, {"label": "Is Completed", "column_type": "field", "field": "is_completed", "type": "bool", "required": true}, {"label": "Assigned To", "column_type": "lookup", "path": "assigned_to", "entity": "User", "field": "last_name", "type": "str", "required": true}, {"label": "Contact", "column_type": "lookup", "path": "contact", "entity": "Contact", "field": "last_name", "type": "str", "required": false}], "formColumns": [{"column_type": "field", "field": "description", "label": "description", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "due_date", "label": "due_date", "type": "datetime", "required": false, "defaultValue": null}, {"column_type": "field", "field": "created_at", "label": "created_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "title", "label": "title", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "completed_at", "label": "completed_at", "type": "datetime", "required": false, "defaultValue": null}, {"column_type": "field", "field": "is_completed", "label": "is_completed", "type": "bool", "required": true, "defaultValue": false}, {"column_type": "lookup", "path": "opportunity", "field": "opportunity", "lookup_field": "expected_close_date", "entity": "Opportunity", "type": "str", "required": false}, {"column_type": "lookup", "path": "contact", "field": "contact", "lookup_field": "updated_at", "entity": "Contact", "type": "str", "required": false}, {"column_type": "lookup", "path": "assigned_to", "field": "assigned_to", "lookup_field": "last_name", "entity": "User", "type": "str", "required": true}]}} dataBinding={{"entity": "Task", "endpoint": "/task/"}} />
      </div>
    </Layout>
  );
};

export default Task;
