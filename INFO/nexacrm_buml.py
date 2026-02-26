####################
# STRUCTURAL MODEL #
####################

from besser.BUML.metamodel.structural import (
    Class, Property, Method, Parameter,
    BinaryAssociation, Generalization, DomainModel,
    Enumeration, EnumerationLiteral, Multiplicity,
    StringType, IntegerType, FloatType, BooleanType,
    TimeType, DateType, DateTimeType, TimeDeltaType,
    AnyType, Constraint, AssociationClass, Metadata, MethodImplementationType
)

# Enumerations
UserRole: Enumeration = Enumeration(
    name="UserRole",
    literals={
            EnumerationLiteral(name="SALES_MANAGER"),
			EnumerationLiteral(name="ADMIN"),
			EnumerationLiteral(name="SALES_REP")
    }
)

LeadScoreLevel: Enumeration = Enumeration(
    name="LeadScoreLevel",
    literals={
            EnumerationLiteral(name="COLD"),
			EnumerationLiteral(name="WARM"),
			EnumerationLiteral(name="HOT")
    }
)

OpportunityStage: Enumeration = Enumeration(
    name="OpportunityStage",
    literals={
            EnumerationLiteral(name="PROSPECTING"),
			EnumerationLiteral(name="QUALIFICATION"),
			EnumerationLiteral(name="PROPOSAL"),
			EnumerationLiteral(name="NEGOTIATION"),
			EnumerationLiteral(name="CLOSED_WON"),
			EnumerationLiteral(name="CLOSED_LOST")
    }
)

InteractionType: Enumeration = Enumeration(
    name="InteractionType",
    literals={
            EnumerationLiteral(name="EMAIL"),
			EnumerationLiteral(name="CALL"),
			EnumerationLiteral(name="NOTE"),
			EnumerationLiteral(name="MEETING")
    }
)

InteractionDirection: Enumeration = Enumeration(
    name="InteractionDirection",
    literals={
            EnumerationLiteral(name="INBOUND"),
			EnumerationLiteral(name="OUTBOUND")
    }
)

Industry: Enumeration = Enumeration(
    name="Industry",
    literals={
            EnumerationLiteral(name="TECHNOLOGY"),
			EnumerationLiteral(name="FINANCE"),
			EnumerationLiteral(name="HEALTHCARE"),
			EnumerationLiteral(name="MANUFACTURING"),
			EnumerationLiteral(name="RETAIL"),
			EnumerationLiteral(name="SERVICES"),
			EnumerationLiteral(name="OTHER")
    }
)

CompanySize: Enumeration = Enumeration(
    name="CompanySize",
    literals={
            EnumerationLiteral(name="STARTUP"),
			EnumerationLiteral(name="SMALL"),
			EnumerationLiteral(name="MEDIUM"),
			EnumerationLiteral(name="LARGE"),
			EnumerationLiteral(name="ENTERPRISE")
    }
)

# Classes
User = Class(name="User")
Company = Class(name="Company")
Contact = Class(name="Contact")
Opportunity = Class(name="Opportunity")
Interaction = Class(name="Interaction")
Tag = Class(name="Tag")
Task = Class(name="Task")
EmailTemplate = Class(name="EmailTemplate")
GeneratedEmail = Class(name="GeneratedEmail")
EnrichmentLog = Class(name="EnrichmentLog")
ScoreHistory = Class(name="ScoreHistory")

# User class attributes and methods
User_id: Property = Property(name="id", type=IntegerType)
User_email: Property = Property(name="email", type=StringType)
User_password_hash: Property = Property(name="password_hash", type=StringType)
User_first_name: Property = Property(name="first_name", type=StringType)
User_last_name: Property = Property(name="last_name", type=StringType)
User_role: Property = Property(name="role", type=UserRole)
User_is_active: Property = Property(name="is_active", type=BooleanType, default_value=True)
User_created_at: Property = Property(name="created_at", type=DateTimeType)
User_last_login: Property = Property(name="last_login", type=DateTimeType, is_optional=True)
User.attributes={User_first_name, User_email, User_last_name, User_role, User_id, User_is_active, User_password_hash, User_created_at, User_last_login}

