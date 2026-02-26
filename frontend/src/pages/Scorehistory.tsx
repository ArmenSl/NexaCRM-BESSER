import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Scorehistory: React.FC = () => {
  return (
    <div id="2e72c9fb">
    <div id="ijga1z" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ippg3z" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i5zwkl" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"NexaCRM"}</h2>
        <div id="iainzr" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="iqz7v6" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/">{"Dashboard"}</a>
          <a id="ii4dt8" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/contact">{"Contacts"}</a>
          <a id="ikktf5" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/company">{"Companies"}</a>
          <a id="iiqqtq" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/opportunity">{"Pipeline"}</a>
          <a id="iiuwmq" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/task">{"Tasks"}</a>
          <a id="i1ms7k" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/emailtemplate">{"Email Templates"}</a>
        </div>
        <p id="ib29ml" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 NexaCRM. All rights reserved."}</p>
      </nav>
      <main id="imn74w" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="i79h56" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Score History"}</h1>
        <p id="ij5ncu" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Lead score change tracking"}</p>
        <TableBlock id="table-scorehistory-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Score History" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "Old Score", "column_type": "field", "field": "old_score", "type": "int", "required": true}, {"label": "New Score", "column_type": "field", "field": "new_score", "type": "int", "required": true}, {"label": "Reason", "column_type": "field", "field": "reason", "type": "str", "required": true}, {"label": "Calculated At", "column_type": "field", "field": "calculated_at", "type": "datetime", "required": true}, {"label": "Contact", "column_type": "lookup", "path": "contact", "entity": "Contact", "field": "last_name", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "calculated_at", "label": "calculated_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "reason", "label": "reason", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "new_score", "label": "new_score", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "old_score", "label": "old_score", "type": "int", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "contact", "field": "contact", "lookup_field": "updated_at", "entity": "Contact", "type": "str", "required": true}]}} dataBinding={{"entity": "ScoreHistory", "endpoint": "/scorehistory/"}} />
      </main>
    </div>    </div>
  );
};

export default Scorehistory;
