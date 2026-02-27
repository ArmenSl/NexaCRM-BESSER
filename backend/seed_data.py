"""
Seed script for NexaCRM — populates the database with realistic demo data.
Run: python seed_data.py
"""
import os
import sys
from datetime import datetime, timedelta
import random

# Setup SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql_alchemy import (
    Base, User, Company, Contact, Opportunity, Interaction, Task,
    Tag, EmailTemplate, GeneratedEmail, EnrichmentLog, ScoreHistory,
    opportunity_contact, company_tag, contact_tag,
    UserRole, CompanySize, Industry, LeadScoreLevel,
    OpportunityStage, InteractionType, InteractionDirection,
)
from auth import get_password_hash

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
os.makedirs("data", exist_ok=True)
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
db = Session()

NOW = datetime.utcnow()

def days_ago(n):
    return NOW - timedelta(days=n)

def hours_ago(n):
    return NOW - timedelta(hours=n)

print("Seeding NexaCRM database...")

# ─── Check if already seeded ────────────────────────────────────────────────
if db.query(User).count() > 0:
    print("Database already has data. Skipping seed.")
    sys.exit(0)

# ─── 1. USERS ───────────────────────────────────────────────────────────────
users_data = [
    {"email": "admin@nexacrm.com", "first_name": "Armen", "last_name": "SL", "role": UserRole.ADMIN, "password": "admin123"},
    {"email": "john.miller@nexacrm.com", "first_name": "John", "last_name": "Miller", "role": UserRole.SALES_MANAGER, "password": "password123"},
    {"email": "emma.wilson@nexacrm.com", "first_name": "Emma", "last_name": "Wilson", "role": UserRole.SALES_REP, "password": "password123"},
    {"email": "david.garcia@nexacrm.com", "first_name": "David", "last_name": "Garcia", "role": UserRole.SALES_REP, "password": "password123"},
    {"email": "lisa.johnson@nexacrm.com", "first_name": "Lisa", "last_name": "Johnson", "role": UserRole.SALES_REP, "password": "password123"},
]

users = []
for i, u in enumerate(users_data, 1):
    user = User(
        id=i,
        email=u["email"],
        password_hash=get_password_hash(u["password"]),
        first_name=u["first_name"],
        last_name=u["last_name"],
        role=u["role"].value,
        is_active=True,
        created_at=days_ago(90),
        last_login=hours_ago(random.randint(1, 48)),
    )
    db.add(user)
    users.append(user)
db.flush()
print(f"  Created {len(users)} users")

# ─── 2. TAGS ────────────────────────────────────────────────────────────────
tags_data = [
    {"name": "VIP", "color": "#e74c3c"},
    {"name": "Enterprise", "color": "#9b59b6"},
    {"name": "Startup", "color": "#3498db"},
    {"name": "Partner", "color": "#27ae60"},
    {"name": "Needs Follow-up", "color": "#e67e22"},
    {"name": "Decision Maker", "color": "#f39c12"},
    {"name": "Technical", "color": "#1abc9c"},
    {"name": "Churned", "color": "#95a5a6"},
]

tags = []
for i, t in enumerate(tags_data, 1):
    tag = Tag(id=i, name=t["name"], color=t["color"])
    db.add(tag)
    tags.append(tag)
db.flush()
print(f"  Created {len(tags)} tags")