# Company class attributes and methods
Company_id: Property = Property(name="id", type=IntegerType)
Company_name: Property = Property(name="name", type=StringType)
Company_industry: Property = Property(name="industry", type=Industry)
Company_size: Property = Property(name="size", type=CompanySize, is_optional=True)
Company_website: Property = Property(name="website", type=StringType, is_optional=True)
Company_linkedin_url: Property = Property(name="linkedin_url", type=StringType, is_optional=True)
Company_phone: Property = Property(name="phone", type=StringType, is_optional=True)
Company_address: Property = Property(name="address", type=StringType, is_optional=True)
Company_city: Property = Property(name="city", type=StringType, is_optional=True)
Company_country: Property = Property(name="country", type=StringType, is_optional=True)
Company_description: Property = Property(name="description", type=StringType, is_optional=True)
Company_created_at: Property = Property(name="created_at", type=DateTimeType)
Company_updated_at: Property = Property(name="updated_at", type=DateTimeType)
Company.attributes={Company_description, Company_linkedin_url, Company_created_at, Company_phone, Company_website, Company_address, Company_id, Company_name, Company_city, Company_size, Company_country, Company_industry, Company_updated_at}

# Contact class attributes and methods
Contact_id: Property = Property(name="id", type=IntegerType)
Contact_first_name: Property = Property(name="first_name", type=StringType)
Contact_last_name: Property = Property(name="last_name", type=StringType)
Contact_email: Property = Property(name="email", type=StringType, is_optional=True)
Contact_phone: Property = Property(name="phone", type=StringType, is_optional=True)
Contact_job_title: Property = Property(name="job_title", type=StringType, is_optional=True)
Contact_linkedin_url: Property = Property(name="linkedin_url", type=StringType, is_optional=True)
Contact_profile_picture_url: Property = Property(name="profile_picture_url", type=StringType, is_optional=True)
Contact_lead_score: Property = Property(name="lead_score", type=IntegerType, default_value=0)
Contact_lead_score_level: Property = Property(name="lead_score_level", type=LeadScoreLevel, default_value="COLD")
Contact_is_enriched: Property = Property(name="is_enriched", type=BooleanType, default_value=False)
Contact_notes: Property = Property(name="notes", type=StringType, is_optional=True)
Contact_created_at: Property = Property(name="created_at", type=DateTimeType)
Contact_updated_at: Property = Property(name="updated_at", type=DateTimeType)
Contact.attributes={Contact_created_at, Contact_last_name, Contact_profile_picture_url, Contact_phone, Contact_lead_score, Contact_first_name, Contact_email, Contact_lead_score_level, Contact_updated_at, Contact_is_enriched, Contact_job_title, Contact_notes, Contact_id, Contact_linkedin_url}

# Opportunity class attributes and methods
Opportunity_id: Property = Property(name="id", type=IntegerType)
Opportunity_title: Property = Property(name="title", type=StringType)
Opportunity_description: Property = Property(name="description", type=StringType, is_optional=True)
Opportunity_value: Property = Property(name="value", type=FloatType, is_optional=True)
Opportunity_stage: Property = Property(name="stage", type=OpportunityStage, default_value="PROSPECTING")
Opportunity_probability: Property = Property(name="probability", type=IntegerType, is_optional=True)
Opportunity_expected_close_date: Property = Property(name="expected_close_date", type=DateType, is_optional=True)
Opportunity_created_at: Property = Property(name="created_at", type=DateTimeType)
Opportunity_updated_at: Property = Property(name="updated_at", type=DateTimeType)
Opportunity_closed_at: Property = Property(name="closed_at", type=DateTimeType, is_optional=True)
Opportunity.attributes={Opportunity_title, Opportunity_updated_at, Opportunity_stage, Opportunity_closed_at, Opportunity_probability, Opportunity_id, Opportunity_expected_close_date, Opportunity_description, Opportunity_created_at, Opportunity_value}

# Interaction class attributes and methods
Interaction_id: Property = Property(name="id", type=IntegerType)
Interaction_type: Property = Property(name="type", type=InteractionType)
Interaction_direction: Property = Property(name="direction", type=InteractionDirection, is_optional=True)
Interaction_subject: Property = Property(name="subject", type=StringType, is_optional=True)
Interaction_content: Property = Property(name="content", type=StringType)
Interaction_occurred_at: Property = Property(name="occurred_at", type=DateTimeType)
Interaction_created_at: Property = Property(name="created_at", type=DateTimeType)
Interaction.attributes={Interaction_subject, Interaction_occurred_at, Interaction_content, Interaction_id, Interaction_type, Interaction_created_at, Interaction_direction}

# Tag class attributes and methods
Tag_id: Property = Property(name="id", type=IntegerType)
Tag_name: Property = Property(name="name", type=StringType)
Tag_color: Property = Property(name="color", type=StringType, default_value="#3B82F6")
Tag.attributes={Tag_name, Tag_color, Tag_id}

# Task class attributes and methods
Task_id: Property = Property(name="id", type=IntegerType)
Task_title: Property = Property(name="title", type=StringType)
Task_description: Property = Property(name="description", type=StringType, is_optional=True)
Task_due_date: Property = Property(name="due_date", type=DateTimeType, is_optional=True)
Task_is_completed: Property = Property(name="is_completed", type=BooleanType, default_value=False)
Task_completed_at: Property = Property(name="completed_at", type=DateTimeType, is_optional=True)
Task_created_at: Property = Property(name="created_at", type=DateTimeType)
Task.attributes={Task_created_at, Task_description, Task_due_date, Task_is_completed, Task_id, Task_completed_at, Task_title}

