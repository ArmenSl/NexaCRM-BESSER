import React from "react";
import { ChartBlock } from "../components/runtime/ChartBlock";
import { TableBlock } from "../components/runtime/TableBlock";
import { MetricCardBlock } from "../components/runtime/MetricCardBlock";
import Layout from "../components/Layout";

const Dashboard: React.FC = () => {
  return (
    <Layout>
      <h1 style={{ marginTop: "0", color: "#333", fontSize: "32px", marginBottom: "10px" }}>Dashboard</h1>
      <p style={{ color: "#666", marginBottom: "30px" }}>Welcome to NexaCRM — your sales command center</p>
      <div style={{ display: "flex", gap: "20px", marginBottom: "30px", flexWrap: "wrap" }}>
        <div style={{ flex: "1", minWidth: "200px" }}>
          <MetricCardBlock id="izumy7" metric={{ metricTitle: "Total Contacts", format: "number", valueColor: "#3498db", valueSize: 32, showTrend: true, positiveColor: "#27ae60", negativeColor: "#e74c3c", value: 0, trend: 12 }} dataBinding={{ entity: "Contact", endpoint: "/contact/", data_field: "id" }} />
        </div>
        <div style={{ flex: "1", minWidth: "200px" }}>
          <MetricCardBlock id="ihkdqo" metric={{ metricTitle: "Total Companies", format: "number", valueColor: "#27ae60", valueSize: 32, showTrend: true, positiveColor: "#27ae60", negativeColor: "#e74c3c", value: 0, trend: 12 }} dataBinding={{ entity: "Company", endpoint: "/company/", data_field: "id" }} />
        </div>
        <div style={{ flex: "1", minWidth: "200px" }}>
          <MetricCardBlock id="iu6u9h" metric={{ metricTitle: "Open Opportunities", format: "currency", valueColor: "#e67e22", valueSize: 32, showTrend: true, positiveColor: "#27ae60", negativeColor: "#e74c3c", value: 0, trend: 12 }} dataBinding={{ entity: "Opportunity", endpoint: "/opportunity/", data_field: "value" }} />
        </div>
        <div style={{ flex: "1", minWidth: "200px" }}>
          <MetricCardBlock id="i9ub79" metric={{ metricTitle: "Pending Tasks", format: "number", valueColor: "#e74c3c", valueSize: 32, showTrend: true, positiveColor: "#27ae60", negativeColor: "#e74c3c", value: 0, trend: 12 }} dataBinding={{ entity: "Task", endpoint: "/task/", data_field: "id" }} />
        </div>
      </div>
      <div style={{ display: "flex", gap: "20px", marginBottom: "30px" }}>
        <div style={{ flex: "1" }}>
          <ChartBlock id="icmcnw" styles={{ width: "auto", height: "auto", padding: "0", margin: "0", position: "static", textAlign: "left", zIndex: 0, "--chart-bar-color": "#5a3d91", "--chart-color-palette": "default" }} chartType="bar-chart" title="Opportunities by Stage" color="#5a3d91" chart={{ barWidth: 30, orientation: "vertical", showGrid: true, showLegend: true, showTooltip: true, stacked: false, animate: true, legendPosition: "top", gridColor: "#e0e0e0", barGap: 4 }} series={[{ name: "Series_1", label: "Series 1", color: "#5a3d91", dataSource: "opportunity", endpoint: "/opportunity/", labelField: "stage", dataField: "value" }]} />
        </div>
      </div>
      <TableBlock id="table-dashboard-recent" styles={{ width: "100%", minHeight: "300px" }} title="Recent Contacts" options={{ showHeader: true, stripedRows: false, showPagination: true, rowsPerPage: 5, actionButtons: true, columns: [{ label: "First Name", column_type: "field", field: "first_name", type: "str", required: true }, { label: "Last Name", column_type: "field", field: "last_name", type: "str", required: true }, { label: "Email", column_type: "field", field: "email", type: "str", required: true }, { label: "Company", column_type: "lookup", path: "company", entity: "Company", field: "name", type: "str", required: false }, { label: "Lead Score", column_type: "field", field: "lead_score", type: "int", required: true }], formColumns: [{ column_type: "field", field: "updated_at", label: "updated_at", type: "datetime", required: true, defaultValue: null }, { column_type: "field", field: "phone", label: "phone", type: "str", required: false, defaultValue: null }, { column_type: "field", field: "lead_score_level", label: "lead_score_level", type: "enum", required: true, defaultValue: "COLD", options: ["COLD", "HOT", "WARM"] }, { column_type: "field", field: "email", label: "email", type: "str", required: false, defaultValue: null }, { column_type: "field", field: "lead_score", label: "lead_score", type: "int", required: true, defaultValue: 0 }, { column_type: "field", field: "last_name", label: "last_name", type: "str", required: true, defaultValue: null }, { column_type: "field", field: "profile_picture_url", label: "profile_picture_url", type: "str", required: false, defaultValue: null }, { column_type: "field", field: "first_name", label: "first_name", type: "str", required: true, defaultValue: null }, { column_type: "field", field: "created_at", label: "created_at", type: "datetime", required: true, defaultValue: null }, { column_type: "field", field: "linkedin_url", label: "linkedin_url", type: "str", required: false, defaultValue: null }, { column_type: "field", field: "id", label: "id", type: "int", required: true, defaultValue: null }, { column_type: "field", field: "notes", label: "notes", type: "str", required: false, defaultValue: null }, { column_type: "field", field: "job_title", label: "job_title", type: "str", required: false, defaultValue: null }, { column_type: "field", field: "is_enriched", label: "is_enriched", type: "bool", required: true, defaultValue: false }, { column_type: "lookup", path: "company", field: "company", lookup_field: "website", entity: "Company", type: "str", required: false }, { column_type: "lookup", path: "enrichment_logs", field: "enrichment_logs", lookup_field: "id", entity: "EnrichmentLog", type: "list", required: false }, { column_type: "lookup", path: "created_by", field: "created_by", lookup_field: "last_name", entity: "User", type: "str", required: true }, { column_type: "lookup", path: "opportunities", field: "opportunities", lookup_field: "expected_close_date", entity: "Opportunity", type: "list", required: false }, { column_type: "lookup", path: "generated_emails", field: "generated_emails", lookup_field: "created_at", entity: "GeneratedEmail", type: "list", required: false }, { column_type: "lookup", path: "tags", field: "tags", lookup_field: "name", entity: "Tag", type: "list", required: false }, { column_type: "lookup", path: "interactions", field: "interactions", lookup_field: "created_at", entity: "Interaction", type: "list", required: false }, { column_type: "lookup", path: "tasks", field: "tasks", lookup_field: "description", entity: "Task", type: "list", required: false }, { column_type: "lookup", path: "score_history", field: "score_history", lookup_field: "id", entity: "ScoreHistory", type: "list", required: false }] }} dataBinding={{ entity: "Contact", endpoint: "/contact/" }} />
    </Layout>
  );
};

export default Dashboard;