# ─── 3. COMPANIES ───────────────────────────────────────────────────────────
companies_data = [
    {"name": "TechVision Inc.", "industry": Industry.TECHNOLOGY, "size": CompanySize.LARGE, "website": "https://techvision.com", "city": "San Francisco", "country": "USA", "phone": "+1-415-555-0100", "description": "Enterprise AI solutions provider"},
    {"name": "FinanceFlow", "industry": Industry.FINANCE, "size": CompanySize.ENTERPRISE, "website": "https://financeflow.io", "city": "New York", "country": "USA", "phone": "+1-212-555-0200", "description": "Digital banking platform"},
    {"name": "MedCore Health", "industry": Industry.HEALTHCARE, "size": CompanySize.MEDIUM, "website": "https://medcore.health", "city": "Boston", "country": "USA", "phone": "+1-617-555-0300", "description": "Healthcare data analytics"},
    {"name": "RetailEdge", "industry": Industry.RETAIL, "size": CompanySize.LARGE, "website": "https://retailedge.com", "city": "Chicago", "country": "USA", "phone": "+1-312-555-0400", "description": "E-commerce optimization platform"},
    {"name": "CloudScale Systems", "industry": Industry.TECHNOLOGY, "size": CompanySize.STARTUP, "website": "https://cloudscale.dev", "city": "Austin", "country": "USA", "phone": "+1-512-555-0500", "description": "Cloud infrastructure startup"},
    {"name": "GreenManufact", "industry": Industry.MANUFACTURING, "size": CompanySize.ENTERPRISE, "website": "https://greenmanufact.com", "city": "Detroit", "country": "USA", "phone": "+1-313-555-0600", "description": "Sustainable manufacturing solutions"},
    {"name": "DataPulse Analytics", "industry": Industry.SERVICES, "size": CompanySize.MEDIUM, "website": "https://datapulse.ai", "city": "Seattle", "country": "USA", "phone": "+1-206-555-0700", "description": "Business intelligence consulting"},
    {"name": "NovaPharma", "industry": Industry.HEALTHCARE, "size": CompanySize.LARGE, "website": "https://novapharma.com", "city": "San Diego", "country": "USA", "phone": "+1-619-555-0800", "description": "Pharmaceutical research company"},
    {"name": "UrbanRetail Group", "industry": Industry.RETAIL, "size": CompanySize.MEDIUM, "website": "https://urbanretail.co", "city": "Portland", "country": "USA", "phone": "+1-503-555-0900", "description": "Boutique retail chain"},
    {"name": "SecureNet Solutions", "industry": Industry.TECHNOLOGY, "size": CompanySize.SMALL, "website": "https://securenet.io", "city": "Denver", "country": "USA", "phone": "+1-720-555-1000", "description": "Cybersecurity firm"},
    {"name": "AlphaFinance", "industry": Industry.FINANCE, "size": CompanySize.LARGE, "website": "https://alphafinance.com", "city": "Charlotte", "country": "USA", "phone": "+1-704-555-1100", "description": "Investment management firm"},
    {"name": "SwiftLogistics", "industry": Industry.SERVICES, "size": CompanySize.MEDIUM, "website": "https://swiftlogistics.com", "city": "Memphis", "country": "USA", "phone": "+1-901-555-1200", "description": "Supply chain optimization"},
]

companies = []
for i, c in enumerate(companies_data, 1):
    company = Company(
        id=i,
        name=c["name"],
        industry=c["industry"].value,
        size=c["size"].value if c.get("size") else None,
        website=c.get("website"),
        city=c.get("city"),
        country=c.get("country"),
        phone=c.get("phone"),
        description=c.get("description"),
        created_at=days_ago(random.randint(30, 90)),
        updated_at=days_ago(random.randint(0, 15)),
        created_by_id=random.choice([1, 2]),
    )
    db.add(company)
    companies.append(company)
db.flush()

# Company-tag associations
for company in companies:
    num_tags = random.randint(0, 3)
    chosen_tags = random.sample(tags, min(num_tags, len(tags)))
    for tag in chosen_tags:
        db.execute(company_tag.insert().values(tagged_companies=company.id, tags=tag.id))
db.flush()
print(f"  Created {len(companies)} companies")

