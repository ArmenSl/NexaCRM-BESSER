import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Enrichmentlog: React.FC = () => {
  return (
    <div id="d3371a67">
    <div id="icoi1y" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ixoz2l" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="iv8anu" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"NexaCRM"}</h2>
        <div id="iroof9" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="iebt9e" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/">{"Dashboard"}</a>
          <a id="izstpj" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/contact">{"Contacts"}</a>
          <a id="i41huk" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/company">{"Companies"}</a>
          <a id="iml3i2" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/opportunity">{"Pipeline"}</a>
          <a id="iv47ns" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/task">{"Tasks"}</a>
          <a id="iibvig" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/emailtemplate">{"Email Templates"}</a>
        </div>
        <p id="i9snhp" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 NexaCRM. All rights reserved."}</p>
      </nav>
      <main id="i28jad" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="i1i257" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Enrichment Logs"}</h1>
        <p id="igybfl" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"LinkedIn data enrichment history"}</p>
        <TableBlock id="table-enrichmentlog-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Enrichment Logs" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "LinkedIn URL", "column_type": "field", "field": "linkedin_url", "type": "str", "required": true}, {"label": "Is Successful", "column_type": "field", "field": "is_successful", "type": "bool", "required": true}, {"label": "Error Message", "column_type": "field", "field": "error_message", "type": "str", "required": true}, {"label": "Enriched At", "column_type": "field", "field": "enriched_at", "type": "datetime", "required": true}, {"label": "Contact", "column_type": "lookup", "path": "contact", "entity": "Contact", "field": "last_name", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "error_message", "label": "error_message", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "is_successful", "label": "is_successful", "type": "bool", "required": true, "defaultValue": null}, {"column_type": "field", "field": "linkedin_url", "label": "linkedin_url", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "enriched_at", "label": "enriched_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "contact", "field": "contact", "lookup_field": "updated_at", "entity": "Contact", "type": "str", "required": true}]}} dataBinding={{"entity": "EnrichmentLog", "endpoint": "/enrichmentlog/"}} />
      </main>
    </div>    </div>
  );
};

export default Enrichmentlog;
