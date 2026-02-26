import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Generatedemail: React.FC = () => {
  return (
    <div id="a28ec4a4">
    <div id="i96uly" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ilm4b2" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="iq9j4d" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"NexaCRM"}</h2>
        <div id="izm0v4" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="i4svgh" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/">{"Dashboard"}</a>
          <a id="is9p36" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/contact">{"Contacts"}</a>
          <a id="i4z9zy" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/company">{"Companies"}</a>
          <a id="iydkn9" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/opportunity">{"Pipeline"}</a>
          <a id="iqgrpk" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/task">{"Tasks"}</a>
          <a id="i50zuq" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/emailtemplate">{"Email Templates"}</a>
        </div>
        <p id="i9n06b" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 NexaCRM. All rights reserved."}</p>
      </nav>
      <main id="i7bxv3" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="icnmyh" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Generated Emails"}</h1>
        <p id="i87who" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"AI-generated email communications"}</p>
        <TableBlock id="table-generatedemail-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Generated Emails" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "Subject", "column_type": "field", "field": "subject", "type": "str", "required": true}, {"label": "Is Sent", "column_type": "field", "field": "is_sent", "type": "bool", "required": true}, {"label": "Sent At", "column_type": "field", "field": "sent_at", "type": "datetime", "required": true}, {"label": "Contact", "column_type": "lookup", "path": "contact", "entity": "Contact", "field": "last_name", "type": "str", "required": true}, {"label": "Created By", "column_type": "lookup", "path": "created_by", "entity": "User", "field": "last_name", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "created_at", "label": "created_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "sent_at", "label": "sent_at", "type": "datetime", "required": false, "defaultValue": null}, {"column_type": "field", "field": "is_sent", "label": "is_sent", "type": "bool", "required": true, "defaultValue": false}, {"column_type": "field", "field": "body", "label": "body", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "subject", "label": "subject", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "contact", "field": "contact", "lookup_field": "updated_at", "entity": "Contact", "type": "str", "required": true}, {"column_type": "lookup", "path": "template", "field": "template", "lookup_field": "created_at", "entity": "EmailTemplate", "type": "str", "required": false}, {"column_type": "lookup", "path": "created_by", "field": "created_by", "lookup_field": "last_name", "entity": "User", "type": "str", "required": true}]}} dataBinding={{"entity": "GeneratedEmail", "endpoint": "/generatedemail/"}} />
      </main>
    </div>    </div>
  );
};

export default Generatedemail;