# ─── 4. CONTACTS ─────────────────────────────────────────────────────────────
contacts_data = [
    {"first_name": "Michael", "last_name": "Roberts", "email": "m.roberts@techvision.com", "job_title": "CTO", "company_id": 1, "phone": "+1-415-555-0101", "linkedin_url": "https://linkedin.com/in/michael-roberts", "is_enriched": True},
    {"first_name": "Jennifer", "last_name": "Adams", "email": "j.adams@techvision.com", "job_title": "VP of Engineering", "company_id": 1, "phone": "+1-415-555-0102"},
    {"first_name": "Robert", "last_name": "Chang", "email": "r.chang@financeflow.io", "job_title": "CEO", "company_id": 2, "phone": "+1-212-555-0201", "linkedin_url": "https://linkedin.com/in/robert-chang", "is_enriched": True},
    {"first_name": "Amanda", "last_name": "Foster", "email": "a.foster@financeflow.io", "job_title": "Head of Partnerships", "company_id": 2, "phone": "+1-212-555-0202"},
    {"first_name": "Dr. Sarah", "last_name": "Patel", "email": "s.patel@medcore.health", "job_title": "Chief Medical Officer", "company_id": 3, "phone": "+1-617-555-0301", "linkedin_url": "https://linkedin.com/in/sarah-patel"},
    {"first_name": "James", "last_name": "O'Brien", "email": "j.obrien@retailedge.com", "job_title": "Director of Sales", "company_id": 4, "phone": "+1-312-555-0401"},
    {"first_name": "Aisha", "last_name": "Kimani", "email": "a.kimani@cloudscale.dev", "job_title": "Co-Founder", "company_id": 5, "phone": "+1-512-555-0501", "linkedin_url": "https://linkedin.com/in/aisha-kimani", "is_enriched": True},
    {"first_name": "Thomas", "last_name": "Weber", "email": "t.weber@greenmanufact.com", "job_title": "Procurement Manager", "company_id": 6, "phone": "+1-313-555-0601"},
    {"first_name": "Elena", "last_name": "Volkov", "email": "e.volkov@datapulse.ai", "job_title": "Head of Analytics", "company_id": 7, "phone": "+1-206-555-0701", "linkedin_url": "https://linkedin.com/in/elena-volkov"},
    {"first_name": "Marcus", "last_name": "Lee", "email": "m.lee@novapharma.com", "job_title": "VP of Business Development", "company_id": 8, "phone": "+1-619-555-0801"},
    {"first_name": "Sophie", "last_name": "Martin", "email": "s.martin@urbanretail.co", "job_title": "CEO", "company_id": 9, "phone": "+1-503-555-0901", "linkedin_url": "https://linkedin.com/in/sophie-martin", "is_enriched": True},
    {"first_name": "Kevin", "last_name": "Nguyen", "email": "k.nguyen@securenet.io", "job_title": "Founder & CTO", "company_id": 10, "phone": "+1-720-555-1001"},
    {"first_name": "Rachel", "last_name": "Green", "email": "r.green@alphafinance.com", "job_title": "Managing Director", "company_id": 11, "phone": "+1-704-555-1101", "linkedin_url": "https://linkedin.com/in/rachel-green"},
    {"first_name": "Daniel", "last_name": "Kim", "email": "d.kim@swiftlogistics.com", "job_title": "Operations Director", "company_id": 12, "phone": "+1-901-555-1201"},
    {"first_name": "Olivia", "last_name": "Brown", "email": "o.brown@techvision.com", "job_title": "Product Manager", "company_id": 1, "phone": "+1-415-555-0103"},
    {"first_name": "Lucas", "last_name": "Fernandez", "email": "l.fernandez@financeflow.io", "job_title": "Head of Risk", "company_id": 2},
    {"first_name": "Maria", "last_name": "Santos", "email": "m.santos@medcore.health", "job_title": "Research Director", "company_id": 3, "phone": "+1-617-555-0302"},
    {"first_name": "Andrew", "last_name": "Thompson", "email": "a.thompson@retailedge.com", "job_title": "CTO", "company_id": 4, "phone": "+1-312-555-0402", "linkedin_url": "https://linkedin.com/in/andrew-thompson", "is_enriched": True},
    {"first_name": "Priya", "last_name": "Sharma", "email": "p.sharma@cloudscale.dev", "job_title": "Head of Sales", "company_id": 5, "phone": "+1-512-555-0502"},
    {"first_name": "Chris", "last_name": "Wallace", "email": "c.wallace@greenmanufact.com", "job_title": "VP of Operations", "company_id": 6, "phone": "+1-313-555-0602"},
]

