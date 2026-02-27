import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import Layout from "../components/Layout";
import InteractionTimeline from "../components/InteractionTimeline";
import AddInteractionModal from "../components/AddInteractionModal";
import EmailGenerationModal from "../components/EmailGenerationModal";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const scoreLevelColors: Record<string, string> = {
  HOT: "#e74c3c",
  WARM: "#e67e22",
  COLD: "#3498db",
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

  useEffect(() => {
    fetchContact();
  }, [id]);

  const handleRecalculateScore = async () => {
    setActionLoading("score");
    try {
      await axios.post(`${API_URL}/contact/${id}/recalculate-score/`);
      await fetchContact();
    } catch {}
    setActionLoading("");
  };

  const handleEnrich = async () => {
    if (!enrichUrl.trim()) return;
    setActionLoading("enrich");
    try {
      await axios.post(`${API_URL}/contact/${id}/enrich/`, { linkedin_url: enrichUrl });
      setShowEnrichInput(false);
      await fetchContact();
    } catch {}
    setActionLoading("");
  };

  if (loading) {
    return <Layout><p>Loading...</p></Layout>;
  }

  if (!contact) {
    return <Layout><p>Contact not found.</p></Layout>;
  }

  const level = contact.lead_score_level?.replace?.(/^.*\./, "") || contact.lead_score_level || "COLD";
  const levelColor = scoreLevelColors[level] || "#999";

  return (
    <Layout>
      <button onClick={() => navigate("/contact")} style={{ background: "none", border: "none", color: "#5a3d91", cursor: "pointer", fontSize: "14px", marginBottom: "20px", padding: 0 }}>
        &larr; Back to Contacts
      </button>

      {/* Contact Info Card */}
      <div style={{ background: "white", borderRadius: "12px", padding: "24px", marginBottom: "24px", boxShadow: "0 2px 8px rgba(0,0,0,0.06)" }}>
        <div style={{ display: "flex", alignItems: "flex-start", gap: "20px" }}>
          {contact.profile_picture_url ? (
            <img src={contact.profile_picture_url} alt="" style={{ width: "80px", height: "80px", borderRadius: "50%", objectFit: "cover" }} />
          ) : (
            <div style={{ width: "80px", height: "80px", borderRadius: "50%", background: "#5a3d91", display: "flex", alignItems: "center", justifyContent: "center", color: "white", fontSize: "28px", fontWeight: "bold" }}>
              {contact.first_name?.[0]}{contact.last_name?.[0]}
            </div>
          )}
          <div style={{ flex: 1 }}>
            <h1 style={{ margin: "0 0 4px 0", fontSize: "26px", color: "#333" }}>{contact.first_name} {contact.last_name}</h1>
            <p style={{ margin: "0 0 4px 0", color: "#666" }}>{contact.job_title || "No title"}{contact.company ? ` at ${contact.company.name}` : ""}</p>
            <div style={{ display: "flex", gap: "15px", marginTop: "8px", flexWrap: "wrap" }}>
              {contact.email && <span style={{ fontSize: "14px", color: "#555" }}>{contact.email}</span>}
              {contact.phone && <span style={{ fontSize: "14px", color: "#555" }}>{contact.phone}</span>}
              {contact.linkedin_url && <a href={contact.linkedin_url} target="_blank" rel="noopener noreferrer" style={{ fontSize: "14px", color: "#0077b5" }}>LinkedIn</a>}
            </div>
          </div>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: "36px", fontWeight: "bold", color: levelColor }}>{contact.lead_score}</div>
            <span style={{ background: levelColor, color: "white", padding: "3px 12px", borderRadius: "12px", fontSize: "12px", fontWeight: "bold" }}>{level}</span>
            {contact.is_enriched && <div style={{ marginTop: "6px", fontSize: "11px", color: "#27ae60" }}>Enriched</div>}
          </div>
        </div>
        {/* Tags */}
        {contact.tags && contact.tags.length > 0 && (
          <div style={{ marginTop: "12px", display: "flex", gap: "6px", flexWrap: "wrap" }}>
            {contact.tags.map((t: any) => (
              <span key={t.id} style={{ background: t.color || "#5a3d91", color: "white", padding: "2px 10px", borderRadius: "10px", fontSize: "12px" }}>{t.name}</span>
            ))}
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "24px", flexWrap: "wrap" }}>
        <button onClick={() => setShowEnrichInput(!showEnrichInput)} style={{ padding: "8px 16px", borderRadius: "6px", border: "1px solid #0077b5", background: "white", color: "#0077b5", cursor: "pointer", fontWeight: "bold" }}>
          Enrich
        </button>
        <button onClick={() => setShowEmailModal(true)} style={{ padding: "8px 16px", borderRadius: "6px", border: "1px solid #27ae60", background: "white", color: "#27ae60", cursor: "pointer", fontWeight: "bold" }}>
          Generate Email
        </button>
        <button onClick={handleRecalculateScore} disabled={actionLoading === "score"} style={{ padding: "8px 16px", borderRadius: "6px", border: "1px solid #e67e22", background: "white", color: "#e67e22", cursor: "pointer", fontWeight: "bold", opacity: actionLoading === "score" ? 0.6 : 1 }}>
          {actionLoading === "score" ? "Calculating..." : "Recalculate Score"}
        </button>
        <button onClick={() => setShowAddInteraction(true)} style={{ padding: "8px 16px", borderRadius: "6px", border: "none", background: "#5a3d91", color: "white", cursor: "pointer", fontWeight: "bold" }}>
          + Add Interaction
        </button>
      </div>

      {/* Enrich Input */}
      {showEnrichInput && (
        <div style={{ background: "white", borderRadius: "8px", padding: "16px", marginBottom: "20px", display: "flex", gap: "10px", alignItems: "center" }}>
          <input type="text" value={enrichUrl} onChange={(e) => setEnrichUrl(e.target.value)} placeholder="LinkedIn profile URL" style={{ flex: 1, padding: "8px", borderRadius: "6px", border: "1px solid #ddd" }} />
          <button onClick={handleEnrich} disabled={actionLoading === "enrich"} style={{ padding: "8px 16px", borderRadius: "6px", border: "none", background: "#0077b5", color: "white", cursor: "pointer" }}>
            {actionLoading === "enrich" ? "Enriching..." : "Enrich"}
          </button>
        </div>
      )}

      {/* Two-column layout */}
      <div style={{ display: "flex", gap: "24px" }}>
        {/* Left: Timeline */}
        <div style={{ flex: 2 }}>
          <h2 style={{ fontSize: "20px", color: "#333", marginBottom: "16px" }}>Interaction Timeline</h2>
          <InteractionTimeline interactions={contact.interactions || []} />
        </div>

        {/* Right: Side panels */}
        <div style={{ flex: 1 }}>
          {/* Opportunities */}
          {contact.opportunities && contact.opportunities.length > 0 && (
            <div style={{ background: "white", borderRadius: "8px", padding: "16px", marginBottom: "16px" }}>
              <h3 style={{ margin: "0 0 10px 0", fontSize: "16px", color: "#333" }}>Opportunities</h3>
              {contact.opportunities.map((o: any) => (
                <div key={o.id} style={{ padding: "8px 0", borderBottom: "1px solid #f0f0f0" }}>
                  <div style={{ fontWeight: "bold", fontSize: "14px" }}>{o.title}</div>
                  <div style={{ fontSize: "12px", color: "#666" }}>
                    {o.stage} {o.value ? `- $${Number(o.value).toLocaleString()}` : ""}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Score History */}
          {contact.score_history && contact.score_history.length > 0 && (
            <div style={{ background: "white", borderRadius: "8px", padding: "16px", marginBottom: "16px" }}>
              <h3 style={{ margin: "0 0 10px 0", fontSize: "16px", color: "#333" }}>Score History</h3>
              {contact.score_history.slice(0, 5).map((s: any) => (
                <div key={s.id} style={{ padding: "6px 0", borderBottom: "1px solid #f0f0f0", fontSize: "13px" }}>
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span>{s.old_score} &rarr; {s.new_score}</span>
                    <span style={{ color: "#999" }}>{new Date(s.calculated_at).toLocaleDateString()}</span>
                  </div>
                  <div style={{ color: "#888", fontSize: "12px" }}>{s.reason}</div>
                </div>
              ))}
            </div>
          )}

          {/* Generated Emails */}
          {contact.generated_emails && contact.generated_emails.length > 0 && (
            <div style={{ background: "white", borderRadius: "8px", padding: "16px", marginBottom: "16px" }}>
              <h3 style={{ margin: "0 0 10px 0", fontSize: "16px", color: "#333" }}>Generated Emails</h3>
              {contact.generated_emails.slice(0, 5).map((e: any) => (
                <div key={e.id} style={{ padding: "6px 0", borderBottom: "1px solid #f0f0f0", fontSize: "13px" }}>
                  <div style={{ fontWeight: "bold" }}>{e.subject}</div>
                  <div style={{ color: "#999", fontSize: "12px" }}>{new Date(e.created_at).toLocaleDateString()}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Modals */}
      {showAddInteraction && (
        <AddInteractionModal contactId={Number(id)} onClose={() => setShowAddInteraction(false)} onSaved={fetchContact} />
      )}
      {showEmailModal && (
        <EmailGenerationModal contactId={Number(id)} onClose={() => setShowEmailModal(false)} onSaved={fetchContact} />
      )}
    </Layout>
  );
};

export default ContactDetail;
