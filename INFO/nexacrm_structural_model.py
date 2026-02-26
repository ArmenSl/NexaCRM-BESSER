"""
NexaCRM - AI-Powered Intelligent CRM
Complete B-UML Structural Domain Model
"""

from besser.BUML.metamodel.structural import (
    DomainModel, Class, Property, Method, Parameter, Multiplicity,
    BinaryAssociation, Enumeration, EnumerationLiteral, Generalization,
    StringType, IntegerType, FloatType, BooleanType, DateType, DateTimeType
)

# ============================================================================
# ENUMERATIONS
# ============================================================================

# -- User Role --
role_admin = EnumerationLiteral(name="ADMIN")
role_sales = EnumerationLiteral(name="SALES_REP")
role_manager = EnumerationLiteral(name="SALES_MANAGER")

UserRole = Enumeration(name="UserRole", literals={role_admin, role_sales, role_manager})

# -- Lead Score Level --
score_cold = EnumerationLiteral(name="COLD")
score_warm = EnumerationLiteral(name="WARM")
score_hot = EnumerationLiteral(name="HOT")

LeadScoreLevel = Enumeration(name="LeadScoreLevel", literals={score_cold, score_warm, score_hot})

# -- Opportunity Stage --
stage_prospecting = EnumerationLiteral(name="PROSPECTING")
stage_qualification = EnumerationLiteral(name="QUALIFICATION")
stage_proposal = EnumerationLiteral(name="PROPOSAL")
stage_negotiation = EnumerationLiteral(name="NEGOTIATION")
stage_closed_won = EnumerationLiteral(name="CLOSED_WON")
stage_closed_lost = EnumerationLiteral(name="CLOSED_LOST")

OpportunityStage = Enumeration(
    name="OpportunityStage",
    literals={stage_prospecting, stage_qualification, stage_proposal,
              stage_negotiation, stage_closed_won, stage_closed_lost}
)

# -- Interaction Type --
interaction_email = EnumerationLiteral(name="EMAIL")
interaction_call = EnumerationLiteral(name="CALL")
interaction_note = EnumerationLiteral(name="NOTE")
interaction_meeting = EnumerationLiteral(name="MEETING")

InteractionType = Enumeration(
    name="InteractionType",
    literals={interaction_email, interaction_call, interaction_note, interaction_meeting}
)

# -- Interaction Direction (for emails/calls) --
direction_inbound = EnumerationLiteral(name="INBOUND")
direction_outbound = EnumerationLiteral(name="OUTBOUND")

InteractionDirection = Enumeration(
    name="InteractionDirection",
    literals={direction_inbound, direction_outbound}
)

# -- Industry --
ind_tech = EnumerationLiteral(name="TECHNOLOGY")
ind_finance = EnumerationLiteral(name="FINANCE")
ind_healthcare = EnumerationLiteral(name="HEALTHCARE")
ind_manufacturing = EnumerationLiteral(name="MANUFACTURING")
ind_retail = EnumerationLiteral(name="RETAIL")
ind_services = EnumerationLiteral(name="SERVICES")
ind_other = EnumerationLiteral(name="OTHER")

Industry = Enumeration(
    name="Industry",
    literals={ind_tech, ind_finance, ind_healthcare, ind_manufacturing,
              ind_retail, ind_services, ind_other}
)

# -- Company Size --
size_startup = EnumerationLiteral(name="STARTUP")
size_small = EnumerationLiteral(name="SMALL")
size_medium = EnumerationLiteral(name="MEDIUM")
size_large = EnumerationLiteral(name="LARGE")
size_enterprise = EnumerationLiteral(name="ENTERPRISE")

CompanySize = Enumeration(
    name="CompanySize",
    literals={size_startup, size_small, size_medium, size_large, size_enterprise}
)

# ============================================================================
# CLASSES
# ============================================================================

# -- User --
User = Class(
    name="User",
    attributes={
        Property(name="id", type=IntegerType, is_id=True),
        Property(name="email", type=StringType),
        Property(name="password_hash", type=StringType),
        Property(name="first_name", type=StringType),
        Property(name="last_name", type=StringType),
        Property(name="role", type=UserRole),
        Property(name="is_active", type=BooleanType, default_value=True),
        Property(name="created_at", type=DateTimeType),
        Property(name="last_login", type=DateTimeType, is_optional=True),
    }
)

