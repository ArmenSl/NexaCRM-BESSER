import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Task: React.FC = () => {
  return (
    <div id="4f806ae4">
    <div id="ijw7t5" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="i9t69q" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="is8muc" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"NexaCRM"}</h2>
        <div id="ip00jk" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="id2vy8" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/">{"Dashboard"}</a>
          <a id="ij0e2w" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/contact">{"Contacts"}</a>
          <a id="isrg7t" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/company">{"Companies"}</a>
          <a id="iw2itc" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/opportunity">{"Pipeline"}</a>
          <a id="iow1dl" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/task">{"Tasks"}</a>
          <a id="inv8yq" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/emailtemplate">{"Email Templates"}</a>
        </div>
        <p id="il1kvj" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 NexaCRM. All rights reserved."}</p>
      </nav>
      <main id="i4lft3" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="iw3q9e" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Tasks"}</h1>
        <p id="i173v9" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Follow-up actions and reminders"}</p>
        <TableBlock id="table-task-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Tasks" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 10, "actionButtons": true, "columns": [{"label": "Title", "column_type": "field", "field": "title", "type": "str", "required": true}, {"label": "Description", "column_type": "field", "field": "description", "type": "str", "required": true}, {"label": "Due Date", "column_type": "field", "field": "due_date", "type": "datetime", "required": true}, {"label": "Is Completed", "column_type": "field", "field": "is_completed", "type": "bool", "required": true}, {"label": "Assigned To", "column_type": "lookup", "path": "assigned_to", "entity": "User", "field": "last_name", "type": "str", "required": true}, {"label": "Contact", "column_type": "lookup", "path": "contact", "entity": "Contact", "field": "last_name", "type": "str", "required": false}], "formColumns": [{"column_type": "field", "field": "description", "label": "description", "type": "str", "required": false, "defaultValue": null}, {"column_type": "field", "field": "due_date", "label": "due_date", "type": "datetime", "required": false, "defaultValue": null}, {"column_type": "field", "field": "created_at", "label": "created_at", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "title", "label": "title", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "id", "label": "id", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "completed_at", "label": "completed_at", "type": "datetime", "required": false, "defaultValue": null}, {"column_type": "field", "field": "is_completed", "label": "is_completed", "type": "bool", "required": true, "defaultValue": false}, {"column_type": "lookup", "path": "opportunity", "field": "opportunity", "lookup_field": "expected_close_date", "entity": "Opportunity", "type": "str", "required": false}, {"column_type": "lookup", "path": "contact", "field": "contact", "lookup_field": "updated_at", "entity": "Contact", "type": "str", "required": false}, {"column_type": "lookup", "path": "assigned_to", "field": "assigned_to", "lookup_field": "last_name", "entity": "User", "type": "str", "required": true}]}} dataBinding={{"entity": "Task", "endpoint": "/task/"}} />
      </main>
    </div>    </div>
  );
};

export default Task;
