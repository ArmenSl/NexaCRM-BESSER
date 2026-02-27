import enum
from typing import List, Optional
from sqlalchemy import (
    create_engine, Column, ForeignKey, Table, Text, Boolean, String, Date, 
    Time, DateTime, Float, Integer, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass

# Definitions of Enumerations
class LeadScoreLevel(enum.Enum):
    WARM = "WARM"
    COLD = "COLD"
    HOT = "HOT"

class InteractionDirection(enum.Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"

class Industry(enum.Enum):
    TECHNOLOGY = "TECHNOLOGY"
    SERVICES = "SERVICES"
    FINANCE = "FINANCE"
    RETAIL = "RETAIL"
    HEALTHCARE = "HEALTHCARE"
    MANUFACTURING = "MANUFACTURING"
    OTHER = "OTHER"

class OpportunityStage(enum.Enum):
    CLOSED_LOST = "CLOSED_LOST"
    PROSPECTING = "PROSPECTING"
    CLOSED_WON = "CLOSED_WON"
    PROPOSAL = "PROPOSAL"
    NEGOTIATION = "NEGOTIATION"
    QUALIFICATION = "QUALIFICATION"

class InteractionType(enum.Enum):
    CALL = "CALL"
    EMAIL = "EMAIL"
    NOTE = "NOTE"
    MEETING = "MEETING"

class UserRole(enum.Enum):
    SALES_MANAGER = "SALES_MANAGER"
    SALES_REP = "SALES_REP"
    ADMIN = "ADMIN"

class CompanySize(enum.Enum):
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"
    STARTUP = "STARTUP"
    ENTERPRISE = "ENTERPRISE"
    LARGE = "LARGE"


# Tables definition for many-to-many relationships
opportunity_contact = Table(
    "opportunity_contact",
    Base.metadata,
    Column("contacts", ForeignKey("contact.id"), primary_key=True),
    Column("opportunities", ForeignKey("opportunity.id"), primary_key=True),
)
company_tag = Table(
    "company_tag",
    Base.metadata,
    Column("tagged_companies", ForeignKey("company.id"), primary_key=True),
    Column("tags", ForeignKey("tag.id"), primary_key=True),
)
contact_tag = Table(
    "contact_tag",
    Base.metadata,
    Column("tags", ForeignKey("tag.id"), primary_key=True),
    Column("tagged_contacts", ForeignKey("contact.id"), primary_key=True),
)

# Tables definition
class Task(Base):
    __tablename__ = "task"
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    due_date: Mapped[Optional[dt_datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[dt_datetime] = mapped_column(DateTime)
    title: Mapped[str] = mapped_column(String(100))
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    completed_at: Mapped[Optional[dt_datetime]] = mapped_column(DateTime, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contact.id"), nullable=True)
    assigned_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunity.id"), nullable=True)

class EmailTemplate(Base):
    __tablename__ = "emailtemplate"
    created_at: Mapped[dt_datetime] = mapped_column(DateTime)
    category: Mapped[str] = mapped_column(String(100))
    body_template: Mapped[str] = mapped_column(Text)
    subject_template: Mapped[str] = mapped_column(String(500))
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

class GeneratedEmail(Base):
    __tablename__ = "generatedemail"
    created_at: Mapped[dt_datetime] = mapped_column(DateTime)
    sent_at: Mapped[Optional[dt_datetime]] = mapped_column(DateTime, nullable=True)
    is_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    body: Mapped[str] = mapped_column(Text)
    subject: Mapped[str] = mapped_column(String(500))
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contact.id"))
    template_id: Mapped[int] = mapped_column(ForeignKey("emailtemplate.id"), nullable=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

class EnrichmentLog(Base):
    __tablename__ = "enrichmentlog"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    error_message: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_successful: Mapped[bool] = mapped_column(Boolean)
    linkedin_url: Mapped[str] = mapped_column(String(100))
    enriched_at: Mapped[dt_datetime] = mapped_column(DateTime)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contact.id"))

class ScoreHistory(Base):
    __tablename__ = "scorehistory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    calculated_at: Mapped[dt_datetime] = mapped_column(DateTime)
    reason: Mapped[str] = mapped_column(String(100))
    new_score: Mapped[int] = mapped_column(Integer)
    old_score: Mapped[int] = mapped_column(Integer)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contact.id"))

class User(Base):
    __tablename__ = "user"
    last_name: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))
    last_login: Mapped[Optional[dt_datetime]] = mapped_column(DateTime, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[dt_datetime] = mapped_column(DateTime)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))

class Company(Base):
    __tablename__ = "company"
    website: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[dt_datetime] = mapped_column(DateTime)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    updated_at: Mapped[dt_datetime] = mapped_column(DateTime)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    size: Mapped[Optional[CompanySize]] = mapped_column(Enum(CompanySize), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    industry: Mapped[Industry] = mapped_column(Enum(Industry))
    address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

class Contact(Base):
    __tablename__ = "contact"
    updated_at: Mapped[dt_datetime] = mapped_column(DateTime)
    phone: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    lead_score_level: Mapped[LeadScoreLevel] = mapped_column(Enum(LeadScoreLevel), default=LeadScoreLevel.COLD)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    lead_score: Mapped[int] = mapped_column(Integer, default=0)
    last_name: Mapped[str] = mapped_column(String(100))
    profile_picture_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    first_name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[dt_datetime] = mapped_column(DateTime)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    notes: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    job_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_enriched: Mapped[bool] = mapped_column(Boolean, default=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

class Opportunity(Base):
    __tablename__ = "opportunity"
    expected_close_date: Mapped[Optional[dt_date]] = mapped_column(Date, nullable=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    probability: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    closed_at: Mapped[Optional[dt_datetime]] = mapped_column(DateTime, nullable=True)
    stage: Mapped[OpportunityStage] = mapped_column(Enum(OpportunityStage), default=OpportunityStage.PROSPECTING)
    updated_at: Mapped[dt_datetime] = mapped_column(DateTime)
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[dt_datetime] = mapped_column(DateTime)
    title: Mapped[str] = mapped_column(String(100))
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=True)

class Interaction(Base):
    __tablename__ = "interaction"
    created_at: Mapped[dt_datetime] = mapped_column(DateTime)
    subject: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    type: Mapped[InteractionType] = mapped_column(Enum(InteractionType))
    content: Mapped[str] = mapped_column(String(100))
    occurred_at: Mapped[dt_datetime] = mapped_column(DateTime)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    direction: Mapped[Optional[InteractionDirection]] = mapped_column(Enum(InteractionDirection), nullable=True)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contact.id"))
    performed_by_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

class Tag(Base):
    __tablename__ = "tag"
    name: Mapped[str] = mapped_column(String(100))
    color: Mapped[str] = mapped_column(String(100), default="#3B82F6")
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


#--- Relationships of the task table
Task.contact: Mapped["Contact"] = relationship("Contact", back_populates="tasks", foreign_keys=[Task.contact_id])
Task.assigned_to: Mapped["User"] = relationship("User", back_populates="tasks", foreign_keys=[Task.assigned_to_id])
Task.opportunity: Mapped["Opportunity"] = relationship("Opportunity", back_populates="tasks", foreign_keys=[Task.opportunity_id])

#--- Relationships of the emailtemplate table
EmailTemplate.created_by: Mapped["User"] = relationship("User", back_populates="email_templates", foreign_keys=[EmailTemplate.created_by_id])
EmailTemplate.generated_emails: Mapped[List["GeneratedEmail"]] = relationship("GeneratedEmail", back_populates="template", foreign_keys=[GeneratedEmail.template_id])

#--- Relationships of the generatedemail table
GeneratedEmail.contact: Mapped["Contact"] = relationship("Contact", back_populates="generated_emails", foreign_keys=[GeneratedEmail.contact_id])
GeneratedEmail.template: Mapped["EmailTemplate"] = relationship("EmailTemplate", back_populates="generated_emails", foreign_keys=[GeneratedEmail.template_id])
GeneratedEmail.created_by: Mapped["User"] = relationship("User", back_populates="generated_emails", foreign_keys=[GeneratedEmail.created_by_id])

#--- Relationships of the enrichmentlog table
EnrichmentLog.contact: Mapped["Contact"] = relationship("Contact", back_populates="enrichment_logs", foreign_keys=[EnrichmentLog.contact_id])

#--- Relationships of the scorehistory table
ScoreHistory.contact: Mapped["Contact"] = relationship("Contact", back_populates="score_history", foreign_keys=[ScoreHistory.contact_id])

#--- Relationships of the user table
User.created_contacts: Mapped[List["Contact"]] = relationship("Contact", back_populates="created_by", foreign_keys=[Contact.created_by_id])
User.generated_emails: Mapped[List["GeneratedEmail"]] = relationship("GeneratedEmail", back_populates="created_by", foreign_keys=[GeneratedEmail.created_by_id])
User.interactions: Mapped[List["Interaction"]] = relationship("Interaction", back_populates="performed_by", foreign_keys=[Interaction.performed_by_id])
User.tasks: Mapped[List["Task"]] = relationship("Task", back_populates="assigned_to", foreign_keys=[Task.assigned_to_id])
User.email_templates: Mapped[List["EmailTemplate"]] = relationship("EmailTemplate", back_populates="created_by", foreign_keys=[EmailTemplate.created_by_id])
User.owned_opportunities: Mapped[List["Opportunity"]] = relationship("Opportunity", back_populates="owner", foreign_keys=[Opportunity.owner_id])
User.created_companies: Mapped[List["Company"]] = relationship("Company", back_populates="created_by", foreign_keys=[Company.created_by_id])

#--- Relationships of the company table
Company.opportunities: Mapped[List["Opportunity"]] = relationship("Opportunity", back_populates="company", foreign_keys=[Opportunity.company_id])
Company.created_by: Mapped["User"] = relationship("User", back_populates="created_companies", foreign_keys=[Company.created_by_id])
Company.contacts: Mapped[List["Contact"]] = relationship("Contact", back_populates="company", foreign_keys=[Contact.company_id])
Company.tags: Mapped[List["Tag"]] = relationship("Tag", secondary=company_tag, back_populates="tagged_companies")

#--- Relationships of the contact table
Contact.interactions: Mapped[List["Interaction"]] = relationship("Interaction", back_populates="contact", foreign_keys=[Interaction.contact_id])
Contact.tags: Mapped[List["Tag"]] = relationship("Tag", secondary=contact_tag, back_populates="tagged_contacts")
Contact.generated_emails: Mapped[List["GeneratedEmail"]] = relationship("GeneratedEmail", back_populates="contact", foreign_keys=[GeneratedEmail.contact_id])
Contact.company: Mapped["Company"] = relationship("Company", back_populates="contacts", foreign_keys=[Contact.company_id])
Contact.created_by: Mapped["User"] = relationship("User", back_populates="created_contacts", foreign_keys=[Contact.created_by_id])
Contact.enrichment_logs: Mapped[List["EnrichmentLog"]] = relationship("EnrichmentLog", back_populates="contact", foreign_keys=[EnrichmentLog.contact_id])
Contact.score_history: Mapped[List["ScoreHistory"]] = relationship("ScoreHistory", back_populates="contact", foreign_keys=[ScoreHistory.contact_id])
Contact.tasks: Mapped[List["Task"]] = relationship("Task", back_populates="contact", foreign_keys=[Task.contact_id])
Contact.opportunities: Mapped[List["Opportunity"]] = relationship("Opportunity", secondary=opportunity_contact, back_populates="contacts")

#--- Relationships of the opportunity table
Opportunity.owner: Mapped["User"] = relationship("User", back_populates="owned_opportunities", foreign_keys=[Opportunity.owner_id])
Opportunity.company: Mapped["Company"] = relationship("Company", back_populates="opportunities", foreign_keys=[Opportunity.company_id])
Opportunity.contacts: Mapped[List["Contact"]] = relationship("Contact", secondary=opportunity_contact, back_populates="opportunities")
Opportunity.tasks: Mapped[List["Task"]] = relationship("Task", back_populates="opportunity", foreign_keys=[Task.opportunity_id])

#--- Relationships of the interaction table
Interaction.contact: Mapped["Contact"] = relationship("Contact", back_populates="interactions", foreign_keys=[Interaction.contact_id])
Interaction.performed_by: Mapped["User"] = relationship("User", back_populates="interactions", foreign_keys=[Interaction.performed_by_id])

#--- Relationships of the tag table
Tag.tagged_contacts: Mapped[List["Contact"]] = relationship("Contact", secondary=contact_tag, back_populates="tags")
Tag.tagged_companies: Mapped[List["Company"]] = relationship("Company", secondary=company_tag, back_populates="tags")

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)