score_levels = {
    "HOT": LeadScoreLevel.HOT,
    "WARM": LeadScoreLevel.WARM,
    "COLD": LeadScoreLevel.COLD,
}

contacts = []
for i, c in enumerate(contacts_data, 1):
    score = random.randint(5, 95)
    level = "HOT" if score >= 70 else ("WARM" if score >= 40 else "COLD")
    pic_url = None
    if c.get("is_enriched"):
        pic_url = f"https://ui-avatars.com/api/?name={c['first_name']}+{c['last_name']}&background=5a3d91&color=fff&size=200"

    contact = Contact(
        id=i,
        first_name=c["first_name"],
        last_name=c["last_name"],
        email=c.get("email"),
        job_title=c.get("job_title"),
        phone=c.get("phone"),
        linkedin_url=c.get("linkedin_url"),
        profile_picture_url=pic_url,
        is_enriched=c.get("is_enriched", False),
        lead_score=score,
        lead_score_level=score_levels[level].value,
        created_at=days_ago(random.randint(15, 80)),
        updated_at=days_ago(random.randint(0, 10)),
        company_id=c.get("company_id"),
        created_by_id=random.choice([2, 3, 4, 5]),
    )
    db.add(contact)
    contacts.append(contact)
db.flush()

# Contact-tag associations
for contact in contacts:
    num_tags = random.randint(0, 3)
    chosen_tags = random.sample(tags, min(num_tags, len(tags)))
    for tag in chosen_tags:
        db.execute(contact_tag.insert().values(tagged_contacts=contact.id, tags=tag.id))
db.flush()
print(f"  Created {len(contacts)} contacts")

# ─── 5. OPPORTUNITIES ───────────────────────────────────────────────────────
opportunities_data = [
    {"title": "TechVision Enterprise License", "value": 250000, "stage": OpportunityStage.NEGOTIATION, "probability": 75, "company_id": 1, "owner_id": 2, "contact_ids": [1, 2]},
    {"title": "FinanceFlow Platform Integration", "value": 180000, "stage": OpportunityStage.PROPOSAL, "probability": 60, "company_id": 2, "owner_id": 3, "contact_ids": [3, 4]},
    {"title": "MedCore Analytics Suite", "value": 95000, "stage": OpportunityStage.QUALIFICATION, "probability": 40, "company_id": 3, "owner_id": 4, "contact_ids": [5]},
    {"title": "RetailEdge Multi-Store Rollout", "value": 320000, "stage": OpportunityStage.CLOSED_WON, "probability": 100, "company_id": 4, "owner_id": 2, "contact_ids": [6]},
    {"title": "CloudScale Infrastructure Deal", "value": 45000, "stage": OpportunityStage.PROSPECTING, "probability": 20, "company_id": 5, "owner_id": 5, "contact_ids": [7]},
    {"title": "GreenManufact Automation", "value": 150000, "stage": OpportunityStage.PROPOSAL, "probability": 55, "company_id": 6, "owner_id": 3, "contact_ids": [8]},
    {"title": "DataPulse Consulting Contract", "value": 75000, "stage": OpportunityStage.NEGOTIATION, "probability": 80, "company_id": 7, "owner_id": 4, "contact_ids": [9]},
    {"title": "NovaPharma Research Platform", "value": 420000, "stage": OpportunityStage.QUALIFICATION, "probability": 35, "company_id": 8, "owner_id": 2, "contact_ids": [10]},
    {"title": "UrbanRetail POS System", "value": 60000, "stage": OpportunityStage.CLOSED_WON, "probability": 100, "company_id": 9, "owner_id": 5, "contact_ids": [11]},
    {"title": "SecureNet Security Audit", "value": 35000, "stage": OpportunityStage.PROSPECTING, "probability": 15, "company_id": 10, "owner_id": 3, "contact_ids": [12]},
    {"title": "AlphaFinance Dashboard", "value": 200000, "stage": OpportunityStage.NEGOTIATION, "probability": 70, "company_id": 11, "owner_id": 2, "contact_ids": [13]},
    {"title": "SwiftLogistics Tracking Module", "value": 85000, "stage": OpportunityStage.PROPOSAL, "probability": 50, "company_id": 12, "owner_id": 4, "contact_ids": [14]},
    {"title": "TechVision Support Extension", "value": 50000, "stage": OpportunityStage.CLOSED_LOST, "probability": 0, "company_id": 1, "owner_id": 3, "contact_ids": [1, 15]},
    {"title": "FinanceFlow Compliance Module", "value": 130000, "stage": OpportunityStage.QUALIFICATION, "probability": 45, "company_id": 2, "owner_id": 5, "contact_ids": [3, 16]},
    {"title": "CloudScale Premium Support", "value": 28000, "stage": OpportunityStage.CLOSED_WON, "probability": 100, "company_id": 5, "owner_id": 5, "contact_ids": [7, 19]},
]

