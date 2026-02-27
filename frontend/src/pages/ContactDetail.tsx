import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import Layout from "../components/Layout";
import InteractionTimeline from "../components/InteractionTimeline";
import AddInteractionModal from "../components/AddInteractionModal";
import EmailGenerationModal from "../components/EmailGenerationModal";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const scoreLevelConfig: Record<string, { color: string; bg: string }> = {
  HOT: { color: "#dc2626", bg: "#fef2f2" },
  WARM: { color: "#d97706", bg: "#fffbeb" },
  COLD: { color: "#2563eb", bg: "#eff6ff" },
};

const ContactDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [contact, setContact] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [showAddInteraction, setShowAddInteraction] = useState(false);
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [enrichUrl, setEnrichUrl] = useState("");
  const [showEnrichInput, setShowEnrichInput] = useState(false);
  const [actionLoading, setActionLoading] = useState("");

  const fetchContact = async () => {
    try {
      const res = await axios.get(`${API_URL}/contact/${id}/detail/`);
      setContact(res.data);
      setEnrichUrl(res.data.linkedin_url || "");
    } catch {
      navigate("/contact");
    }
    setLoading(false);
  };

  useEffect(() => { fetchContact(); }, [id]);

  const handleRecalculateScore = async () => {
    setActionLoading("score");
    try { await axios.post(`${API_URL}/contact/${id}/recalculate-score/`); await fetchContact(); } catch {}
    setActionLoading("");
  };

  const handleEnrich = async () => {
    if (!enrichUrl.trim()) return;
    setActionLoading("enrich");
    try { await axios.post(`${API_URL}/contact/${id}/enrich/`, { linkedin_url: enrichUrl }); setShowEnrichInput(false); await fetchContact(); } catch {}
    setActionLoading("");
  };

  if (loading) return <Layout><div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "50vh", color: "#9ca3af" }}>Loading...</div></Layout>;
  if (!contact) return <Layout><div style={{ textAlign: "center", padding: "60px", color: "#6b7280" }}>Contact not found.</div></Layout>;

  const level = contact.lead_score_level?.replace?.(/^.*\./, "") || contact.lead_score_level || "COLD";
  const cfg = scoreLevelConfig[level] || { color: "#6b7280", bg: "#f3f4f6" };

  const btnStyle = (border: string, color: string): React.CSSProperties => ({
    padding: "9px 18px", borderRadius: "10px", border: `1.5px solid ${border}`, background: "white",
    color, cursor: "pointer", fontWeight: "600", fontSize: "13px", fontFamily: "inherit",
    transition: "all 150ms ease",
  });

  return (
    <Layout>
      {/* Back button */}
      <button onClick={() => navigate("/contact")} style={{
        background: "none", border: "none", color: "#6c5ce7", cursor: "pointer",
        fontSize: "13px", marginBottom: "20px", padding: 0, fontWeight: "600", fontFamily: "inherit",
        display: "flex", alignItems: "center", gap: "4px",
      }}>
        &#8592; Back to Contacts
      </button>

      {/* Contact Info Card */}
      <div style={{
        background: "white", borderRadius: "16px", padding: "28px", marginBottom: "24px",
        boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)",
      }}>
        <div style={{ display: "flex", alignItems: "flex-start", gap: "20px" }}>
          {contact.profile_picture_url ? (
            <img src={contact.profile_picture_url} alt="" style={{ width: "72px", height: "72px", borderRadius: "16px", objectFit: "cover" }} />
          ) : (
            <div style={{
              width: "72px", height: "72px", borderRadius: "16px",
              background: "linear-gradient(135deg, #6c5ce7, #a29bfe)",
              display: "flex", alignItems: "center", justifyContent: "center",
              color: "white", fontSize: "24px", fontWeight: "700", flexShrink: 0,
            }}>
              {contact.first_name?.[0]}{contact.last_name?.[0]}
            </div>
          )}
          <div style={{ flex: 1 }}>
            <h1 style={{ margin: "0 0 4px 0", fontSize: "24px", fontWeight: "700", color: "#1a1a2e", letterSpacing: "-0.5px" }}>
              {contact.first_name} {contact.last_name}
            </h1>
            <p style={{ margin: "0 0 8px 0", color: "#6b7280", fontSize: "15px" }}>
              {contact.job_title || "No title"}{contact.company ? ` at ${contact.company.name}` : ""}
            </p>
            <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
              {contact.email && <span style={{ fontSize: "13px", color: "#6b7280" }}>{contact.email}</span>}
              {contact.phone && <span style={{ fontSize: "13px", color: "#6b7280" }}>{contact.phone}</span>}
              {contact.linkedin_url && <a href={contact.linkedin_url} target="_blank" rel="noopener noreferrer" style={{ fontSize: "13px", color: "#0a66c2", fontWeight: "500", textDecoration: "none" }}>LinkedIn</a>}
            </div>
          </div>

          {/* Score badge */}
          <div style={{ textAlign: "center", padding: "12px 20px", background: cfg.bg, borderRadius: "14px", minWidth: "80px" }}>
            <div style={{ fontSize: "32px", fontWeight: "800", color: cfg.color, lineHeight: 1 }}>{contact.lead_score}</div>
            <span style={{ background: cfg.color, color: "white", padding: "3px 12px", borderRadius: "20px", fontSize: "11px", fontWeight: "700", display: "inline-block", marginTop: "6px" }}>{level}</span>
            {contact.is_enriched && <div style={{ marginTop: "6px", fontSize: "11px", color: "#10b981", fontWeight: "600" }}>Enriched</div>}
          </div>
        </div>

        {/* Tags */}
        {contact.tags && contact.tags.length > 0 && (
          <div style={{ marginTop: "16px", display: "flex", gap: "6px", flexWrap: "wrap" }}>
            {contact.tags.map((t: any) => (
              <span key={t.id} style={{ background: t.color || "#6c5ce7", color: "white", padding: "3px 12px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>{t.name}</span>
            ))}
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "24px", flexWrap: "wrap" }}>
        <button onClick={() => setShowEnrichInput(!showEnrichInput)} style={btnStyle("#0a66c2", "#0a66c2")}>Enrich</button>
        <button onClick={() => setShowEmailModal(true)} style={btnStyle("#10b981", "#10b981")}>Generate Email</button>
        <button onClick={handleRecalculateScore} disabled={actionLoading === "score"} style={{ ...btnStyle("#f59e0b", "#d97706"), opacity: actionLoading === "score" ? 0.6 : 1 }}>
          {actionLoading === "score" ? "Calculating..." : "Recalculate Score"}
        </button>
        <button onClick={() => setShowAddInteraction(true)} style={{
          padding: "9px 18px", borderRadius: "10px", border: "none",
          background: "linear-gradient(135deg, #6c5ce7, #5a4bd1)", color: "white",
          cursor: "pointer", fontWeight: "600", fontSize: "13px", fontFamily: "inherit",
          boxShadow: "0 4px 12px rgba(108,92,231,0.25)",
        }}>
          + Add Interaction
        </button>
      </div>

      {/* Enrich Input */}
      {showEnrichInput && (
        <div style={{
          background: "white", borderRadius: "14px", padding: "16px", marginBottom: "20px",
          display: "flex", gap: "10px", alignItems: "center",
          boxShadow: "0 4px 12px rgba(0,0,0,0.06)", border: "1px solid rgba(0,0,0,0.04)",
          animation: "fadeIn 0.25s ease-out",
        }}>
          <input type="text" value={enrichUrl} onChange={(e) => setEnrichUrl(e.target.value)} placeholder="LinkedIn profile URL"
            style={{ flex: 1, padding: "10px 14px", borderRadius: "10px", border: "1.5px solid #e5e7eb", fontSize: "14px", fontFamily: "inherit", outline: "none" }}
            onFocus={(e) => { e.target.style.borderColor = "#0a66c2"; }}
            onBlur={(e) => { e.target.style.borderColor = "#e5e7eb"; }}
          />
          <button onClick={handleEnrich} disabled={actionLoading === "enrich"} style={{
            padding: "10px 20px", borderRadius: "10px", border: "none",
            background: "#0a66c2", color: "white", cursor: "pointer", fontWeight: "600", fontFamily: "inherit", fontSize: "13px",
          }}>
            {actionLoading === "enrich" ? "Enriching..." : "Enrich"}
          </button>
        </div>
      )}

      {/* Two-column layout */}
      <div style={{ display: "flex", gap: "24px" }}>
        <div style={{ flex: 2 }}>
          <h2 style={{ fontSize: "18px", fontWeight: "700", color: "#1a1a2e", marginBottom: "16px" }}>Interaction Timeline</h2>
          <InteractionTimeline interactions={contact.interactions || []} />
        </div>

        <div style={{ flex: 1 }}>
          {contact.opportunities && contact.opportunities.length > 0 && (
            <div style={{ background: "white", borderRadius: "14px", padding: "20px", marginBottom: "16px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
              <h3 style={{ margin: "0 0 12px 0", fontSize: "15px", fontWeight: "700", color: "#1a1a2e" }}>Opportunities</h3>
              {contact.opportunities.map((o: any) => (
                <div key={o.id} style={{ padding: "10px 0", borderBottom: "1px solid #f3f4f6" }}>
                  <div style={{ fontWeight: "600", fontSize: "14px", color: "#1a1a2e" }}>{o.title}</div>
                  <div style={{ fontSize: "12px", color: "#6b7280", marginTop: "2px" }}>
                    {o.stage} {o.value ? `- $${Number(o.value).toLocaleString()}` : ""}
                  </div>
                </div>
              ))}
            </div>
          )}

          {contact.score_history && contact.score_history.length > 0 && (
            <div style={{ background: "white", borderRadius: "14px", padding: "20px", marginBottom: "16px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
              <h3 style={{ margin: "0 0 12px 0", fontSize: "15px", fontWeight: "700", color: "#1a1a2e" }}>Score History</h3>
              {contact.score_history.slice(0, 5).map((s: any) => (
                <div key={s.id} style={{ padding: "8px 0", borderBottom: "1px solid #f3f4f6", fontSize: "13px" }}>
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span style={{ fontWeight: "600" }}>{s.old_score} &rarr; {s.new_score}</span>
                    <span style={{ color: "#9ca3af", fontSize: "12px" }}>{new Date(s.calculated_at).toLocaleDateString()}</span>
                  </div>
                  <div style={{ color: "#6b7280", fontSize: "12px", marginTop: "2px" }}>{s.reason}</div>
                </div>
              ))}
            </div>
          )}

          {contact.generated_emails && contact.generated_emails.length > 0 && (
            <div style={{ background: "white", borderRadius: "14px", padding: "20px", marginBottom: "16px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.04)" }}>
              <h3 style={{ margin: "0 0 12px 0", fontSize: "15px", fontWeight: "700", color: "#1a1a2e" }}>Generated Emails</h3>
              {contact.generated_emails.slice(0, 5).map((e: any) => (
                <div key={e.id} style={{ padding: "8px 0", borderBottom: "1px solid #f3f4f6", fontSize: "13px" }}>
                  <div style={{ fontWeight: "600", color: "#1a1a2e" }}>{e.subject}</div>
                  <div style={{ color: "#9ca3af", fontSize: "12px", marginTop: "2px" }}>{new Date(e.created_at).toLocaleDateString()}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {showAddInteraction && <AddInteractionModal contactId={Number(id)} onClose={() => setShowAddInteraction(false)} onSaved={fetchContact} />}
      {showEmailModal && <EmailGenerationModal contactId={Number(id)} onClose={() => setShowEmailModal(false)} onSaved={fetchContact} />}
    </Layout>
  );
};

export default ContactDetail;