# -- Company --
Company = Class(
    name="Company",
    attributes={
        Property(name="id", type=IntegerType, is_id=True),
        Property(name="name", type=StringType),
        Property(name="industry", type=Industry),
        Property(name="size", type=CompanySize, is_optional=True),
        Property(name="website", type=StringType, is_optional=True),
        Property(name="linkedin_url", type=StringType, is_optional=True),
        Property(name="phone", type=StringType, is_optional=True),
        Property(name="address", type=StringType, is_optional=True),
        Property(name="city", type=StringType, is_optional=True),
        Property(name="country", type=StringType, is_optional=True),
        Property(name="description", type=StringType, is_optional=True),
        Property(name="created_at", type=DateTimeType),
        Property(name="updated_at", type=DateTimeType),
    }
)

# -- Contact --
Contact = Class(
    name="Contact",
    attributes={
        Property(name="id", type=IntegerType, is_id=True),
        Property(name="first_name", type=StringType),
        Property(name="last_name", type=StringType),
        Property(name="email", type=StringType, is_optional=True),
        Property(name="phone", type=StringType, is_optional=True),
        Property(name="job_title", type=StringType, is_optional=True),
        Property(name="linkedin_url", type=StringType, is_optional=True),
        Property(name="profile_picture_url", type=StringType, is_optional=True),
        Property(name="lead_score", type=IntegerType, default_value=0),
        Property(name="lead_score_level", type=LeadScoreLevel, default_value="COLD"),
        Property(name="is_enriched", type=BooleanType, default_value=False),
        Property(name="notes", type=StringType, is_optional=True),
        Property(name="created_at", type=DateTimeType),
        Property(name="updated_at", type=DateTimeType),
    }
)

# -- Opportunity --
Opportunity = Class(
    name="Opportunity",
    attributes={
        Property(name="id", type=IntegerType, is_id=True),
        Property(name="title", type=StringType),
        Property(name="description", type=StringType, is_optional=True),
        Property(name="value", type=FloatType, is_optional=True),
        Property(name="stage", type=OpportunityStage, default_value="PROSPECTING"),
        Property(name="probability", type=IntegerType, is_optional=True),
        Property(name="expected_close_date", type=DateType, is_optional=True),
        Property(name="created_at", type=DateTimeType),
        Property(name="updated_at", type=DateTimeType),
        Property(name="closed_at", type=DateTimeType, is_optional=True),
    }
)

# -- Interaction --
Interaction = Class(
    name="Interaction",
    attributes={
        Property(name="id", type=IntegerType, is_id=True),
        Property(name="type", type=InteractionType),
        Property(name="direction", type=InteractionDirection, is_optional=True),
        Property(name="subject", type=StringType, is_optional=True),
        Property(name="content", type=StringType),
        Property(name="occurred_at", type=DateTimeType),
        Property(name="created_at", type=DateTimeType),
    }
)

# -- Tag (for categorizing contacts/companies) --
Tag = Class(
    name="Tag",
    attributes={
        Property(name="id", type=IntegerType, is_id=True),
        Property(name="name", type=StringType),
        Property(name="color", type=StringType, default_value="#3B82F6"),
    }
)

# -- Task (follow-up actions) --
Task = Class(
    name="Task",
    attributes={
        Property(name="id", type=IntegerType, is_id=True),
        Property(name="title", type=StringType),
        Property(name="description", type=StringType, is_optional=True),
        Property(name="due_date", type=DateTimeType, is_optional=True),
        Property(name="is_completed", type=BooleanType, default_value=False),
        Property(name="completed_at", type=DateTimeType, is_optional=True),
        Property(name="created_at", type=DateTimeType),
    }
)

# -- EmailTemplate (for the writing assistant) --
EmailTemplate = Class(
    name="EmailTemplate",
    attributes={
        Property(name="id", type=IntegerType, is_id=True),
        Property(name="name", type=StringType),
        Property(name="subject_template", type=StringType),
        Property(name="body_template", type=StringType),
        Property(name="category", type=StringType),
        Property(name="created_at", type=DateTimeType),
    }
)

