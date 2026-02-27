import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import Layout from "../components/Layout";

const Generatedemail: React.FC = () => {
  return (
    <Layout>
      <h1 style={{ marginTop: "0", color: "#333", fontSize: "32px", marginBottom: "10px" }}>{"Generated Emails"}</h1>
      <p style={{ color: "#666", marginBottom: "30px" }}>{"AI-generated email communications"}</p>
      <TableBlock id="table-generatedemail-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Generated Emails" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "Subject", "column_type": "field", "field": "subject", "type": "str", "required": true}, {"label": "Is Sent", "column_type": "field", "field": "is_sent", "type": "bool", "required": true}, {"label": "Sent At", "column_type": "field", "field": "sent_at", "type": "datetime", "required": true}, {"label": "Contact", "column_type": "lookup", "path": "contact", "entity": "Contact", "field": "last_name", "type": "str", "required": true}, {"label": "Created By", "column_type": "lookup", "path": "created_by", "entity": "User", "field": "last_name", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "created_at", "label": "created_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "sent_at", "label": "sent_at", "type": "datetime", "required": false, "defaultValue": null}, {"column_type": "field", "field": "is_sent", "label": "is_sent", "type": "bool", "required": true, "defaultValue": false}, {"column_type": "field", "field": "body", "label": "body", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "subject", "label": "subject", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "contact", "field": "contact", "lookup_field": "updated_at", "entity": "Contact", "type": "str", "required": true}, {"column_type": "lookup", "path": "template", "field": "template", "lookup_field": "created_at", "entity": "EmailTemplate", "type": "str", "required": false}, {"column_type": "lookup", "path": "created_by", "field": "created_by", "lookup_field": "last_name", "entity": "User", "type": "str", "required": true}]}} dataBinding={{"entity": "GeneratedEmail", "endpoint": "/generatedemail/"}} />
    </Layout>
  );
};

export default Generatedemail;
