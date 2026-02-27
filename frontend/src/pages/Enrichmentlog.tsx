import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import Layout from "../components/Layout";

const Enrichmentlog: React.FC = () => {
  return (
    <Layout>
      <h1 style={{ marginTop: "0", color: "#333", fontSize: "32px", marginBottom: "10px" }}>{"Enrichment Logs"}</h1>
      <p style={{ color: "#666", marginBottom: "30px" }}>{"LinkedIn data enrichment history"}</p>
      <TableBlock id="table-enrichmentlog-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Enrichment Logs" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "LinkedIn URL", "column_type": "field", "field": "linkedin_url", "type": "str", "required": true}, {"label": "Is Successful", "column_type": "field", "field": "is_successful", "type": "bool", "required": true}, {"label": "Error Message", "column_type": "field", "field": "error_message", "type": "str", "required": true}, {"label": "Enriched At", "column_type": "field", "field": "enriched_at", "type": "datetime", "required": true}, {"label": "Contact", "column_type": "lookup", "path": "contact", "entity": "Contact", "field": "last_name", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "error_message", "label": "error_message", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "is_successful", "label": "is_successful", "type": "bool", "required": true, "defaultValue": null}, {"column_type": "field", "field": "linkedin_url", "label": "linkedin_url", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "enriched_at", "label": "enriched_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "contact", "field": "contact", "lookup_field": "updated_at", "entity": "Contact", "type": "str", "required": true}]}} dataBinding={{"entity": "EnrichmentLog", "endpoint": "/enrichmentlog/"}} />
    </Layout>
  );
};

export default Enrichmentlog;
