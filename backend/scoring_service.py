from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sql_alchemy import (
    Contact, Interaction, Opportunity, EnrichmentLog, ScoreHistory,
    opportunity_contact, LeadScoreLevel
)


def calculate_lead_score(contact_id: int, db: Session) -> dict:
    """
    Calculate lead score (0-100) based on:
    - Interaction recency (0-25)
    - Interaction count (0-25)
    - Opportunity value (0-25)
    - Enrichment status (0-15)
    - Has email (0-5)
    - Has phone (0-5)
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return {"score": 0, "level": "COLD", "breakdown": {}}

    now = datetime.utcnow()
    breakdown = {}

    # 1. Interaction recency (0-25)
    latest_interaction = (
        db.query(Interaction)
        .filter(Interaction.contact_id == contact_id)
        .order_by(Interaction.occurred_at.desc())
        .first()
    )
    if latest_interaction and latest_interaction.occurred_at:
        days_ago = (now - latest_interaction.occurred_at).days
        if days_ago <= 7:
            breakdown["interaction_recency"] = 25
        elif days_ago <= 30:
            breakdown["interaction_recency"] = 15
        elif days_ago <= 90:
            breakdown["interaction_recency"] = 5
        else:
            breakdown["interaction_recency"] = 0
    else:
        breakdown["interaction_recency"] = 0

    # 2. Interaction count (0-25)
    interaction_count = (
        db.query(Interaction)
        .filter(Interaction.contact_id == contact_id)
        .count()
    )
    if interaction_count >= 10:
        breakdown["interaction_count"] = 25
    elif interaction_count >= 5:
        breakdown["interaction_count"] = 15
    elif interaction_count >= 1:
        breakdown["interaction_count"] = 8
    else:
        breakdown["interaction_count"] = 0

    # 3. Opportunity value (0-25)
    opp_ids = (
        db.query(opportunity_contact.c.opportunities)
        .filter(opportunity_contact.c.contacts == contact_id)
        .all()
    )
    opp_id_list = [x[0] for x in opp_ids]
    weighted_value = 0.0
    if opp_id_list:
        opps = db.query(Opportunity).filter(Opportunity.id.in_(opp_id_list)).all()
        for opp in opps:
            val = opp.value or 0
            prob = opp.probability or 0
            weighted_value += val * (prob / 100.0)

    if weighted_value > 100000:
        breakdown["opportunity_value"] = 25
    elif weighted_value > 50000:
        breakdown["opportunity_value"] = 20
    elif weighted_value > 10000:
        breakdown["opportunity_value"] = 12
    elif weighted_value > 0:
        breakdown["opportunity_value"] = 5
    else:
        breakdown["opportunity_value"] = 0

    # 4. Enrichment status (0-15)
    if contact.is_enriched:
        breakdown["enrichment"] = 15
    elif contact.linkedin_url:
        breakdown["enrichment"] = 5
    else:
        breakdown["enrichment"] = 0

    # 5. Has email (0-5)
    breakdown["has_email"] = 5 if contact.email else 0

    # 6. Has phone (0-5)
    breakdown["has_phone"] = 5 if contact.phone else 0

    score = sum(breakdown.values())
    score = min(score, 100)

    if score >= 70:
        level = "HOT"
    elif score >= 40:
        level = "WARM"
    else:
        level = "COLD"

    return {"score": score, "level": level, "breakdown": breakdown}


def recalculate_and_save(contact_id: int, reason: str, db: Session) -> dict:
    """Calculate score, update Contact, create ScoreHistory entry."""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return {"score": 0, "level": "COLD", "breakdown": {}}

    old_score = contact.lead_score or 0
    result = calculate_lead_score(contact_id, db)

    contact.lead_score = result["score"]
    contact.lead_score_level = LeadScoreLevel(result["level"])
    contact.updated_at = datetime.utcnow()

    # Create ScoreHistory entry
    max_id = db.query(ScoreHistory.id).order_by(ScoreHistory.id.desc()).first()
    new_id = (max_id[0] + 1) if max_id else 1

    history = ScoreHistory(
        id=new_id,
        contact_id=contact_id,
        old_score=old_score,
        new_score=result["score"],
        reason=reason,
        calculated_at=datetime.utcnow(),
    )
    db.add(history)
    db.commit()

    result["old_score"] = old_score
    return result