# EmailTemplate class attributes and methods
EmailTemplate_id: Property = Property(name="id", type=IntegerType)
EmailTemplate_name: Property = Property(name="name", type=StringType)
EmailTemplate_subject_template: Property = Property(name="subject_template", type=StringType)
EmailTemplate_body_template: Property = Property(name="body_template", type=StringType)
EmailTemplate_category: Property = Property(name="category", type=StringType)
EmailTemplate_created_at: Property = Property(name="created_at", type=DateTimeType)
EmailTemplate.attributes={EmailTemplate_body_template, EmailTemplate_name, EmailTemplate_category, EmailTemplate_created_at, EmailTemplate_id, EmailTemplate_subject_template}

# GeneratedEmail class attributes and methods
GeneratedEmail_id: Property = Property(name="id", type=IntegerType)
GeneratedEmail_subject: Property = Property(name="subject", type=StringType)
GeneratedEmail_body: Property = Property(name="body", type=StringType)
GeneratedEmail_is_sent: Property = Property(name="is_sent", type=BooleanType, default_value=False)
GeneratedEmail_sent_at: Property = Property(name="sent_at", type=DateTimeType, is_optional=True)
GeneratedEmail_created_at: Property = Property(name="created_at", type=DateTimeType)
GeneratedEmail.attributes={GeneratedEmail_sent_at, GeneratedEmail_is_sent, GeneratedEmail_created_at, GeneratedEmail_subject, GeneratedEmail_id, GeneratedEmail_body}

# EnrichmentLog class attributes and methods
EnrichmentLog_id: Property = Property(name="id", type=IntegerType)
EnrichmentLog_linkedin_url: Property = Property(name="linkedin_url", type=StringType)
EnrichmentLog_is_successful: Property = Property(name="is_successful", type=BooleanType)
EnrichmentLog_error_message: Property = Property(name="error_message", type=StringType, is_optional=True)
EnrichmentLog_enriched_at: Property = Property(name="enriched_at", type=DateTimeType)
EnrichmentLog.attributes={EnrichmentLog_id, EnrichmentLog_is_successful, EnrichmentLog_enriched_at, EnrichmentLog_error_message, EnrichmentLog_linkedin_url}

# ScoreHistory class attributes and methods
ScoreHistory_id: Property = Property(name="id", type=IntegerType)
ScoreHistory_old_score: Property = Property(name="old_score", type=IntegerType)
ScoreHistory_new_score: Property = Property(name="new_score", type=IntegerType)
ScoreHistory_reason: Property = Property(name="reason", type=StringType)
ScoreHistory_calculated_at: Property = Property(name="calculated_at", type=DateTimeType)
ScoreHistory.attributes={ScoreHistory_id, ScoreHistory_new_score, ScoreHistory_reason, ScoreHistory_old_score, ScoreHistory_calculated_at}