# -- GeneratedEmail (emails produced by the writing assistant) --
GeneratedEmail = Class(
    name="GeneratedEmail",
    attributes={
        Property(name="id", type=IntegerType, is_id=True),
        Property(name="subject", type=StringType),
        Property(name="body", type=StringType),
        Property(name="is_sent", type=BooleanType, default_value=False),
        Property(name="sent_at", type=DateTimeType, is_optional=True),
        Property(name="created_at", type=DateTimeType),
    }
)

# -- EnrichmentLog (track LinkedIn enrichment attempts) --
EnrichmentLog = Class(
    name="EnrichmentLog",
    attributes={
        Property(name="id", type=IntegerType, is_id=True),
        Property(name="linkedin_url", type=StringType),
        Property(name="is_successful", type=BooleanType),
        Property(name="error_message", type=StringType, is_optional=True),
        Property(name="enriched_at", type=DateTimeType),
    }
)

# -- ScoreHistory (track lead score changes over time) --
ScoreHistory = Class(
    name="ScoreHistory",
    attributes={
        Property(name="id", type=IntegerType, is_id=True),
        Property(name="old_score", type=IntegerType),
        Property(name="new_score", type=IntegerType),
        Property(name="reason", type=StringType),
        Property(name="calculated_at", type=DateTimeType),
    }
)

# ============================================================================
# ASSOCIATIONS
# ============================================================================