opportunities = []
for i, o in enumerate(opportunities_data, 1):
    closed = None
    exp_close = None
    if o["stage"] in (OpportunityStage.CLOSED_WON, OpportunityStage.CLOSED_LOST):
        closed = days_ago(random.randint(1, 20))
    else:
        exp_close = (NOW + timedelta(days=random.randint(10, 90))).date()

    opp = Opportunity(
        id=i,
        title=o["title"],
        value=o["value"],
        stage=o["stage"].value,
        probability=o["probability"],
        expected_close_date=exp_close,
        closed_at=closed,
        created_at=days_ago(random.randint(20, 70)),
        updated_at=days_ago(random.randint(0, 10)),
        owner_id=o["owner_id"],
        company_id=o.get("company_id"),
    )
    db.add(opp)
    opportunities.append(opp)
db.flush()

# Opportunity-contact associations
for i, o in enumerate(opportunities_data):
    for cid in o["contact_ids"]:
        db.execute(opportunity_contact.insert().values(opportunities=i + 1, contacts=cid))
db.flush()
print(f"  Created {len(opportunities)} opportunities")

# ─── 6. INTERACTIONS ─────────────────────────────────────────────────────────
interaction_templates = [
    {"type": InteractionType.CALL, "subjects": ["Discovery call", "Follow-up call", "Demo scheduled", "Pricing discussion", "Quarterly check-in"]},
    {"type": InteractionType.EMAIL, "subjects": ["Introduction email", "Proposal sent", "Follow-up on meeting", "Product update", "Thank you note"]},
    {"type": InteractionType.MEETING, "subjects": ["Product demo", "Executive presentation", "Strategy session", "Contract review", "Onboarding kickoff"]},
    {"type": InteractionType.NOTE, "subjects": ["Meeting notes", "Internal discussion", "Competitor mentioned", "Budget confirmed", "Timeline updated"]},
]

content_templates = {
    InteractionType.CALL: [
        "Discussed current pain points with {name}. They mentioned issues with {topic}. Scheduled follow-up for next week.",
        "Quick call with {name} to review proposal details. They're interested but need internal approval from {role}.",
        "Called {name} to check on decision timeline. Budget approval expected by end of month.",
        "{name} called to ask about integration capabilities. Sent technical documentation afterwards.",
        "30-minute call reviewing pricing tiers with {name}. They're comparing with two other vendors.",
    ],
    InteractionType.EMAIL: [
        "Sent introductory email to {name} outlining our key value propositions for their {industry} use case.",
        "Followed up with {name} after the demo. Attached case study from similar {industry} client.",
        "Sent revised proposal to {name} with the volume discount they requested. Awaiting response.",
        "Shared product roadmap update with {name}. New features align well with their requirements.",
        "Thank you email to {name} after productive meeting. Outlined next steps and timeline.",
    ],
    InteractionType.MEETING: [
        "Full product demo with {name} and their team. Strong interest in the analytics module. Next step: technical deep-dive.",
        "Executive presentation to {name} and leadership team. CEO was particularly interested in ROI projections.",
        "Strategy session with {name} to map out implementation plan. Estimated 6-week deployment timeline.",
        "Contract review meeting with {name} and legal team. Minor revisions needed on SLA terms.",
        "Onboarding kickoff with {name}. Assigned dedicated success manager. Training scheduled for next week.",
    ],
    InteractionType.NOTE: [
        "Internal note: {name} mentioned they're also evaluating CompetitorX. We need to emphasize our {topic} advantage.",
        "Note from team meeting: {name}'s budget for Q2 is confirmed at $150K. We're within range.",
        "Spoke with {role} internally about {name}'s account. Recommended fast-tracking the proposal.",
        "{name} shared positive feedback from their pilot users. Conversion probability increased.",
        "Timeline update: {name} pushed decision to next quarter due to internal reorganization.",
    ],
}