# Relationships
contact_company: BinaryAssociation = BinaryAssociation(
    name="contact_company",
    ends={
        Property(name="company", type=Company, multiplicity=Multiplicity(0, 1)),
        Property(name="contacts", type=Contact, multiplicity=Multiplicity(0, 9999))
    }
)
opportunity_contact: BinaryAssociation = BinaryAssociation(
    name="opportunity_contact",
    ends={
        Property(name="opportunities", type=Opportunity, multiplicity=Multiplicity(0, 9999)),
        Property(name="contacts", type=Contact, multiplicity=Multiplicity(1, 9999))
    }
)
opportunity_company: BinaryAssociation = BinaryAssociation(
    name="opportunity_company",
    ends={
        Property(name="company", type=Company, multiplicity=Multiplicity(0, 1)),
        Property(name="opportunities", type=Opportunity, multiplicity=Multiplicity(0, 9999))
    }
)
opportunity_owner: BinaryAssociation = BinaryAssociation(
    name="opportunity_owner",
    ends={
        Property(name="owner", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="owned_opportunities", type=Opportunity, multiplicity=Multiplicity(0, 9999))
    }
)
interaction_contact: BinaryAssociation = BinaryAssociation(
    name="interaction_contact",
    ends={
        Property(name="contact", type=Contact, multiplicity=Multiplicity(1, 1), is_composite=True),
        Property(name="interactions", type=Interaction, multiplicity=Multiplicity(0, 9999))
    }
)
interaction_user: BinaryAssociation = BinaryAssociation(
    name="interaction_user",
    ends={
        Property(name="performed_by", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="interactions", type=Interaction, multiplicity=Multiplicity(0, 9999))
    }
)
contact_tag: BinaryAssociation = BinaryAssociation(
    name="contact_tag",
    ends={
        Property(name="tagged_contacts", type=Contact, multiplicity=Multiplicity(0, 9999)),
        Property(name="tags", type=Tag, multiplicity=Multiplicity(0, 9999))
    }
)
company_tag: BinaryAssociation = BinaryAssociation(
    name="company_tag",
    ends={
        Property(name="tagged_companies", type=Company, multiplicity=Multiplicity(0, 9999)),
        Property(name="tags", type=Tag, multiplicity=Multiplicity(0, 9999))
    }
)
task_user: BinaryAssociation = BinaryAssociation(
    name="task_user",
    ends={
        Property(name="assigned_to", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="tasks", type=Task, multiplicity=Multiplicity(0, 9999))
    }
)
task_contact: BinaryAssociation = BinaryAssociation(
    name="task_contact",
    ends={
        Property(name="contact", type=Contact, multiplicity=Multiplicity(0, 1)),
        Property(name="tasks", type=Task, multiplicity=Multiplicity(0, 9999))
    }
)
task_opportunity: BinaryAssociation = BinaryAssociation(
    name="task_opportunity",
    ends={
        Property(name="opportunity", type=Opportunity, multiplicity=Multiplicity(0, 1)),
        Property(name="tasks", type=Task, multiplicity=Multiplicity(0, 9999))
    }
)
email_contact: BinaryAssociation = BinaryAssociation(
    name="email_contact",
    ends={
        Property(name="contact", type=Contact, multiplicity=Multiplicity(1, 1)),
        Property(name="generated_emails", type=GeneratedEmail, multiplicity=Multiplicity(0, 9999))
    }
)
email_user: BinaryAssociation = BinaryAssociation(
    name="email_user",
    ends={
        Property(name="created_by", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="generated_emails", type=GeneratedEmail, multiplicity=Multiplicity(0, 9999))
    }
)
email_template_link: BinaryAssociation = BinaryAssociation(
    name="email_template_link",
    ends={
        Property(name="template", type=EmailTemplate, multiplicity=Multiplicity(0, 1)),
        Property(name="generated_emails", type=GeneratedEmail, multiplicity=Multiplicity(0, 9999))
    }
)
template_user: BinaryAssociation = BinaryAssociation(
    name="template_user",
    ends={
        Property(name="created_by", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="email_templates", type=EmailTemplate, multiplicity=Multiplicity(0, 9999))
    }
)
enrichment_contact: BinaryAssociation = BinaryAssociation(
    name="enrichment_contact",
    ends={
        Property(name="contact", type=Contact, multiplicity=Multiplicity(1, 1)),
        Property(name="enrichment_logs", type=EnrichmentLog, multiplicity=Multiplicity(0, 9999))
    }
)
score_contact: BinaryAssociation = BinaryAssociation(
    name="score_contact",
    ends={
        Property(name="contact", type=Contact, multiplicity=Multiplicity(1, 1), is_composite=True),
        Property(name="score_history", type=ScoreHistory, multiplicity=Multiplicity(0, 9999))
    }
)
contact_created_by: BinaryAssociation = BinaryAssociation(
    name="contact_created_by",
    ends={
        Property(name="created_by", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="created_contacts", type=Contact, multiplicity=Multiplicity(0, 9999))
    }
)
company_created_by: BinaryAssociation = BinaryAssociation(
    name="company_created_by",
    ends={
        Property(name="created_by", type=User, multiplicity=Multiplicity(1, 1)),
        Property(name="created_companies", type=Company, multiplicity=Multiplicity(0, 9999))
    }
)

# Domain Model
domain_model = DomainModel(
    name="NexaCRM",
    types={User, Company, Contact, Opportunity, Interaction, Tag, Task, EmailTemplate, GeneratedEmail, EnrichmentLog, ScoreHistory, UserRole, LeadScoreLevel, OpportunityStage, InteractionType, InteractionDirection, Industry, CompanySize},
    associations={contact_company, opportunity_contact, opportunity_company, opportunity_owner, interaction_contact, interaction_user, contact_tag, company_tag, task_user, task_contact, task_opportunity, email_contact, email_user, email_template_link, template_user, enrichment_contact, score_contact, contact_created_by, company_created_by},
    generalizations={},
    metadata=None
)

from besser.BUML.metamodel.project import Project
from besser.BUML.metamodel.structural.structural import Metadata

metadata = Metadata(description="VIBE CODING VIBE MODELING")
project = Project(
    name="NexaCRM",
    models=[domain_model],
    owner="User",
    metadata=metadata
)