# -- Contact belongs to Company (N:1) --
contact_company = BinaryAssociation(
    name="contact_company",
    ends={
        Property(name="company", type=Company, multiplicity=Multiplicity(0, 1)),
        Property(name="contacts", type=Contact, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- Opportunity linked to Contact (N:M) --
opportunity_contact = BinaryAssociation(
    name="opportunity_contact",
    ends={
        Property(name="opportunities", type=Opportunity, multiplicity=Multiplicity(0, 9999)),
        Property(name="contacts", type=Contact, multiplicity=Multiplicity(1, 9999)),
    }
)

# -- Opportunity linked to Company (N:1) --
opportunity_company = BinaryAssociation(
    name="opportunity_company",
    ends={
        Property(name="company", type=Company, multiplicity=Multiplicity(0, 1)),
        Property(name="opportunities", type=Opportunity, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- Opportunity assigned to User (N:1) --
opportunity_owner = BinaryAssociation(
    name="opportunity_owner",
    ends={
        Property(name="owner", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="owned_opportunities", type=Opportunity, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- Interaction linked to Contact (N:1, composition) --
interaction_contact = BinaryAssociation(
    name="interaction_contact",
    ends={
        Property(name="contact", type=Contact, multiplicity=Multiplicity(1, 1), is_composite=True),
        Property(name="interactions", type=Interaction, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- Interaction performed by User (N:1) --
interaction_user = BinaryAssociation(
    name="interaction_user",
    ends={
        Property(name="performed_by", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="interactions", type=Interaction, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- Contact tagged (N:M) --
contact_tag = BinaryAssociation(
    name="contact_tag",
    ends={
        Property(name="tagged_contacts", type=Contact, multiplicity=Multiplicity(0, 9999)),
        Property(name="tags", type=Tag, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- Company tagged (N:M) --
company_tag = BinaryAssociation(
    name="company_tag",
    ends={
        Property(name="tagged_companies", type=Company, multiplicity=Multiplicity(0, 9999)),
        Property(name="tags", type=Tag, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- Task assigned to User (N:1) --
task_user = BinaryAssociation(
    name="task_user",
    ends={
        Property(name="assigned_to", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="tasks", type=Task, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- Task linked to Contact (N:1) --
task_contact = BinaryAssociation(
    name="task_contact",
    ends={
        Property(name="contact", type=Contact, multiplicity=Multiplicity(0, 1)),
        Property(name="tasks", type=Task, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- Task linked to Opportunity (N:1) --
task_opportunity = BinaryAssociation(
    name="task_opportunity",
    ends={
        Property(name="opportunity", type=Opportunity, multiplicity=Multiplicity(0, 1)),
        Property(name="tasks", type=Task, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- GeneratedEmail for Contact (N:1) --
email_contact = BinaryAssociation(
    name="email_contact",
    ends={
        Property(name="contact", type=Contact, multiplicity=Multiplicity(1, 1)),
        Property(name="generated_emails", type=GeneratedEmail, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- GeneratedEmail created by User (N:1) --
email_user = BinaryAssociation(
    name="email_user",
    ends={
        Property(name="created_by", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="generated_emails", type=GeneratedEmail, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- GeneratedEmail based on EmailTemplate (N:1, optional) --
email_template_link = BinaryAssociation(
    name="email_template_link",
    ends={
        Property(name="template", type=EmailTemplate, multiplicity=Multiplicity(0, 1)),
        Property(name="generated_emails", type=GeneratedEmail, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- EmailTemplate created by User (N:1) --
template_user = BinaryAssociation(
    name="template_user",
    ends={
        Property(name="created_by", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="email_templates", type=EmailTemplate, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- EnrichmentLog for Contact (N:1) --
enrichment_contact = BinaryAssociation(
    name="enrichment_contact",
    ends={
        Property(name="contact", type=Contact, multiplicity=Multiplicity(1, 1)),
        Property(name="enrichment_logs", type=EnrichmentLog, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- ScoreHistory for Contact (N:1, composition) --
score_contact = BinaryAssociation(
    name="score_contact",
    ends={
        Property(name="contact", type=Contact, multiplicity=Multiplicity(1, 1), is_composite=True),
        Property(name="score_history", type=ScoreHistory, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- Contact created by User (N:1) --
contact_created_by = BinaryAssociation(
    name="contact_created_by",
    ends={
        Property(name="created_by", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="created_contacts", type=Contact, multiplicity=Multiplicity(0, 9999)),
    }
)

# -- Company created by User (N:1) --
company_created_by = BinaryAssociation(
    name="company_created_by",
    ends={
        Property(name="created_by", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="created_companies", type=Company, multiplicity=Multiplicity(0, 9999)),
    }
)

# ============================================================================
# DOMAIN MODEL
# ============================================================================

nexacrm_model = DomainModel(
    name="NexaCRM",
    types={
        # Classes
        User, Company, Contact, Opportunity, Interaction,
        Tag, Task, EmailTemplate, GeneratedEmail,
        EnrichmentLog, ScoreHistory,
        # Enumerations
        UserRole, LeadScoreLevel, OpportunityStage,
        InteractionType, InteractionDirection,
        Industry, CompanySize,
    },
    associations={
        contact_company, opportunity_contact, opportunity_company,
        opportunity_owner, interaction_contact, interaction_user,
        contact_tag, company_tag, task_user, task_contact,
        task_opportunity, email_contact, email_user,
        email_template_link, template_user, enrichment_contact,
        score_contact, contact_created_by, company_created_by,
    },
)

# ============================================================================
# QUICK VERIFICATION
# ============================================================================

if __name__ == "__main__":
    print(f"Model: {nexacrm_model.name}")
    print(f"Classes: {len([t for t in nexacrm_model.types if isinstance(t, Class)])}")
    print(f"Enumerations: {len(nexacrm_model.get_enumerations())}")
    print(f"Associations: {len(nexacrm_model.associations)}")
    print()

    for t in sorted(nexacrm_model.types, key=lambda x: x.name):
        if isinstance(t, Class):
            attrs = sorted(t.attributes, key=lambda a: a.name)
            print(f"  {t.name} ({len(attrs)} attributes)")
            for a in attrs:
                optional = " [optional]" if a.is_optional else ""
                id_mark = " [PK]" if a.is_id else ""
                default = f" = {a.default_value}" if a.default_value is not None else ""
                print(f"    - {a.name}: {a.type.name}{id_mark}{optional}{default}")
            print()

    for t in sorted(nexacrm_model.types, key=lambda x: x.name):
        if isinstance(t, Enumeration):
            lits = sorted(t.literals, key=lambda l: l.name)
            print(f"  <<enum>> {t.name}: {', '.join(l.name for l in lits)}")

    print()
    for a in sorted(nexacrm_model.associations, key=lambda x: x.name):
        ends = sorted(a.ends, key=lambda e: e.name)
        e1, e2 = ends
        print(f"  {a.name}: {e1.type.name}.{e1.name}[{e1.multiplicity.min}..{e1.multiplicity.max}] "
              f"<-> {e2.type.name}.{e2.name}[{e2.multiplicity.min}..{e2.multiplicity.max}]")
