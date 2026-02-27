import React from "react";
import { ChartBlock } from "../components/runtime/ChartBlock";
import { TableBlock } from "../components/runtime/TableBlock";
import { MetricCardBlock } from "../components/runtime/MetricCardBlock";
import Layout from "../components/Layout";

const Dashboard: React.FC = () => {
  return (
    <Layout>
      <div style={{ marginBottom: "32px" }}>
        <h1 style={{ marginTop: 0, fontSize: "28px", fontWeight: "700", color: "#1a1a2e", letterSpacing: "-0.5px", marginBottom: "6px" }}>Dashboard</h1>
        <p style={{ fontSize: "15px", color: "#6b7280" }}>Welcome to NexaCRM — your sales command center</p>
      </div>

      {/* Metric Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "16px", marginBottom: "28px" }}>
        <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
          <MetricCardBlock id="izumy7" metric={{ metricTitle: "Total Contacts", format: "number", valueColor: "#6c5ce7", valueSize: 32, showTrend: true, positiveColor: "#10b981", negativeColor: "#ef4444", value: 0, trend: 12 }} dataBinding={{ entity: "Contact", endpoint: "/contact/", data_field: "id" }} />
        </div>
        <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
          <MetricCardBlock id="ihkdqo" metric={{ metricTitle: "Total Companies", format: "number", valueColor: "#10b981", valueSize: 32, showTrend: true, positiveColor: "#10b981", negativeColor: "#ef4444", value: 0, trend: 12 }} dataBinding={{ entity: "Company", endpoint: "/company/", data_field: "id" }} />
        </div>
        <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
          <MetricCardBlock id="iu6u9h" metric={{ metricTitle: "Pipeline Value", format: "currency", valueColor: "#f59e0b", valueSize: 32, showTrend: true, positiveColor: "#10b981", negativeColor: "#ef4444", value: 0, trend: 12 }} dataBinding={{ entity: "Opportunity", endpoint: "/opportunity/", data_field: "value" }} />
        </div>
        <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
          <MetricCardBlock id="i9ub79" metric={{ metricTitle: "Pending Tasks", format: "number", valueColor: "#ef4444", valueSize: 32, showTrend: true, positiveColor: "#10b981", negativeColor: "#ef4444", value: 0, trend: 12 }} dataBinding={{ entity: "Task", endpoint: "/task/", data_field: "id" }} />
        </div>
      </div>

      {/* Chart */}
      <div style={{ background: "white", borderRadius: "14px", padding: "20px", marginBottom: "28px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
        <ChartBlock id="icmcnw" styles={{ width: "auto", height: "auto", padding: "0", margin: "0", position: "static", textAlign: "left", zIndex: 0, "--chart-bar-color": "#6c5ce7", "--chart-color-palette": "default" }} chartType="bar-chart" title="Opportunities by Stage" color="#6c5ce7" chart={{ barWidth: 30, orientation: "vertical", showGrid: true, showLegend: true, showTooltip: true, stacked: false, animate: true, legendPosition: "top", gridColor: "#e5e7eb", barGap: 4 }} series={[{ name: "Series_1", label: "Series 1", color: "#6c5ce7", dataSource: "opportunity", endpoint: "/opportunity/", labelField: "stage", dataField: "value" }]} />
      </div>

      {/* Recent Contacts Table */}
      <div style={{ background: "white", borderRadius: "14px", padding: "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
        <TableBlock id="table-dashboard-recent" styles={{ width: "100%", minHeight: "300px" }} title="Recent Contacts" options={{ showHeader: true, stripedRows: false, showPagination: true, rowsPerPage: 5, actionButtons: true, columns: [{ label: "First Name", column_type: "field", field: "first_name", type: "str", required: true }, { label: "Last Name", column_type: "field", field: "last_name", type: "str", required: true }, { label: "Email", column_type: "field", field: "email", type: "str", required: true }, { label: "Company", column_type: "lookup", path: "company", entity: "Company", field: "name", type: "str", required: false }, { label: "Lead Score", column_type: "field", field: "lead_score", type: "int", required: true }], formColumns: [{ column_type: "field", field: "updated_at", label: "updated_at", type: "datetime", required: true, defaultValue: null }, { column_type: "field", field: "phone", label: "phone", type: "str", required: false, defaultValue: null }, { column_type: "field", field: "lead_score_level", label: "lead_score_level", type: "enum", required: true, defaultValue: "COLD", options: ["COLD", "HOT", "WARM"] }, { column_type: "field", field: "email", label: "email", type: "str", required: false, defaultValue: null }, { column_type: "field", field: "lead_score", label: "lead_score", type: "int", required: true, defaultValue: 0 }, { column_type: "field", field: "last_name", label: "last_name", type: "str", required: true, defaultValue: null }, { column_type: "field", field: "profile_picture_url", label: "profile_picture_url", type: "str", required: false, defaultValue: null }, { column_type: "field", field: "first_name", label: "first_name", type: "str", required: true, defaultValue: null }, { column_type: "field", field: "created_at", label: "created_at", type: "datetime", required: true, defaultValue: null }, { column_type: "field", field: "linkedin_url", label: "linkedin_url", type: "str", required: false, defaultValue: null }, { column_type: "field", field: "id", label: "id", type: "int", required: true, defaultValue: null }, { column_type: "field", field: "notes", label: "notes", type: "str", required: false, defaultValue: null }, { column_type: "field", field: "job_title", label: "job_title", type: "str", required: false, defaultValue: null }, { column_type: "field", field: "is_enriched", label: "is_enriched", type: "bool", required: true, defaultValue: false }, { column_type: "lookup", path: "company", field: "company", lookup_field: "website", entity: "Company", type: "str", required: false }, { column_type: "lookup", path: "enrichment_logs", field: "enrichment_logs", lookup_field: "id", entity: "EnrichmentLog", type: "list", required: false }, { column_type: "lookup", path: "created_by", field: "created_by", lookup_field: "last_name", entity: "User", type: "str", required: true }, { column_type: "lookup", path: "opportunities", field: "opportunities", lookup_field: "expected_close_date", entity: "Opportunity", type: "list", required: false }, { column_type: "lookup", path: "generated_emails", field: "generated_emails", lookup_field: "created_at", entity: "GeneratedEmail", type: "list", required: false }, { column_type: "lookup", path: "tags", field: "tags", lookup_field: "name", entity: "Tag", type: "list", required: false }, { column_type: "lookup", path: "interactions", field: "interactions", lookup_field: "created_at", entity: "Interaction", type: "list", required: false }, { column_type: "lookup", path: "tasks", field: "tasks", lookup_field: "description", entity: "Task", type: "list", required: false }, { column_type: "lookup", path: "score_history", field: "score_history", lookup_field: "id", entity: "ScoreHistory", type: "list", required: false }] }} dataBinding={{ entity: "Contact", endpoint: "/contact/" }} />
      </div>
    </Layout>
  );
};

export default Dashboard;
