from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

class LeadScoreLevel(Enum):
    WARM = "WARM"
    COLD = "COLD"
    HOT = "HOT"

class InteractionDirection(Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"

class Industry(Enum):
    TECHNOLOGY = "TECHNOLOGY"
    SERVICES = "SERVICES"
    FINANCE = "FINANCE"
    RETAIL = "RETAIL"
    HEALTHCARE = "HEALTHCARE"
    MANUFACTURING = "MANUFACTURING"
    OTHER = "OTHER"

class OpportunityStage(Enum):
    CLOSED_LOST = "CLOSED_LOST"
    PROSPECTING = "PROSPECTING"
    CLOSED_WON = "CLOSED_WON"
    PROPOSAL = "PROPOSAL"
    NEGOTIATION = "NEGOTIATION"
    QUALIFICATION = "QUALIFICATION"

class InteractionType(Enum):
    CALL = "CALL"
    EMAIL = "EMAIL"
    NOTE = "NOTE"
    MEETING = "MEETING"

class UserRole(Enum):
    SALES_MANAGER = "SALES_MANAGER"
    SALES_REP = "SALES_REP"
    ADMIN = "ADMIN"

class CompanySize(Enum):
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"
    STARTUP = "STARTUP"
    ENTERPRISE = "ENTERPRISE"
    LARGE = "LARGE"

############################################
# Classes are defined here
############################################
class TaskCreate(BaseModel):
    created_at: datetime
    due_date: Optional[datetime] = None
    title: str
    id: int
    completed_at: Optional[datetime] = None
    description: Optional[str] = None
    is_completed: bool = False
    contact: Optional[int] = None  # N:1 Relationship (optional)
    opportunity: Optional[int] = None  # N:1 Relationship (optional)
    assigned_to: int  # N:1 Relationship (mandatory)


class EmailTemplateCreate(BaseModel):
    category: str
    created_at: datetime
    body_template: str
    name: str
    id: int
    subject_template: str
    created_by: int  # N:1 Relationship (mandatory)
    generated_emails: Optional[List[int]] = None  # 1:N Relationship


class GeneratedEmailCreate(BaseModel):
    created_at: datetime
    subject: str
    is_sent: bool = False
    sent_at: Optional[datetime] = None
    id: int
    body: str
    template: Optional[int] = None  # N:1 Relationship (optional)
    created_by: int  # N:1 Relationship (mandatory)
    contact: int  # N:1 Relationship (mandatory)


class EnrichmentLogCreate(BaseModel):
    is_successful: bool
    id: int
    enriched_at: datetime
    error_message: Optional[str] = None
    linkedin_url: str
    contact: int  # N:1 Relationship (mandatory)


class ScoreHistoryCreate(BaseModel):
    reason: str
    id: int
    new_score: int
    calculated_at: datetime
    old_score: int
    contact: int  # N:1 Relationship (mandatory)


class UserCreate(BaseModel):
    created_at: datetime
    last_name: str
    password_hash: str
    email: str
    first_name: str
    is_active: bool = True
    id: int
    role: UserRole
    last_login: Optional[datetime] = None
    created_contacts: Optional[List[int]] = None  # 1:N Relationship
    email_templates: Optional[List[int]] = None  # 1:N Relationship
    created_companies: Optional[List[int]] = None  # 1:N Relationship
    generated_emails: Optional[List[int]] = None  # 1:N Relationship
    owned_opportunities: Optional[List[int]] = None  # 1:N Relationship
    interactions: Optional[List[int]] = None  # 1:N Relationship
    tasks: Optional[List[int]] = None  # 1:N Relationship


class CompanyCreate(BaseModel):
    website: Optional[str] = None
    description: Optional[str] = None
    name: str
    city: Optional[str] = None
    id: int
    industry: Industry
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    updated_at: datetime
    address: Optional[str] = None
    created_at: datetime
    size: Optional[CompanySize] = None
    tags: List[int]  # N:M Relationship
    opportunities: Optional[List[int]] = None  # 1:N Relationship
    created_by: int  # N:1 Relationship (mandatory)
    contacts: Optional[List[int]] = None  # 1:N Relationship


class ContactCreate(BaseModel):
    first_name: str
    phone: Optional[str] = None
    lead_score: int = 0
    notes: Optional[str] = None
    job_title: Optional[str] = None
    created_at: datetime
    profile_picture_url: Optional[str] = None
    is_enriched: bool = False
    updated_at: datetime
    email: Optional[str] = None
    id: int
    last_name: str
    linkedin_url: Optional[str] = None
    lead_score_level: LeadScoreLevel = LeadScoreLevel.COLD
    created_by: int  # N:1 Relationship (mandatory)
    tags: List[int]  # N:M Relationship
    opportunities: List[int]  # N:M Relationship
    generated_emails: Optional[List[int]] = None  # 1:N Relationship
    interactions: Optional[List[int]] = None  # 1:N Relationship
    company: Optional[int] = None  # N:1 Relationship (optional)
    score_history: Optional[List[int]] = None  # 1:N Relationship
    tasks: Optional[List[int]] = None  # 1:N Relationship
    enrichment_logs: Optional[List[int]] = None  # 1:N Relationship


class OpportunityCreate(BaseModel):
    updated_at: datetime
    id: int
    created_at: datetime
    value: Optional[float] = None
    stage: OpportunityStage = OpportunityStage.PROSPECTING
    expected_close_date: Optional[date] = None
    closed_at: Optional[datetime] = None
    description: Optional[str] = None
    probability: Optional[int] = None
    title: str
    owner: int  # N:1 Relationship (mandatory)
    company: Optional[int] = None  # N:1 Relationship (optional)
    contacts: List[int]  # N:M Relationship
    tasks: Optional[List[int]] = None  # 1:N Relationship


class InteractionCreate(BaseModel):
    occurred_at: datetime
    subject: Optional[str] = None
    id: int
    type: InteractionType
    content: str
    created_at: datetime
    direction: Optional[InteractionDirection] = None
    performed_by: int  # N:1 Relationship (mandatory)
    contact: int  # N:1 Relationship (mandatory)


class TagCreate(BaseModel):
    id: int
    name: str
    color: str = "#3B82F6"
    tagged_contacts: List[int]  # N:M Relationship
    tagged_companies: List[int]  # N:M Relationship


