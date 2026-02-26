import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Emailtemplate: React.FC = () => {
  return (
    <div id="810c8802">
    <div id="i3k2nj" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ig6rer" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i94ilk" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"NexaCRM"}</h2>
        <div id="ilfp2d" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="i5cxwc" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/">{"Dashboard"}</a>
          <a id="i823ne" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/contact">{"Contacts"}</a>
          <a id="iooubr" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/company">{"Companies"}</a>
          <a id="ix84to" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/opportunity">{"Pipeline"}</a>
          <a id="iem6ly" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/task">{"Tasks"}</a>
          <a id="i6jxbh" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/emailtemplate">{"Email Templates"}</a>
        </div>
        <p id="itydui" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 NexaCRM. All rights reserved."}</p>
      </nav>
      <main id="izv06q" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="izy1hi" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Email Templates"}</h1>
        <p id="ivorkt" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Reusable email templates for outreach"}</p>
        <TableBlock id="table-emailtemplate-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Email Templates" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "Name", "column_type": "field", "field": "name", "type": "str", "required": true}, {"label": "Category", "column_type": "field", "field": "category", "type": "str", "required": true}, {"label": "Subject Template", "column_type": "field", "field": "subject_template", "type": "str", "required": true}, {"label": "Body Template", "column_type": "field", "field": "body_template", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "created_at", "label": "created_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "category", "label": "category", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "body_template", "label": "body_template", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "subject_template", "label": "subject_template", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "name", "label": "name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "created_by", "field": "created_by", "lookup_field": "last_name", "entity": "User", "type": "str", "required": true}, {"column_type": "lookup", "path": "generated_emails", "field": "generated_emails", "lookup_field": "created_at", "entity": "GeneratedEmail", "type": "list", "required": false}]}} dataBinding={{"entity": "EmailTemplate", "endpoint": "/emailtemplate/"}} />
      </main>
    </div>    </div>
  );
};

export default Emailtemplate;