topics = ["data migration", "API performance", "scalability", "security compliance", "user onboarding", "reporting accuracy"]
roles = ["VP of Sales", "CFO", "Director of IT", "Head of Procurement", "CIO"]
industries = ["technology", "finance", "healthcare", "retail", "manufacturing"]

interactions = []
ix_id = 1
for contact in contacts:
    num_interactions = random.randint(1, 8)
    for _ in range(num_interactions):
        tmpl = random.choice(interaction_templates)
        ix_type = tmpl["type"]
        subject = random.choice(tmpl["subjects"])
        content = random.choice(content_templates[ix_type]).format(
            name=f"{contact.first_name} {contact.last_name}",
            topic=random.choice(topics),
            role=random.choice(roles),
            industry=random.choice(industries),
        )
        direction = random.choice([InteractionDirection.INBOUND, InteractionDirection.OUTBOUND])

        ix = Interaction(
            id=ix_id,
            type=ix_type.value,
            direction=direction.value,
            subject=subject,
            content=content,
            occurred_at=days_ago(random.randint(0, 60)),
            created_at=days_ago(random.randint(0, 60)),
            contact_id=contact.id,
            performed_by_id=random.choice([2, 3, 4, 5]),
        )
        db.add(ix)
        interactions.append(ix)
        ix_id += 1
db.flush()
print(f"  Created {len(interactions)} interactions")

# ─── 7. TASKS ────────────────────────────────────────────────────────────────
task_titles = [
    "Send follow-up proposal", "Schedule product demo", "Review contract terms",
    "Prepare case study", "Call to discuss pricing", "Send meeting recap",
    "Update CRM notes", "Research competitor offering", "Prepare quarterly review",
    "Follow up on pending approval", "Send onboarding materials", "Draft partnership proposal",
]

tasks = []
for i in range(1, 21):
    is_completed = random.random() < 0.35
    contact_id = random.choice(contacts).id
    opp = random.choice(opportunities) if random.random() < 0.5 else None

    task = Task(
        id=i,
        title=random.choice(task_titles),
        description=f"Action item related to {'opportunity ' + str(opp.id) if opp else 'contact ' + str(contact_id)}",
        is_completed=is_completed,
        created_at=days_ago(random.randint(1, 30)),
        due_date=NOW + timedelta(days=random.randint(-5, 20)) if not is_completed else None,
        completed_at=days_ago(random.randint(0, 5)) if is_completed else None,
        assigned_to_id=random.choice([2, 3, 4, 5]),
        contact_id=contact_id,
        opportunity_id=opp.id if opp else None,
    )
    db.add(task)
    tasks.append(task)
db.flush()
print(f"  Created {len(tasks)} tasks")

# ─── 8. EMAIL TEMPLATES ─────────────────────────────────────────────────────
templates_data = [
    {"name": "Cold Outreach", "category": "Prospecting", "subject": "Helping {company} with {first_name}", "body": "Hi {first_name},\n\nI came across {company} and was impressed by your work in the industry.\n\nWe help companies like yours solve common challenges around efficiency and growth.\n\nWould you be open to a brief 15-minute call this week?\n\nBest regards"},
    {"name": "Follow-Up After Demo", "category": "Follow-up", "subject": "Great connecting, {first_name}!", "body": "Hi {first_name},\n\nThank you for taking the time to see our product demo today. I was excited to hear about your goals at {company}.\n\nAs discussed, I've attached the relevant case study. I think you'll find the results compelling.\n\nShall we schedule a follow-up to discuss next steps?\n\nBest regards"},
    {"name": "Deal Closing", "category": "Closing", "subject": "Next steps for {company}", "body": "Hi {first_name},\n\nI wanted to follow up on our recent conversation about the proposal for {company}.\n\nWe're confident that our solution will deliver significant value, and we'd love to finalize the details.\n\nAre you available for a quick call to review the final terms?\n\nBest regards"},
]

email_templates = []
for i, t in enumerate(templates_data, 1):
    et = EmailTemplate(
        id=i,
        name=t["name"],
        category=t["category"],
        subject_template=t["subject"],
        body_template=t["body"],
        created_at=days_ago(60),
        created_by_id=1,
    )
    db.add(et)
    email_templates.append(et)
db.flush()
print(f"  Created {len(email_templates)} email templates")

# ─── 9. GENERATED EMAILS ────────────────────────────────────────────────────
gen_emails = []
for i in range(1, 7):
    contact = random.choice(contacts[:10])
    ge = GeneratedEmail(
        id=i,
        subject=f"Following up - {contact.first_name} {contact.last_name}",
        body=f"Hi {contact.first_name},\n\nI hope this message finds you well at {companies[contact.company_id - 1].name}. I wanted to reach out regarding a potential collaboration that could help streamline your operations.\n\nWould you be available for a quick call this week?\n\nBest regards",
        is_sent=random.random() < 0.5,
        sent_at=days_ago(random.randint(0, 5)) if random.random() < 0.3 else None,
        created_at=days_ago(random.randint(0, 15)),
        contact_id=contact.id,
        template_id=random.choice([1, 2, 3]) if random.random() < 0.7 else None,
        created_by_id=random.choice([2, 3, 4, 5]),
    )
    db.add(ge)
    gen_emails.append(ge)
db.flush()
print(f"  Created {len(gen_emails)} generated emails")

# ─── 10. ENRICHMENT LOGS ────────────────────────────────────────────────────
enrich_logs = []
elog_id = 1
for contact in contacts:
    if contact.is_enriched or contact.linkedin_url:
        elog = EnrichmentLog(
            id=elog_id,
            contact_id=contact.id,
            linkedin_url=contact.linkedin_url or "https://linkedin.com/in/unknown",
            enriched_at=days_ago(random.randint(1, 30)),
            is_successful=contact.is_enriched,
            error_message=None if contact.is_enriched else "Profile not found",
        )
        db.add(elog)
        enrich_logs.append(elog)
        elog_id += 1
db.flush()
print(f"  Created {len(enrich_logs)} enrichment logs")

# ─── 11. SCORE HISTORY ──────────────────────────────────────────────────────
score_entries = []
sh_id = 1
for contact in contacts:
    num_entries = random.randint(1, 4)
    prev_score = random.randint(0, 30)
    for j in range(num_entries):
        new_score = min(prev_score + random.randint(5, 25), 100)
        reasons = [
            "New interaction recorded",
            "Post-enrichment recalculation",
            "Opportunity updated",
            "Manual recalculation",
            "Periodic score refresh",
        ]
        sh = ScoreHistory(
            id=sh_id,
            contact_id=contact.id,
            old_score=prev_score,
            new_score=new_score,
            reason=random.choice(reasons),
            calculated_at=days_ago(random.randint(0, 50)),
        )
        db.add(sh)
        score_entries.append(sh)
        prev_score = new_score
        sh_id += 1
db.flush()
print(f"  Created {len(score_entries)} score history entries")

# ─── COMMIT ──────────────────────────────────────────────────────────────────
db.commit()
db.close()

print("\nDatabase seeded successfully!")
print(f"  Login credentials:")
print(f"    admin@nexacrm.com / admin123 (Admin)")
print(f"    john.miller@nexacrm.com / password123 (Sales Manager)")
print(f"    emma.wilson@nexacrm.com / password123 (Sales Rep)")
print(f"    david.garcia@nexacrm.com / password123 (Sales Rep)")
print(f"    lisa.johnson@nexacrm.com / password123 (Sales Rep)")
