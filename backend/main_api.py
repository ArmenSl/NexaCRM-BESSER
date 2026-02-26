import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "Task", "description": "Operations for Task entities"},
        {"name": "Task Relationships", "description": "Manage Task relationships"},
        {"name": "EmailTemplate", "description": "Operations for EmailTemplate entities"},
        {"name": "EmailTemplate Relationships", "description": "Manage EmailTemplate relationships"},
        {"name": "GeneratedEmail", "description": "Operations for GeneratedEmail entities"},
        {"name": "GeneratedEmail Relationships", "description": "Manage GeneratedEmail relationships"},
        {"name": "EnrichmentLog", "description": "Operations for EnrichmentLog entities"},
        {"name": "EnrichmentLog Relationships", "description": "Manage EnrichmentLog relationships"},
        {"name": "ScoreHistory", "description": "Operations for ScoreHistory entities"},
        {"name": "ScoreHistory Relationships", "description": "Manage ScoreHistory relationships"},
        {"name": "User", "description": "Operations for User entities"},
        {"name": "User Relationships", "description": "Manage User relationships"},
        {"name": "Company", "description": "Operations for Company entities"},
        {"name": "Company Relationships", "description": "Manage Company relationships"},
        {"name": "Contact", "description": "Operations for Contact entities"},
        {"name": "Contact Relationships", "description": "Manage Contact relationships"},
        {"name": "Opportunity", "description": "Operations for Opportunity entities"},
        {"name": "Opportunity Relationships", "description": "Manage Opportunity relationships"},
        {"name": "Interaction", "description": "Operations for Interaction entities"},
        {"name": "Interaction Relationships", "description": "Manage Interaction relationships"},
        {"name": "Tag", "description": "Operations for Tag entities"},
        {"name": "Tag Relationships", "description": "Manage Tag relationships"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["task_count"] = database.query(Task).count()
    stats["emailtemplate_count"] = database.query(EmailTemplate).count()
    stats["generatedemail_count"] = database.query(GeneratedEmail).count()
    stats["enrichmentlog_count"] = database.query(EnrichmentLog).count()
    stats["scorehistory_count"] = database.query(ScoreHistory).count()
    stats["user_count"] = database.query(User).count()
    stats["company_count"] = database.query(Company).count()
    stats["contact_count"] = database.query(Contact).count()
    stats["opportunity_count"] = database.query(Opportunity).count()
    stats["interaction_count"] = database.query(Interaction).count()
    stats["tag_count"] = database.query(Tag).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   Task functions
#
############################################

@app.get("/task/", response_model=None, tags=["Task"])
def get_all_task(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Task)
        query = query.options(joinedload(Task.contact))
        query = query.options(joinedload(Task.opportunity))
        query = query.options(joinedload(Task.assigned_to))
        task_list = query.all()

        # Serialize with relationships included
        result = []
        for task_item in task_list:
            item_dict = task_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if task_item.contact:
                related_obj = task_item.contact
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['contact'] = related_dict
            else:
                item_dict['contact'] = None
            if task_item.opportunity:
                related_obj = task_item.opportunity
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['opportunity'] = related_dict
            else:
                item_dict['opportunity'] = None
            if task_item.assigned_to:
                related_obj = task_item.assigned_to
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['assigned_to'] = related_dict
            else:
                item_dict['assigned_to'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Task).all()


@app.get("/task/count/", response_model=None, tags=["Task"])
def get_count_task(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Task entities"""
    count = database.query(Task).count()
    return {"count": count}


@app.get("/task/paginated/", response_model=None, tags=["Task"])
def get_paginated_task(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Task entities"""
    total = database.query(Task).count()
    task_list = database.query(Task).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": task_list
    }


@app.get("/task/search/", response_model=None, tags=["Task"])
def search_task(
    database: Session = Depends(get_db)
) -> list:
    """Search Task entities by attributes"""
    query = database.query(Task)


    results = query.all()
    return results


@app.get("/task/{task_id}/", response_model=None, tags=["Task"])
async def get_task(task_id: int, database: Session = Depends(get_db)) -> Task:
    db_task = database.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    response_data = {
        "task": db_task,
}
    return response_data



@app.post("/task/", response_model=None, tags=["Task"])
async def create_task(task_data: TaskCreate, database: Session = Depends(get_db)) -> Task:

    if task_data.contact :
        db_contact = database.query(Contact).filter(Contact.id == task_data.contact).first()
        if not db_contact:
            raise HTTPException(status_code=400, detail="Contact not found")
    if task_data.opportunity :
        db_opportunity = database.query(Opportunity).filter(Opportunity.id == task_data.opportunity).first()
        if not db_opportunity:
            raise HTTPException(status_code=400, detail="Opportunity not found")
    if task_data.assigned_to is not None:
        db_assigned_to = database.query(User).filter(User.id == task_data.assigned_to).first()
        if not db_assigned_to:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")

    db_task = Task(
        created_at=task_data.created_at,        due_date=task_data.due_date,        title=task_data.title,        id=task_data.id,        completed_at=task_data.completed_at,        description=task_data.description,        is_completed=task_data.is_completed,        contact_id=task_data.contact,        opportunity_id=task_data.opportunity,        assigned_to_id=task_data.assigned_to        )

    database.add(db_task)
    database.commit()
    database.refresh(db_task)




    return db_task


@app.post("/task/bulk/", response_model=None, tags=["Task"])
async def bulk_create_task(items: list[TaskCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Task entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.assigned_to:
                raise ValueError("User ID is required")

            db_task = Task(
                created_at=item_data.created_at,                due_date=item_data.due_date,                title=item_data.title,                id=item_data.id,                completed_at=item_data.completed_at,                description=item_data.description,                is_completed=item_data.is_completed,                contact_id=item_data.contact,                opportunity_id=item_data.opportunity,                assigned_to_id=item_data.assigned_to            )
            database.add(db_task)
            database.flush()  # Get ID without committing
            created_items.append(db_task.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Task entities"
    }


@app.delete("/task/bulk/", response_model=None, tags=["Task"])
async def bulk_delete_task(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Task entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_task = database.query(Task).filter(Task.id == item_id).first()
        if db_task:
            database.delete(db_task)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Task entities"
    }

@app.put("/task/{task_id}/", response_model=None, tags=["Task"])
async def update_task(task_id: int, task_data: TaskCreate, database: Session = Depends(get_db)) -> Task:
    db_task = database.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    setattr(db_task, 'created_at', task_data.created_at)
    setattr(db_task, 'due_date', task_data.due_date)
    setattr(db_task, 'title', task_data.title)
    setattr(db_task, 'id', task_data.id)
    setattr(db_task, 'completed_at', task_data.completed_at)
    setattr(db_task, 'description', task_data.description)
    setattr(db_task, 'is_completed', task_data.is_completed)
    if task_data.contact is not None:
        db_contact = database.query(Contact).filter(Contact.id == task_data.contact).first()
        if not db_contact:
            raise HTTPException(status_code=400, detail="Contact not found")
        setattr(db_task, 'contact_id', task_data.contact)
    else:
        setattr(db_task, 'contact_id', None)
    if task_data.opportunity is not None:
        db_opportunity = database.query(Opportunity).filter(Opportunity.id == task_data.opportunity).first()
        if not db_opportunity:
            raise HTTPException(status_code=400, detail="Opportunity not found")
        setattr(db_task, 'opportunity_id', task_data.opportunity)
    else:
        setattr(db_task, 'opportunity_id', None)
    if task_data.assigned_to is not None:
        db_assigned_to = database.query(User).filter(User.id == task_data.assigned_to).first()
        if not db_assigned_to:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_task, 'assigned_to_id', task_data.assigned_to)
    database.commit()
    database.refresh(db_task)

    return db_task


@app.delete("/task/{task_id}/", response_model=None, tags=["Task"])
async def delete_task(task_id: int, database: Session = Depends(get_db)):
    db_task = database.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    database.delete(db_task)
    database.commit()
    return db_task





############################################
#
#   EmailTemplate functions
#
############################################

@app.get("/emailtemplate/", response_model=None, tags=["EmailTemplate"])
def get_all_emailtemplate(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(EmailTemplate)
        query = query.options(joinedload(EmailTemplate.created_by))
        emailtemplate_list = query.all()

        # Serialize with relationships included
        result = []
        for emailtemplate_item in emailtemplate_list:
            item_dict = emailtemplate_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if emailtemplate_item.created_by:
                related_obj = emailtemplate_item.created_by
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['created_by'] = related_dict
            else:
                item_dict['created_by'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            generatedemail_list = database.query(GeneratedEmail).filter(GeneratedEmail.template_id == emailtemplate_item.id).all()
            item_dict['generated_emails'] = []
            for generatedemail_obj in generatedemail_list:
                generatedemail_dict = generatedemail_obj.__dict__.copy()
                generatedemail_dict.pop('_sa_instance_state', None)
                item_dict['generated_emails'].append(generatedemail_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(EmailTemplate).all()


@app.get("/emailtemplate/count/", response_model=None, tags=["EmailTemplate"])
def get_count_emailtemplate(database: Session = Depends(get_db)) -> dict:
    """Get the total count of EmailTemplate entities"""
    count = database.query(EmailTemplate).count()
    return {"count": count}


@app.get("/emailtemplate/paginated/", response_model=None, tags=["EmailTemplate"])
def get_paginated_emailtemplate(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of EmailTemplate entities"""
    total = database.query(EmailTemplate).count()
    emailtemplate_list = database.query(EmailTemplate).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": emailtemplate_list
        }

    result = []
    for emailtemplate_item in emailtemplate_list:
        generated_emails_ids = database.query(GeneratedEmail.id).filter(GeneratedEmail.template_id == emailtemplate_item.id).all()
        item_data = {
            "emailtemplate": emailtemplate_item,
            "generated_emails_ids": [x[0] for x in generated_emails_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/emailtemplate/search/", response_model=None, tags=["EmailTemplate"])
def search_emailtemplate(
    database: Session = Depends(get_db)
) -> list:
    """Search EmailTemplate entities by attributes"""
    query = database.query(EmailTemplate)


    results = query.all()
    return results


@app.get("/emailtemplate/{emailtemplate_id}/", response_model=None, tags=["EmailTemplate"])
async def get_emailtemplate(emailtemplate_id: int, database: Session = Depends(get_db)) -> EmailTemplate:
    db_emailtemplate = database.query(EmailTemplate).filter(EmailTemplate.id == emailtemplate_id).first()
    if db_emailtemplate is None:
        raise HTTPException(status_code=404, detail="EmailTemplate not found")

    generated_emails_ids = database.query(GeneratedEmail.id).filter(GeneratedEmail.template_id == db_emailtemplate.id).all()
    response_data = {
        "emailtemplate": db_emailtemplate,
        "generated_emails_ids": [x[0] for x in generated_emails_ids]}
    return response_data



@app.post("/emailtemplate/", response_model=None, tags=["EmailTemplate"])
async def create_emailtemplate(emailtemplate_data: EmailTemplateCreate, database: Session = Depends(get_db)) -> EmailTemplate:

    if emailtemplate_data.created_by is not None:
        db_created_by = database.query(User).filter(User.id == emailtemplate_data.created_by).first()
        if not db_created_by:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")

    db_emailtemplate = EmailTemplate(
        category=emailtemplate_data.category,        created_at=emailtemplate_data.created_at,        body_template=emailtemplate_data.body_template,        name=emailtemplate_data.name,        id=emailtemplate_data.id,        subject_template=emailtemplate_data.subject_template,        created_by_id=emailtemplate_data.created_by        )

    database.add(db_emailtemplate)
    database.commit()
    database.refresh(db_emailtemplate)

    if emailtemplate_data.generated_emails:
        # Validate that all GeneratedEmail IDs exist
        for generatedemail_id in emailtemplate_data.generated_emails:
            db_generatedemail = database.query(GeneratedEmail).filter(GeneratedEmail.id == generatedemail_id).first()
            if not db_generatedemail:
                raise HTTPException(status_code=400, detail=f"GeneratedEmail with id {generatedemail_id} not found")

        # Update the related entities with the new foreign key
        database.query(GeneratedEmail).filter(GeneratedEmail.id.in_(emailtemplate_data.generated_emails)).update(
            {GeneratedEmail.template_id: db_emailtemplate.id}, synchronize_session=False
        )
        database.commit()



    generated_emails_ids = database.query(GeneratedEmail.id).filter(GeneratedEmail.template_id == db_emailtemplate.id).all()
    response_data = {
        "emailtemplate": db_emailtemplate,
        "generated_emails_ids": [x[0] for x in generated_emails_ids]    }
    return response_data


@app.post("/emailtemplate/bulk/", response_model=None, tags=["EmailTemplate"])
async def bulk_create_emailtemplate(items: list[EmailTemplateCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple EmailTemplate entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.created_by:
                raise ValueError("User ID is required")

            db_emailtemplate = EmailTemplate(
                category=item_data.category,                created_at=item_data.created_at,                body_template=item_data.body_template,                name=item_data.name,                id=item_data.id,                subject_template=item_data.subject_template,                created_by_id=item_data.created_by            )
            database.add(db_emailtemplate)
            database.flush()  # Get ID without committing
            created_items.append(db_emailtemplate.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} EmailTemplate entities"
    }


@app.delete("/emailtemplate/bulk/", response_model=None, tags=["EmailTemplate"])
async def bulk_delete_emailtemplate(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple EmailTemplate entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_emailtemplate = database.query(EmailTemplate).filter(EmailTemplate.id == item_id).first()
        if db_emailtemplate:
            database.delete(db_emailtemplate)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} EmailTemplate entities"
    }

@app.put("/emailtemplate/{emailtemplate_id}/", response_model=None, tags=["EmailTemplate"])
async def update_emailtemplate(emailtemplate_id: int, emailtemplate_data: EmailTemplateCreate, database: Session = Depends(get_db)) -> EmailTemplate:
    db_emailtemplate = database.query(EmailTemplate).filter(EmailTemplate.id == emailtemplate_id).first()
    if db_emailtemplate is None:
        raise HTTPException(status_code=404, detail="EmailTemplate not found")

    setattr(db_emailtemplate, 'category', emailtemplate_data.category)
    setattr(db_emailtemplate, 'created_at', emailtemplate_data.created_at)
    setattr(db_emailtemplate, 'body_template', emailtemplate_data.body_template)
    setattr(db_emailtemplate, 'name', emailtemplate_data.name)
    setattr(db_emailtemplate, 'id', emailtemplate_data.id)
    setattr(db_emailtemplate, 'subject_template', emailtemplate_data.subject_template)
    if emailtemplate_data.created_by is not None:
        db_created_by = database.query(User).filter(User.id == emailtemplate_data.created_by).first()
        if not db_created_by:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_emailtemplate, 'created_by_id', emailtemplate_data.created_by)
    if emailtemplate_data.generated_emails is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(GeneratedEmail).filter(GeneratedEmail.template_id == db_emailtemplate.id).update(
            {GeneratedEmail.template_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if emailtemplate_data.generated_emails:
            # Validate that all IDs exist
            for generatedemail_id in emailtemplate_data.generated_emails:
                db_generatedemail = database.query(GeneratedEmail).filter(GeneratedEmail.id == generatedemail_id).first()
                if not db_generatedemail:
                    raise HTTPException(status_code=400, detail=f"GeneratedEmail with id {generatedemail_id} not found")

            # Update the related entities with the new foreign key
            database.query(GeneratedEmail).filter(GeneratedEmail.id.in_(emailtemplate_data.generated_emails)).update(
                {GeneratedEmail.template_id: db_emailtemplate.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_emailtemplate)

    generated_emails_ids = database.query(GeneratedEmail.id).filter(GeneratedEmail.template_id == db_emailtemplate.id).all()
    response_data = {
        "emailtemplate": db_emailtemplate,
        "generated_emails_ids": [x[0] for x in generated_emails_ids]    }
    return response_data


@app.delete("/emailtemplate/{emailtemplate_id}/", response_model=None, tags=["EmailTemplate"])
async def delete_emailtemplate(emailtemplate_id: int, database: Session = Depends(get_db)):
    db_emailtemplate = database.query(EmailTemplate).filter(EmailTemplate.id == emailtemplate_id).first()
    if db_emailtemplate is None:
        raise HTTPException(status_code=404, detail="EmailTemplate not found")
    database.delete(db_emailtemplate)
    database.commit()
    return db_emailtemplate





############################################
#
#   GeneratedEmail functions
#
############################################

@app.get("/generatedemail/", response_model=None, tags=["GeneratedEmail"])
def get_all_generatedemail(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(GeneratedEmail)
        query = query.options(joinedload(GeneratedEmail.template))
        query = query.options(joinedload(GeneratedEmail.created_by))
        query = query.options(joinedload(GeneratedEmail.contact))
        generatedemail_list = query.all()

        # Serialize with relationships included
        result = []
        for generatedemail_item in generatedemail_list:
            item_dict = generatedemail_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if generatedemail_item.template:
                related_obj = generatedemail_item.template
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['template'] = related_dict
            else:
                item_dict['template'] = None
            if generatedemail_item.created_by:
                related_obj = generatedemail_item.created_by
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['created_by'] = related_dict
            else:
                item_dict['created_by'] = None
            if generatedemail_item.contact:
                related_obj = generatedemail_item.contact
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['contact'] = related_dict
            else:
                item_dict['contact'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(GeneratedEmail).all()


@app.get("/generatedemail/count/", response_model=None, tags=["GeneratedEmail"])
def get_count_generatedemail(database: Session = Depends(get_db)) -> dict:
    """Get the total count of GeneratedEmail entities"""
    count = database.query(GeneratedEmail).count()
    return {"count": count}


@app.get("/generatedemail/paginated/", response_model=None, tags=["GeneratedEmail"])
def get_paginated_generatedemail(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of GeneratedEmail entities"""
    total = database.query(GeneratedEmail).count()
    generatedemail_list = database.query(GeneratedEmail).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": generatedemail_list
    }


@app.get("/generatedemail/search/", response_model=None, tags=["GeneratedEmail"])
def search_generatedemail(
    database: Session = Depends(get_db)
) -> list:
    """Search GeneratedEmail entities by attributes"""
    query = database.query(GeneratedEmail)


    results = query.all()
    return results


@app.get("/generatedemail/{generatedemail_id}/", response_model=None, tags=["GeneratedEmail"])
async def get_generatedemail(generatedemail_id: int, database: Session = Depends(get_db)) -> GeneratedEmail:
    db_generatedemail = database.query(GeneratedEmail).filter(GeneratedEmail.id == generatedemail_id).first()
    if db_generatedemail is None:
        raise HTTPException(status_code=404, detail="GeneratedEmail not found")

    response_data = {
        "generatedemail": db_generatedemail,
}
    return response_data



@app.post("/generatedemail/", response_model=None, tags=["GeneratedEmail"])
async def create_generatedemail(generatedemail_data: GeneratedEmailCreate, database: Session = Depends(get_db)) -> GeneratedEmail:

    if generatedemail_data.template :
        db_template = database.query(EmailTemplate).filter(EmailTemplate.id == generatedemail_data.template).first()
        if not db_template:
            raise HTTPException(status_code=400, detail="EmailTemplate not found")
    if generatedemail_data.created_by is not None:
        db_created_by = database.query(User).filter(User.id == generatedemail_data.created_by).first()
        if not db_created_by:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")
    if generatedemail_data.contact is not None:
        db_contact = database.query(Contact).filter(Contact.id == generatedemail_data.contact).first()
        if not db_contact:
            raise HTTPException(status_code=400, detail="Contact not found")
    else:
        raise HTTPException(status_code=400, detail="Contact ID is required")

    db_generatedemail = GeneratedEmail(
        created_at=generatedemail_data.created_at,        subject=generatedemail_data.subject,        is_sent=generatedemail_data.is_sent,        sent_at=generatedemail_data.sent_at,        id=generatedemail_data.id,        body=generatedemail_data.body,        template_id=generatedemail_data.template,        created_by_id=generatedemail_data.created_by,        contact_id=generatedemail_data.contact        )

    database.add(db_generatedemail)
    database.commit()
    database.refresh(db_generatedemail)




    return db_generatedemail


@app.post("/generatedemail/bulk/", response_model=None, tags=["GeneratedEmail"])
async def bulk_create_generatedemail(items: list[GeneratedEmailCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple GeneratedEmail entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.created_by:
                raise ValueError("User ID is required")
            if not item_data.contact:
                raise ValueError("Contact ID is required")

            db_generatedemail = GeneratedEmail(
                created_at=item_data.created_at,                subject=item_data.subject,                is_sent=item_data.is_sent,                sent_at=item_data.sent_at,                id=item_data.id,                body=item_data.body,                template_id=item_data.template,                created_by_id=item_data.created_by,                contact_id=item_data.contact            )
            database.add(db_generatedemail)
            database.flush()  # Get ID without committing
            created_items.append(db_generatedemail.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} GeneratedEmail entities"
    }


@app.delete("/generatedemail/bulk/", response_model=None, tags=["GeneratedEmail"])
async def bulk_delete_generatedemail(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple GeneratedEmail entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_generatedemail = database.query(GeneratedEmail).filter(GeneratedEmail.id == item_id).first()
        if db_generatedemail:
            database.delete(db_generatedemail)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} GeneratedEmail entities"
    }

@app.put("/generatedemail/{generatedemail_id}/", response_model=None, tags=["GeneratedEmail"])
async def update_generatedemail(generatedemail_id: int, generatedemail_data: GeneratedEmailCreate, database: Session = Depends(get_db)) -> GeneratedEmail:
    db_generatedemail = database.query(GeneratedEmail).filter(GeneratedEmail.id == generatedemail_id).first()
    if db_generatedemail is None:
        raise HTTPException(status_code=404, detail="GeneratedEmail not found")

    setattr(db_generatedemail, 'created_at', generatedemail_data.created_at)
    setattr(db_generatedemail, 'subject', generatedemail_data.subject)
    setattr(db_generatedemail, 'is_sent', generatedemail_data.is_sent)
    setattr(db_generatedemail, 'sent_at', generatedemail_data.sent_at)
    setattr(db_generatedemail, 'id', generatedemail_data.id)
    setattr(db_generatedemail, 'body', generatedemail_data.body)
    if generatedemail_data.template is not None:
        db_template = database.query(EmailTemplate).filter(EmailTemplate.id == generatedemail_data.template).first()
        if not db_template:
            raise HTTPException(status_code=400, detail="EmailTemplate not found")
        setattr(db_generatedemail, 'template_id', generatedemail_data.template)
    else:
        setattr(db_generatedemail, 'template_id', None)
    if generatedemail_data.created_by is not None:
        db_created_by = database.query(User).filter(User.id == generatedemail_data.created_by).first()
        if not db_created_by:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_generatedemail, 'created_by_id', generatedemail_data.created_by)
    if generatedemail_data.contact is not None:
        db_contact = database.query(Contact).filter(Contact.id == generatedemail_data.contact).first()
        if not db_contact:
            raise HTTPException(status_code=400, detail="Contact not found")
        setattr(db_generatedemail, 'contact_id', generatedemail_data.contact)
    database.commit()
    database.refresh(db_generatedemail)

    return db_generatedemail


@app.delete("/generatedemail/{generatedemail_id}/", response_model=None, tags=["GeneratedEmail"])
async def delete_generatedemail(generatedemail_id: int, database: Session = Depends(get_db)):
    db_generatedemail = database.query(GeneratedEmail).filter(GeneratedEmail.id == generatedemail_id).first()
    if db_generatedemail is None:
        raise HTTPException(status_code=404, detail="GeneratedEmail not found")
    database.delete(db_generatedemail)
    database.commit()
    return db_generatedemail





############################################
#
#   EnrichmentLog functions
#
############################################

@app.get("/enrichmentlog/", response_model=None, tags=["EnrichmentLog"])
def get_all_enrichmentlog(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(EnrichmentLog)
        query = query.options(joinedload(EnrichmentLog.contact))
        enrichmentlog_list = query.all()

        # Serialize with relationships included
        result = []
        for enrichmentlog_item in enrichmentlog_list:
            item_dict = enrichmentlog_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if enrichmentlog_item.contact:
                related_obj = enrichmentlog_item.contact
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['contact'] = related_dict
            else:
                item_dict['contact'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(EnrichmentLog).all()


@app.get("/enrichmentlog/count/", response_model=None, tags=["EnrichmentLog"])
def get_count_enrichmentlog(database: Session = Depends(get_db)) -> dict:
    """Get the total count of EnrichmentLog entities"""
    count = database.query(EnrichmentLog).count()
    return {"count": count}


@app.get("/enrichmentlog/paginated/", response_model=None, tags=["EnrichmentLog"])
def get_paginated_enrichmentlog(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of EnrichmentLog entities"""
    total = database.query(EnrichmentLog).count()
    enrichmentlog_list = database.query(EnrichmentLog).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": enrichmentlog_list
    }


@app.get("/enrichmentlog/search/", response_model=None, tags=["EnrichmentLog"])
def search_enrichmentlog(
    database: Session = Depends(get_db)
) -> list:
    """Search EnrichmentLog entities by attributes"""
    query = database.query(EnrichmentLog)


    results = query.all()
    return results


@app.get("/enrichmentlog/{enrichmentlog_id}/", response_model=None, tags=["EnrichmentLog"])
async def get_enrichmentlog(enrichmentlog_id: int, database: Session = Depends(get_db)) -> EnrichmentLog:
    db_enrichmentlog = database.query(EnrichmentLog).filter(EnrichmentLog.id == enrichmentlog_id).first()
    if db_enrichmentlog is None:
        raise HTTPException(status_code=404, detail="EnrichmentLog not found")

    response_data = {
        "enrichmentlog": db_enrichmentlog,
}
    return response_data



@app.post("/enrichmentlog/", response_model=None, tags=["EnrichmentLog"])
async def create_enrichmentlog(enrichmentlog_data: EnrichmentLogCreate, database: Session = Depends(get_db)) -> EnrichmentLog:

    if enrichmentlog_data.contact is not None:
        db_contact = database.query(Contact).filter(Contact.id == enrichmentlog_data.contact).first()
        if not db_contact:
            raise HTTPException(status_code=400, detail="Contact not found")
    else:
        raise HTTPException(status_code=400, detail="Contact ID is required")

    db_enrichmentlog = EnrichmentLog(
        is_successful=enrichmentlog_data.is_successful,        id=enrichmentlog_data.id,        enriched_at=enrichmentlog_data.enriched_at,        error_message=enrichmentlog_data.error_message,        linkedin_url=enrichmentlog_data.linkedin_url,        contact_id=enrichmentlog_data.contact        )

    database.add(db_enrichmentlog)
    database.commit()
    database.refresh(db_enrichmentlog)




    return db_enrichmentlog


@app.post("/enrichmentlog/bulk/", response_model=None, tags=["EnrichmentLog"])
async def bulk_create_enrichmentlog(items: list[EnrichmentLogCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple EnrichmentLog entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.contact:
                raise ValueError("Contact ID is required")

            db_enrichmentlog = EnrichmentLog(
                is_successful=item_data.is_successful,                id=item_data.id,                enriched_at=item_data.enriched_at,                error_message=item_data.error_message,                linkedin_url=item_data.linkedin_url,                contact_id=item_data.contact            )
            database.add(db_enrichmentlog)
            database.flush()  # Get ID without committing
            created_items.append(db_enrichmentlog.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} EnrichmentLog entities"
    }


@app.delete("/enrichmentlog/bulk/", response_model=None, tags=["EnrichmentLog"])
async def bulk_delete_enrichmentlog(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple EnrichmentLog entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_enrichmentlog = database.query(EnrichmentLog).filter(EnrichmentLog.id == item_id).first()
        if db_enrichmentlog:
            database.delete(db_enrichmentlog)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} EnrichmentLog entities"
    }

@app.put("/enrichmentlog/{enrichmentlog_id}/", response_model=None, tags=["EnrichmentLog"])
async def update_enrichmentlog(enrichmentlog_id: int, enrichmentlog_data: EnrichmentLogCreate, database: Session = Depends(get_db)) -> EnrichmentLog:
    db_enrichmentlog = database.query(EnrichmentLog).filter(EnrichmentLog.id == enrichmentlog_id).first()
    if db_enrichmentlog is None:
        raise HTTPException(status_code=404, detail="EnrichmentLog not found")

    setattr(db_enrichmentlog, 'is_successful', enrichmentlog_data.is_successful)
    setattr(db_enrichmentlog, 'id', enrichmentlog_data.id)
    setattr(db_enrichmentlog, 'enriched_at', enrichmentlog_data.enriched_at)
    setattr(db_enrichmentlog, 'error_message', enrichmentlog_data.error_message)
    setattr(db_enrichmentlog, 'linkedin_url', enrichmentlog_data.linkedin_url)
    if enrichmentlog_data.contact is not None:
        db_contact = database.query(Contact).filter(Contact.id == enrichmentlog_data.contact).first()
        if not db_contact:
            raise HTTPException(status_code=400, detail="Contact not found")
        setattr(db_enrichmentlog, 'contact_id', enrichmentlog_data.contact)
    database.commit()
    database.refresh(db_enrichmentlog)

    return db_enrichmentlog


@app.delete("/enrichmentlog/{enrichmentlog_id}/", response_model=None, tags=["EnrichmentLog"])
async def delete_enrichmentlog(enrichmentlog_id: int, database: Session = Depends(get_db)):
    db_enrichmentlog = database.query(EnrichmentLog).filter(EnrichmentLog.id == enrichmentlog_id).first()
    if db_enrichmentlog is None:
        raise HTTPException(status_code=404, detail="EnrichmentLog not found")
    database.delete(db_enrichmentlog)
    database.commit()
    return db_enrichmentlog





############################################
#
#   ScoreHistory functions
#
############################################

@app.get("/scorehistory/", response_model=None, tags=["ScoreHistory"])
def get_all_scorehistory(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ScoreHistory)
        query = query.options(joinedload(ScoreHistory.contact))
        scorehistory_list = query.all()

        # Serialize with relationships included
        result = []
        for scorehistory_item in scorehistory_list:
            item_dict = scorehistory_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if scorehistory_item.contact:
                related_obj = scorehistory_item.contact
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['contact'] = related_dict
            else:
                item_dict['contact'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ScoreHistory).all()


@app.get("/scorehistory/count/", response_model=None, tags=["ScoreHistory"])
def get_count_scorehistory(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ScoreHistory entities"""
    count = database.query(ScoreHistory).count()
    return {"count": count}


@app.get("/scorehistory/paginated/", response_model=None, tags=["ScoreHistory"])
def get_paginated_scorehistory(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ScoreHistory entities"""
    total = database.query(ScoreHistory).count()
    scorehistory_list = database.query(ScoreHistory).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": scorehistory_list
    }


@app.get("/scorehistory/search/", response_model=None, tags=["ScoreHistory"])
def search_scorehistory(
    database: Session = Depends(get_db)
) -> list:
    """Search ScoreHistory entities by attributes"""
    query = database.query(ScoreHistory)


    results = query.all()
    return results


@app.get("/scorehistory/{scorehistory_id}/", response_model=None, tags=["ScoreHistory"])
async def get_scorehistory(scorehistory_id: int, database: Session = Depends(get_db)) -> ScoreHistory:
    db_scorehistory = database.query(ScoreHistory).filter(ScoreHistory.id == scorehistory_id).first()
    if db_scorehistory is None:
        raise HTTPException(status_code=404, detail="ScoreHistory not found")

    response_data = {
        "scorehistory": db_scorehistory,
}
    return response_data



@app.post("/scorehistory/", response_model=None, tags=["ScoreHistory"])
async def create_scorehistory(scorehistory_data: ScoreHistoryCreate, database: Session = Depends(get_db)) -> ScoreHistory:

    if scorehistory_data.contact is not None:
        db_contact = database.query(Contact).filter(Contact.id == scorehistory_data.contact).first()
        if not db_contact:
            raise HTTPException(status_code=400, detail="Contact not found")
    else:
        raise HTTPException(status_code=400, detail="Contact ID is required")

    db_scorehistory = ScoreHistory(
        reason=scorehistory_data.reason,        id=scorehistory_data.id,        new_score=scorehistory_data.new_score,        calculated_at=scorehistory_data.calculated_at,        old_score=scorehistory_data.old_score,        contact_id=scorehistory_data.contact        )

    database.add(db_scorehistory)
    database.commit()
    database.refresh(db_scorehistory)




    return db_scorehistory


@app.post("/scorehistory/bulk/", response_model=None, tags=["ScoreHistory"])
async def bulk_create_scorehistory(items: list[ScoreHistoryCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ScoreHistory entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.contact:
                raise ValueError("Contact ID is required")

            db_scorehistory = ScoreHistory(
                reason=item_data.reason,                id=item_data.id,                new_score=item_data.new_score,                calculated_at=item_data.calculated_at,                old_score=item_data.old_score,                contact_id=item_data.contact            )
            database.add(db_scorehistory)
            database.flush()  # Get ID without committing
            created_items.append(db_scorehistory.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ScoreHistory entities"
    }


@app.delete("/scorehistory/bulk/", response_model=None, tags=["ScoreHistory"])
async def bulk_delete_scorehistory(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ScoreHistory entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_scorehistory = database.query(ScoreHistory).filter(ScoreHistory.id == item_id).first()
        if db_scorehistory:
            database.delete(db_scorehistory)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ScoreHistory entities"
    }

@app.put("/scorehistory/{scorehistory_id}/", response_model=None, tags=["ScoreHistory"])
async def update_scorehistory(scorehistory_id: int, scorehistory_data: ScoreHistoryCreate, database: Session = Depends(get_db)) -> ScoreHistory:
    db_scorehistory = database.query(ScoreHistory).filter(ScoreHistory.id == scorehistory_id).first()
    if db_scorehistory is None:
        raise HTTPException(status_code=404, detail="ScoreHistory not found")

    setattr(db_scorehistory, 'reason', scorehistory_data.reason)
    setattr(db_scorehistory, 'id', scorehistory_data.id)
    setattr(db_scorehistory, 'new_score', scorehistory_data.new_score)
    setattr(db_scorehistory, 'calculated_at', scorehistory_data.calculated_at)
    setattr(db_scorehistory, 'old_score', scorehistory_data.old_score)
    if scorehistory_data.contact is not None:
        db_contact = database.query(Contact).filter(Contact.id == scorehistory_data.contact).first()
        if not db_contact:
            raise HTTPException(status_code=400, detail="Contact not found")
        setattr(db_scorehistory, 'contact_id', scorehistory_data.contact)
    database.commit()
    database.refresh(db_scorehistory)

    return db_scorehistory


@app.delete("/scorehistory/{scorehistory_id}/", response_model=None, tags=["ScoreHistory"])
async def delete_scorehistory(scorehistory_id: int, database: Session = Depends(get_db)):
    db_scorehistory = database.query(ScoreHistory).filter(ScoreHistory.id == scorehistory_id).first()
    if db_scorehistory is None:
        raise HTTPException(status_code=404, detail="ScoreHistory not found")
    database.delete(db_scorehistory)
    database.commit()
    return db_scorehistory





############################################
#
#   User functions
#
############################################

@app.get("/user/", response_model=None, tags=["User"])
def get_all_user(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(User)
        user_list = query.all()

        # Serialize with relationships included
        result = []
        for user_item in user_list:
            item_dict = user_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            contact_list = database.query(Contact).filter(Contact.created_by_id == user_item.id).all()
            item_dict['created_contacts'] = []
            for contact_obj in contact_list:
                contact_dict = contact_obj.__dict__.copy()
                contact_dict.pop('_sa_instance_state', None)
                item_dict['created_contacts'].append(contact_dict)
            emailtemplate_list = database.query(EmailTemplate).filter(EmailTemplate.created_by_id == user_item.id).all()
            item_dict['email_templates'] = []
            for emailtemplate_obj in emailtemplate_list:
                emailtemplate_dict = emailtemplate_obj.__dict__.copy()
                emailtemplate_dict.pop('_sa_instance_state', None)
                item_dict['email_templates'].append(emailtemplate_dict)
            company_list = database.query(Company).filter(Company.created_by_id == user_item.id).all()
            item_dict['created_companies'] = []
            for company_obj in company_list:
                company_dict = company_obj.__dict__.copy()
                company_dict.pop('_sa_instance_state', None)
                item_dict['created_companies'].append(company_dict)
            generatedemail_list = database.query(GeneratedEmail).filter(GeneratedEmail.created_by_id == user_item.id).all()
            item_dict['generated_emails'] = []
            for generatedemail_obj in generatedemail_list:
                generatedemail_dict = generatedemail_obj.__dict__.copy()
                generatedemail_dict.pop('_sa_instance_state', None)
                item_dict['generated_emails'].append(generatedemail_dict)
            opportunity_list = database.query(Opportunity).filter(Opportunity.owner_id == user_item.id).all()
            item_dict['owned_opportunities'] = []
            for opportunity_obj in opportunity_list:
                opportunity_dict = opportunity_obj.__dict__.copy()
                opportunity_dict.pop('_sa_instance_state', None)
                item_dict['owned_opportunities'].append(opportunity_dict)
            interaction_list = database.query(Interaction).filter(Interaction.performed_by_id == user_item.id).all()
            item_dict['interactions'] = []
            for interaction_obj in interaction_list:
                interaction_dict = interaction_obj.__dict__.copy()
                interaction_dict.pop('_sa_instance_state', None)
                item_dict['interactions'].append(interaction_dict)
            task_list = database.query(Task).filter(Task.assigned_to_id == user_item.id).all()
            item_dict['tasks'] = []
            for task_obj in task_list:
                task_dict = task_obj.__dict__.copy()
                task_dict.pop('_sa_instance_state', None)
                item_dict['tasks'].append(task_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(User).all()


@app.get("/user/count/", response_model=None, tags=["User"])
def get_count_user(database: Session = Depends(get_db)) -> dict:
    """Get the total count of User entities"""
    count = database.query(User).count()
    return {"count": count}


@app.get("/user/paginated/", response_model=None, tags=["User"])
def get_paginated_user(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of User entities"""
    total = database.query(User).count()
    user_list = database.query(User).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": user_list
        }

    result = []
    for user_item in user_list:
        created_contacts_ids = database.query(Contact.id).filter(Contact.created_by_id == user_item.id).all()
        email_templates_ids = database.query(EmailTemplate.id).filter(EmailTemplate.created_by_id == user_item.id).all()
        created_companies_ids = database.query(Company.id).filter(Company.created_by_id == user_item.id).all()
        generated_emails_ids = database.query(GeneratedEmail.id).filter(GeneratedEmail.created_by_id == user_item.id).all()
        owned_opportunities_ids = database.query(Opportunity.id).filter(Opportunity.owner_id == user_item.id).all()
        interactions_ids = database.query(Interaction.id).filter(Interaction.performed_by_id == user_item.id).all()
        tasks_ids = database.query(Task.id).filter(Task.assigned_to_id == user_item.id).all()
        item_data = {
            "user": user_item,
            "created_contacts_ids": [x[0] for x in created_contacts_ids],            "email_templates_ids": [x[0] for x in email_templates_ids],            "created_companies_ids": [x[0] for x in created_companies_ids],            "generated_emails_ids": [x[0] for x in generated_emails_ids],            "owned_opportunities_ids": [x[0] for x in owned_opportunities_ids],            "interactions_ids": [x[0] for x in interactions_ids],            "tasks_ids": [x[0] for x in tasks_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/user/search/", response_model=None, tags=["User"])
def search_user(
    database: Session = Depends(get_db)
) -> list:
    """Search User entities by attributes"""
    query = database.query(User)


    results = query.all()
    return results


@app.get("/user/{user_id}/", response_model=None, tags=["User"])
async def get_user(user_id: int, database: Session = Depends(get_db)) -> User:
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    created_contacts_ids = database.query(Contact.id).filter(Contact.created_by_id == db_user.id).all()
    email_templates_ids = database.query(EmailTemplate.id).filter(EmailTemplate.created_by_id == db_user.id).all()
    created_companies_ids = database.query(Company.id).filter(Company.created_by_id == db_user.id).all()
    generated_emails_ids = database.query(GeneratedEmail.id).filter(GeneratedEmail.created_by_id == db_user.id).all()
    owned_opportunities_ids = database.query(Opportunity.id).filter(Opportunity.owner_id == db_user.id).all()
    interactions_ids = database.query(Interaction.id).filter(Interaction.performed_by_id == db_user.id).all()
    tasks_ids = database.query(Task.id).filter(Task.assigned_to_id == db_user.id).all()
    response_data = {
        "user": db_user,
        "created_contacts_ids": [x[0] for x in created_contacts_ids],        "email_templates_ids": [x[0] for x in email_templates_ids],        "created_companies_ids": [x[0] for x in created_companies_ids],        "generated_emails_ids": [x[0] for x in generated_emails_ids],        "owned_opportunities_ids": [x[0] for x in owned_opportunities_ids],        "interactions_ids": [x[0] for x in interactions_ids],        "tasks_ids": [x[0] for x in tasks_ids]}
    return response_data



@app.post("/user/", response_model=None, tags=["User"])
async def create_user(user_data: UserCreate, database: Session = Depends(get_db)) -> User:


    db_user = User(
        created_at=user_data.created_at,        last_name=user_data.last_name,        password_hash=user_data.password_hash,        email=user_data.email,        first_name=user_data.first_name,        is_active=user_data.is_active,        id=user_data.id,        role=user_data.role.value,        last_login=user_data.last_login        )

    database.add(db_user)
    database.commit()
    database.refresh(db_user)

    if user_data.created_contacts:
        # Validate that all Contact IDs exist
        for contact_id in user_data.created_contacts:
            db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
            if not db_contact:
                raise HTTPException(status_code=400, detail=f"Contact with id {contact_id} not found")

        # Update the related entities with the new foreign key
        database.query(Contact).filter(Contact.id.in_(user_data.created_contacts)).update(
            {Contact.created_by_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.email_templates:
        # Validate that all EmailTemplate IDs exist
        for emailtemplate_id in user_data.email_templates:
            db_emailtemplate = database.query(EmailTemplate).filter(EmailTemplate.id == emailtemplate_id).first()
            if not db_emailtemplate:
                raise HTTPException(status_code=400, detail=f"EmailTemplate with id {emailtemplate_id} not found")

        # Update the related entities with the new foreign key
        database.query(EmailTemplate).filter(EmailTemplate.id.in_(user_data.email_templates)).update(
            {EmailTemplate.created_by_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.created_companies:
        # Validate that all Company IDs exist
        for company_id in user_data.created_companies:
            db_company = database.query(Company).filter(Company.id == company_id).first()
            if not db_company:
                raise HTTPException(status_code=400, detail=f"Company with id {company_id} not found")

        # Update the related entities with the new foreign key
        database.query(Company).filter(Company.id.in_(user_data.created_companies)).update(
            {Company.created_by_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.generated_emails:
        # Validate that all GeneratedEmail IDs exist
        for generatedemail_id in user_data.generated_emails:
            db_generatedemail = database.query(GeneratedEmail).filter(GeneratedEmail.id == generatedemail_id).first()
            if not db_generatedemail:
                raise HTTPException(status_code=400, detail=f"GeneratedEmail with id {generatedemail_id} not found")

        # Update the related entities with the new foreign key
        database.query(GeneratedEmail).filter(GeneratedEmail.id.in_(user_data.generated_emails)).update(
            {GeneratedEmail.created_by_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.owned_opportunities:
        # Validate that all Opportunity IDs exist
        for opportunity_id in user_data.owned_opportunities:
            db_opportunity = database.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
            if not db_opportunity:
                raise HTTPException(status_code=400, detail=f"Opportunity with id {opportunity_id} not found")

        # Update the related entities with the new foreign key
        database.query(Opportunity).filter(Opportunity.id.in_(user_data.owned_opportunities)).update(
            {Opportunity.owner_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.interactions:
        # Validate that all Interaction IDs exist
        for interaction_id in user_data.interactions:
            db_interaction = database.query(Interaction).filter(Interaction.id == interaction_id).first()
            if not db_interaction:
                raise HTTPException(status_code=400, detail=f"Interaction with id {interaction_id} not found")

        # Update the related entities with the new foreign key
        database.query(Interaction).filter(Interaction.id.in_(user_data.interactions)).update(
            {Interaction.performed_by_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.tasks:
        # Validate that all Task IDs exist
        for task_id in user_data.tasks:
            db_task = database.query(Task).filter(Task.id == task_id).first()
            if not db_task:
                raise HTTPException(status_code=400, detail=f"Task with id {task_id} not found")

        # Update the related entities with the new foreign key
        database.query(Task).filter(Task.id.in_(user_data.tasks)).update(
            {Task.assigned_to_id: db_user.id}, synchronize_session=False
        )
        database.commit()



    created_contacts_ids = database.query(Contact.id).filter(Contact.created_by_id == db_user.id).all()
    email_templates_ids = database.query(EmailTemplate.id).filter(EmailTemplate.created_by_id == db_user.id).all()
    created_companies_ids = database.query(Company.id).filter(Company.created_by_id == db_user.id).all()
    generated_emails_ids = database.query(GeneratedEmail.id).filter(GeneratedEmail.created_by_id == db_user.id).all()
    owned_opportunities_ids = database.query(Opportunity.id).filter(Opportunity.owner_id == db_user.id).all()
    interactions_ids = database.query(Interaction.id).filter(Interaction.performed_by_id == db_user.id).all()
    tasks_ids = database.query(Task.id).filter(Task.assigned_to_id == db_user.id).all()
    response_data = {
        "user": db_user,
        "created_contacts_ids": [x[0] for x in created_contacts_ids],        "email_templates_ids": [x[0] for x in email_templates_ids],        "created_companies_ids": [x[0] for x in created_companies_ids],        "generated_emails_ids": [x[0] for x in generated_emails_ids],        "owned_opportunities_ids": [x[0] for x in owned_opportunities_ids],        "interactions_ids": [x[0] for x in interactions_ids],        "tasks_ids": [x[0] for x in tasks_ids]    }
    return response_data


@app.post("/user/bulk/", response_model=None, tags=["User"])
async def bulk_create_user(items: list[UserCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple User entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_user = User(
                created_at=item_data.created_at,                last_name=item_data.last_name,                password_hash=item_data.password_hash,                email=item_data.email,                first_name=item_data.first_name,                is_active=item_data.is_active,                id=item_data.id,                role=item_data.role.value,                last_login=item_data.last_login            )
            database.add(db_user)
            database.flush()  # Get ID without committing
            created_items.append(db_user.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} User entities"
    }


@app.delete("/user/bulk/", response_model=None, tags=["User"])
async def bulk_delete_user(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple User entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_user = database.query(User).filter(User.id == item_id).first()
        if db_user:
            database.delete(db_user)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} User entities"
    }

@app.put("/user/{user_id}/", response_model=None, tags=["User"])
async def update_user(user_id: int, user_data: UserCreate, database: Session = Depends(get_db)) -> User:
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    setattr(db_user, 'created_at', user_data.created_at)
    setattr(db_user, 'last_name', user_data.last_name)
    setattr(db_user, 'password_hash', user_data.password_hash)
    setattr(db_user, 'email', user_data.email)
    setattr(db_user, 'first_name', user_data.first_name)
    setattr(db_user, 'is_active', user_data.is_active)
    setattr(db_user, 'id', user_data.id)
    setattr(db_user, 'role', user_data.role.value)
    setattr(db_user, 'last_login', user_data.last_login)
    if user_data.created_contacts is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Contact).filter(Contact.created_by_id == db_user.id).update(
            {Contact.created_by_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.created_contacts:
            # Validate that all IDs exist
            for contact_id in user_data.created_contacts:
                db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
                if not db_contact:
                    raise HTTPException(status_code=400, detail=f"Contact with id {contact_id} not found")

            # Update the related entities with the new foreign key
            database.query(Contact).filter(Contact.id.in_(user_data.created_contacts)).update(
                {Contact.created_by_id: db_user.id}, synchronize_session=False
            )
    if user_data.email_templates is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(EmailTemplate).filter(EmailTemplate.created_by_id == db_user.id).update(
            {EmailTemplate.created_by_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.email_templates:
            # Validate that all IDs exist
            for emailtemplate_id in user_data.email_templates:
                db_emailtemplate = database.query(EmailTemplate).filter(EmailTemplate.id == emailtemplate_id).first()
                if not db_emailtemplate:
                    raise HTTPException(status_code=400, detail=f"EmailTemplate with id {emailtemplate_id} not found")

            # Update the related entities with the new foreign key
            database.query(EmailTemplate).filter(EmailTemplate.id.in_(user_data.email_templates)).update(
                {EmailTemplate.created_by_id: db_user.id}, synchronize_session=False
            )
    if user_data.created_companies is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Company).filter(Company.created_by_id == db_user.id).update(
            {Company.created_by_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.created_companies:
            # Validate that all IDs exist
            for company_id in user_data.created_companies:
                db_company = database.query(Company).filter(Company.id == company_id).first()
                if not db_company:
                    raise HTTPException(status_code=400, detail=f"Company with id {company_id} not found")

            # Update the related entities with the new foreign key
            database.query(Company).filter(Company.id.in_(user_data.created_companies)).update(
                {Company.created_by_id: db_user.id}, synchronize_session=False
            )
    if user_data.generated_emails is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(GeneratedEmail).filter(GeneratedEmail.created_by_id == db_user.id).update(
            {GeneratedEmail.created_by_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.generated_emails:
            # Validate that all IDs exist
            for generatedemail_id in user_data.generated_emails:
                db_generatedemail = database.query(GeneratedEmail).filter(GeneratedEmail.id == generatedemail_id).first()
                if not db_generatedemail:
                    raise HTTPException(status_code=400, detail=f"GeneratedEmail with id {generatedemail_id} not found")

            # Update the related entities with the new foreign key
            database.query(GeneratedEmail).filter(GeneratedEmail.id.in_(user_data.generated_emails)).update(
                {GeneratedEmail.created_by_id: db_user.id}, synchronize_session=False
            )
    if user_data.owned_opportunities is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Opportunity).filter(Opportunity.owner_id == db_user.id).update(
            {Opportunity.owner_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.owned_opportunities:
            # Validate that all IDs exist
            for opportunity_id in user_data.owned_opportunities:
                db_opportunity = database.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
                if not db_opportunity:
                    raise HTTPException(status_code=400, detail=f"Opportunity with id {opportunity_id} not found")

            # Update the related entities with the new foreign key
            database.query(Opportunity).filter(Opportunity.id.in_(user_data.owned_opportunities)).update(
                {Opportunity.owner_id: db_user.id}, synchronize_session=False
            )
    if user_data.interactions is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Interaction).filter(Interaction.performed_by_id == db_user.id).update(
            {Interaction.performed_by_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.interactions:
            # Validate that all IDs exist
            for interaction_id in user_data.interactions:
                db_interaction = database.query(Interaction).filter(Interaction.id == interaction_id).first()
                if not db_interaction:
                    raise HTTPException(status_code=400, detail=f"Interaction with id {interaction_id} not found")

            # Update the related entities with the new foreign key
            database.query(Interaction).filter(Interaction.id.in_(user_data.interactions)).update(
                {Interaction.performed_by_id: db_user.id}, synchronize_session=False
            )
    if user_data.tasks is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Task).filter(Task.assigned_to_id == db_user.id).update(
            {Task.assigned_to_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.tasks:
            # Validate that all IDs exist
            for task_id in user_data.tasks:
                db_task = database.query(Task).filter(Task.id == task_id).first()
                if not db_task:
                    raise HTTPException(status_code=400, detail=f"Task with id {task_id} not found")

            # Update the related entities with the new foreign key
            database.query(Task).filter(Task.id.in_(user_data.tasks)).update(
                {Task.assigned_to_id: db_user.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_user)

    created_contacts_ids = database.query(Contact.id).filter(Contact.created_by_id == db_user.id).all()
    email_templates_ids = database.query(EmailTemplate.id).filter(EmailTemplate.created_by_id == db_user.id).all()
    created_companies_ids = database.query(Company.id).filter(Company.created_by_id == db_user.id).all()
    generated_emails_ids = database.query(GeneratedEmail.id).filter(GeneratedEmail.created_by_id == db_user.id).all()
    owned_opportunities_ids = database.query(Opportunity.id).filter(Opportunity.owner_id == db_user.id).all()
    interactions_ids = database.query(Interaction.id).filter(Interaction.performed_by_id == db_user.id).all()
    tasks_ids = database.query(Task.id).filter(Task.assigned_to_id == db_user.id).all()
    response_data = {
        "user": db_user,
        "created_contacts_ids": [x[0] for x in created_contacts_ids],        "email_templates_ids": [x[0] for x in email_templates_ids],        "created_companies_ids": [x[0] for x in created_companies_ids],        "generated_emails_ids": [x[0] for x in generated_emails_ids],        "owned_opportunities_ids": [x[0] for x in owned_opportunities_ids],        "interactions_ids": [x[0] for x in interactions_ids],        "tasks_ids": [x[0] for x in tasks_ids]    }
    return response_data


@app.delete("/user/{user_id}/", response_model=None, tags=["User"])
async def delete_user(user_id: int, database: Session = Depends(get_db)):
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    database.delete(db_user)
    database.commit()
    return db_user





############################################
#
#   Company functions
#
############################################

@app.get("/company/", response_model=None, tags=["Company"])
def get_all_company(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Company)
        query = query.options(joinedload(Company.created_by))
        company_list = query.all()

        # Serialize with relationships included
        result = []
        for company_item in company_list:
            item_dict = company_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if company_item.created_by:
                related_obj = company_item.created_by
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['created_by'] = related_dict
            else:
                item_dict['created_by'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            tag_list = database.query(Tag).join(company_tag, Tag.id == company_tag.c.tags).filter(company_tag.c.tagged_companies == company_item.id).all()
            item_dict['tags'] = []
            for tag_obj in tag_list:
                tag_dict = tag_obj.__dict__.copy()
                tag_dict.pop('_sa_instance_state', None)
                item_dict['tags'].append(tag_dict)
            opportunity_list = database.query(Opportunity).filter(Opportunity.company_id == company_item.id).all()
            item_dict['opportunities'] = []
            for opportunity_obj in opportunity_list:
                opportunity_dict = opportunity_obj.__dict__.copy()
                opportunity_dict.pop('_sa_instance_state', None)
                item_dict['opportunities'].append(opportunity_dict)
            contact_list = database.query(Contact).filter(Contact.company_id == company_item.id).all()
            item_dict['contacts'] = []
            for contact_obj in contact_list:
                contact_dict = contact_obj.__dict__.copy()
                contact_dict.pop('_sa_instance_state', None)
                item_dict['contacts'].append(contact_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Company).all()


@app.get("/company/count/", response_model=None, tags=["Company"])
def get_count_company(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Company entities"""
    count = database.query(Company).count()
    return {"count": count}


@app.get("/company/paginated/", response_model=None, tags=["Company"])
def get_paginated_company(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Company entities"""
    total = database.query(Company).count()
    company_list = database.query(Company).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": company_list
        }

    result = []
    for company_item in company_list:
        tag_ids = database.query(company_tag.c.tags).filter(company_tag.c.tagged_companies == company_item.id).all()
        opportunities_ids = database.query(Opportunity.id).filter(Opportunity.company_id == company_item.id).all()
        contacts_ids = database.query(Contact.id).filter(Contact.company_id == company_item.id).all()
        item_data = {
            "company": company_item,
            "tag_ids": [x[0] for x in tag_ids],
            "opportunities_ids": [x[0] for x in opportunities_ids],            "contacts_ids": [x[0] for x in contacts_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/company/search/", response_model=None, tags=["Company"])
def search_company(
    database: Session = Depends(get_db)
) -> list:
    """Search Company entities by attributes"""
    query = database.query(Company)


    results = query.all()
    return results


@app.get("/company/{company_id}/", response_model=None, tags=["Company"])
async def get_company(company_id: int, database: Session = Depends(get_db)) -> Company:
    db_company = database.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    tag_ids = database.query(company_tag.c.tags).filter(company_tag.c.tagged_companies == db_company.id).all()
    opportunities_ids = database.query(Opportunity.id).filter(Opportunity.company_id == db_company.id).all()
    contacts_ids = database.query(Contact.id).filter(Contact.company_id == db_company.id).all()
    response_data = {
        "company": db_company,
        "tag_ids": [x[0] for x in tag_ids],
        "opportunities_ids": [x[0] for x in opportunities_ids],        "contacts_ids": [x[0] for x in contacts_ids]}
    return response_data



@app.post("/company/", response_model=None, tags=["Company"])
async def create_company(company_data: CompanyCreate, database: Session = Depends(get_db)) -> Company:

    if company_data.created_by is not None:
        db_created_by = database.query(User).filter(User.id == company_data.created_by).first()
        if not db_created_by:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")
    if company_data.tags:
        for id in company_data.tags:
            # Entity already validated before creation
            db_tag = database.query(Tag).filter(Tag.id == id).first()
            if not db_tag:
                raise HTTPException(status_code=404, detail=f"Tag with ID {id} not found")

    db_company = Company(
        website=company_data.website,        description=company_data.description,        name=company_data.name,        city=company_data.city,        id=company_data.id,        industry=company_data.industry.value,        linkedin_url=company_data.linkedin_url,        phone=company_data.phone,        country=company_data.country,        updated_at=company_data.updated_at,        address=company_data.address,        created_at=company_data.created_at,        size=company_data.size.value,        created_by_id=company_data.created_by        )

    database.add(db_company)
    database.commit()
    database.refresh(db_company)

    if company_data.opportunities:
        # Validate that all Opportunity IDs exist
        for opportunity_id in company_data.opportunities:
            db_opportunity = database.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
            if not db_opportunity:
                raise HTTPException(status_code=400, detail=f"Opportunity with id {opportunity_id} not found")

        # Update the related entities with the new foreign key
        database.query(Opportunity).filter(Opportunity.id.in_(company_data.opportunities)).update(
            {Opportunity.company_id: db_company.id}, synchronize_session=False
        )
        database.commit()
    if company_data.contacts:
        # Validate that all Contact IDs exist
        for contact_id in company_data.contacts:
            db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
            if not db_contact:
                raise HTTPException(status_code=400, detail=f"Contact with id {contact_id} not found")

        # Update the related entities with the new foreign key
        database.query(Contact).filter(Contact.id.in_(company_data.contacts)).update(
            {Contact.company_id: db_company.id}, synchronize_session=False
        )
        database.commit()

    if company_data.tags:
        for id in company_data.tags:
            # Entity already validated before creation
            db_tag = database.query(Tag).filter(Tag.id == id).first()
            # Create the association
            association = company_tag.insert().values(tagged_companies=db_company.id, tags=db_tag.id)
            database.execute(association)
            database.commit()


    tag_ids = database.query(company_tag.c.tags).filter(company_tag.c.tagged_companies == db_company.id).all()
    opportunities_ids = database.query(Opportunity.id).filter(Opportunity.company_id == db_company.id).all()
    contacts_ids = database.query(Contact.id).filter(Contact.company_id == db_company.id).all()
    response_data = {
        "company": db_company,
        "tag_ids": [x[0] for x in tag_ids],
        "opportunities_ids": [x[0] for x in opportunities_ids],        "contacts_ids": [x[0] for x in contacts_ids]    }
    return response_data


@app.post("/company/bulk/", response_model=None, tags=["Company"])
async def bulk_create_company(items: list[CompanyCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Company entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.created_by:
                raise ValueError("User ID is required")

            db_company = Company(
                website=item_data.website,                description=item_data.description,                name=item_data.name,                city=item_data.city,                id=item_data.id,                industry=item_data.industry.value,                linkedin_url=item_data.linkedin_url,                phone=item_data.phone,                country=item_data.country,                updated_at=item_data.updated_at,                address=item_data.address,                created_at=item_data.created_at,                size=item_data.size.value,                created_by_id=item_data.created_by            )
            database.add(db_company)
            database.flush()  # Get ID without committing
            created_items.append(db_company.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Company entities"
    }


@app.delete("/company/bulk/", response_model=None, tags=["Company"])
async def bulk_delete_company(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Company entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_company = database.query(Company).filter(Company.id == item_id).first()
        if db_company:
            database.delete(db_company)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Company entities"
    }

@app.put("/company/{company_id}/", response_model=None, tags=["Company"])
async def update_company(company_id: int, company_data: CompanyCreate, database: Session = Depends(get_db)) -> Company:
    db_company = database.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    setattr(db_company, 'website', company_data.website)
    setattr(db_company, 'description', company_data.description)
    setattr(db_company, 'name', company_data.name)
    setattr(db_company, 'city', company_data.city)
    setattr(db_company, 'id', company_data.id)
    setattr(db_company, 'industry', company_data.industry.value)
    setattr(db_company, 'linkedin_url', company_data.linkedin_url)
    setattr(db_company, 'phone', company_data.phone)
    setattr(db_company, 'country', company_data.country)
    setattr(db_company, 'updated_at', company_data.updated_at)
    setattr(db_company, 'address', company_data.address)
    setattr(db_company, 'created_at', company_data.created_at)
    setattr(db_company, 'size', company_data.size.value)
    if company_data.created_by is not None:
        db_created_by = database.query(User).filter(User.id == company_data.created_by).first()
        if not db_created_by:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_company, 'created_by_id', company_data.created_by)
    if company_data.opportunities is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Opportunity).filter(Opportunity.company_id == db_company.id).update(
            {Opportunity.company_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if company_data.opportunities:
            # Validate that all IDs exist
            for opportunity_id in company_data.opportunities:
                db_opportunity = database.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
                if not db_opportunity:
                    raise HTTPException(status_code=400, detail=f"Opportunity with id {opportunity_id} not found")

            # Update the related entities with the new foreign key
            database.query(Opportunity).filter(Opportunity.id.in_(company_data.opportunities)).update(
                {Opportunity.company_id: db_company.id}, synchronize_session=False
            )
    if company_data.contacts is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Contact).filter(Contact.company_id == db_company.id).update(
            {Contact.company_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if company_data.contacts:
            # Validate that all IDs exist
            for contact_id in company_data.contacts:
                db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
                if not db_contact:
                    raise HTTPException(status_code=400, detail=f"Contact with id {contact_id} not found")

            # Update the related entities with the new foreign key
            database.query(Contact).filter(Contact.id.in_(company_data.contacts)).update(
                {Contact.company_id: db_company.id}, synchronize_session=False
            )
    existing_tag_ids = [assoc.tags for assoc in database.execute(
        company_tag.select().where(company_tag.c.tagged_companies == db_company.id))]

    tags_to_remove = set(existing_tag_ids) - set(company_data.tags)
    for tag_id in tags_to_remove:
        association = company_tag.delete().where(
            (company_tag.c.tagged_companies == db_company.id) & (company_tag.c.tags == tag_id))
        database.execute(association)

    new_tag_ids = set(company_data.tags) - set(existing_tag_ids)
    for tag_id in new_tag_ids:
        db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
        if db_tag is None:
            raise HTTPException(status_code=404, detail=f"Tag with ID {tag_id} not found")
        association = company_tag.insert().values(tags=db_tag.id, tagged_companies=db_company.id)
        database.execute(association)
    database.commit()
    database.refresh(db_company)

    tag_ids = database.query(company_tag.c.tags).filter(company_tag.c.tagged_companies == db_company.id).all()
    opportunities_ids = database.query(Opportunity.id).filter(Opportunity.company_id == db_company.id).all()
    contacts_ids = database.query(Contact.id).filter(Contact.company_id == db_company.id).all()
    response_data = {
        "company": db_company,
        "tag_ids": [x[0] for x in tag_ids],
        "opportunities_ids": [x[0] for x in opportunities_ids],        "contacts_ids": [x[0] for x in contacts_ids]    }
    return response_data


@app.delete("/company/{company_id}/", response_model=None, tags=["Company"])
async def delete_company(company_id: int, database: Session = Depends(get_db)):
    db_company = database.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    database.delete(db_company)
    database.commit()
    return db_company

@app.post("/company/{company_id}/tags/{tag_id}/", response_model=None, tags=["Company Relationships"])
async def add_tags_to_company(company_id: int, tag_id: int, database: Session = Depends(get_db)):
    """Add a Tag to this Company's tags relationship"""
    db_company = database.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Check if relationship already exists
    existing = database.query(company_tag).filter(
        (company_tag.c.tagged_companies == company_id) &
        (company_tag.c.tags == tag_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = company_tag.insert().values(tagged_companies=company_id, tags=tag_id)
    database.execute(association)
    database.commit()

    return {"message": "Tag added to tags successfully"}


@app.delete("/company/{company_id}/tags/{tag_id}/", response_model=None, tags=["Company Relationships"])
async def remove_tags_from_company(company_id: int, tag_id: int, database: Session = Depends(get_db)):
    """Remove a Tag from this Company's tags relationship"""
    db_company = database.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    # Check if relationship exists
    existing = database.query(company_tag).filter(
        (company_tag.c.tagged_companies == company_id) &
        (company_tag.c.tags == tag_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = company_tag.delete().where(
        (company_tag.c.tagged_companies == company_id) &
        (company_tag.c.tags == tag_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Tag removed from tags successfully"}


@app.get("/company/{company_id}/tags/", response_model=None, tags=["Company Relationships"])
async def get_tags_of_company(company_id: int, database: Session = Depends(get_db)):
    """Get all Tag entities related to this Company through tags"""
    db_company = database.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    tag_ids = database.query(company_tag.c.tags).filter(company_tag.c.tagged_companies == company_id).all()
    tag_list = database.query(Tag).filter(Tag.id.in_([id[0] for id in tag_ids])).all()

    return {
        "company_id": company_id,
        "tags_count": len(tag_list),
        "tags": tag_list
    }





############################################
#
#   Contact functions
#
############################################

@app.get("/contact/", response_model=None, tags=["Contact"])
def get_all_contact(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Contact)
        query = query.options(joinedload(Contact.created_by))
        query = query.options(joinedload(Contact.company))
        contact_list = query.all()

        # Serialize with relationships included
        result = []
        for contact_item in contact_list:
            item_dict = contact_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if contact_item.created_by:
                related_obj = contact_item.created_by
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['created_by'] = related_dict
            else:
                item_dict['created_by'] = None
            if contact_item.company:
                related_obj = contact_item.company
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['company'] = related_dict
            else:
                item_dict['company'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            tag_list = database.query(Tag).join(contact_tag, Tag.id == contact_tag.c.tags).filter(contact_tag.c.tagged_contacts == contact_item.id).all()
            item_dict['tags'] = []
            for tag_obj in tag_list:
                tag_dict = tag_obj.__dict__.copy()
                tag_dict.pop('_sa_instance_state', None)
                item_dict['tags'].append(tag_dict)
            opportunity_list = database.query(Opportunity).join(opportunity_contact, Opportunity.id == opportunity_contact.c.opportunities).filter(opportunity_contact.c.contacts == contact_item.id).all()
            item_dict['opportunities'] = []
            for opportunity_obj in opportunity_list:
                opportunity_dict = opportunity_obj.__dict__.copy()
                opportunity_dict.pop('_sa_instance_state', None)
                item_dict['opportunities'].append(opportunity_dict)
            generatedemail_list = database.query(GeneratedEmail).filter(GeneratedEmail.contact_id == contact_item.id).all()
            item_dict['generated_emails'] = []
            for generatedemail_obj in generatedemail_list:
                generatedemail_dict = generatedemail_obj.__dict__.copy()
                generatedemail_dict.pop('_sa_instance_state', None)
                item_dict['generated_emails'].append(generatedemail_dict)
            interaction_list = database.query(Interaction).filter(Interaction.contact_id == contact_item.id).all()
            item_dict['interactions'] = []
            for interaction_obj in interaction_list:
                interaction_dict = interaction_obj.__dict__.copy()
                interaction_dict.pop('_sa_instance_state', None)
                item_dict['interactions'].append(interaction_dict)
            scorehistory_list = database.query(ScoreHistory).filter(ScoreHistory.contact_id == contact_item.id).all()
            item_dict['score_history'] = []
            for scorehistory_obj in scorehistory_list:
                scorehistory_dict = scorehistory_obj.__dict__.copy()
                scorehistory_dict.pop('_sa_instance_state', None)
                item_dict['score_history'].append(scorehistory_dict)
            task_list = database.query(Task).filter(Task.contact_id == contact_item.id).all()
            item_dict['tasks'] = []
            for task_obj in task_list:
                task_dict = task_obj.__dict__.copy()
                task_dict.pop('_sa_instance_state', None)
                item_dict['tasks'].append(task_dict)
            enrichmentlog_list = database.query(EnrichmentLog).filter(EnrichmentLog.contact_id == contact_item.id).all()
            item_dict['enrichment_logs'] = []
            for enrichmentlog_obj in enrichmentlog_list:
                enrichmentlog_dict = enrichmentlog_obj.__dict__.copy()
                enrichmentlog_dict.pop('_sa_instance_state', None)
                item_dict['enrichment_logs'].append(enrichmentlog_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Contact).all()


@app.get("/contact/count/", response_model=None, tags=["Contact"])
def get_count_contact(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Contact entities"""
    count = database.query(Contact).count()
    return {"count": count}


@app.get("/contact/paginated/", response_model=None, tags=["Contact"])
def get_paginated_contact(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Contact entities"""
    total = database.query(Contact).count()
    contact_list = database.query(Contact).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": contact_list
        }

    result = []
    for contact_item in contact_list:
        tag_ids = database.query(contact_tag.c.tags).filter(contact_tag.c.tagged_contacts == contact_item.id).all()
        opportunity_ids = database.query(opportunity_contact.c.opportunities).filter(opportunity_contact.c.contacts == contact_item.id).all()
        generated_emails_ids = database.query(GeneratedEmail.id).filter(GeneratedEmail.contact_id == contact_item.id).all()
        interactions_ids = database.query(Interaction.id).filter(Interaction.contact_id == contact_item.id).all()
        score_history_ids = database.query(ScoreHistory.id).filter(ScoreHistory.contact_id == contact_item.id).all()
        tasks_ids = database.query(Task.id).filter(Task.contact_id == contact_item.id).all()
        enrichment_logs_ids = database.query(EnrichmentLog.id).filter(EnrichmentLog.contact_id == contact_item.id).all()
        item_data = {
            "contact": contact_item,
            "tag_ids": [x[0] for x in tag_ids],
            "opportunity_ids": [x[0] for x in opportunity_ids],
            "generated_emails_ids": [x[0] for x in generated_emails_ids],            "interactions_ids": [x[0] for x in interactions_ids],            "score_history_ids": [x[0] for x in score_history_ids],            "tasks_ids": [x[0] for x in tasks_ids],            "enrichment_logs_ids": [x[0] for x in enrichment_logs_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/contact/search/", response_model=None, tags=["Contact"])
def search_contact(
    database: Session = Depends(get_db)
) -> list:
    """Search Contact entities by attributes"""
    query = database.query(Contact)


    results = query.all()
    return results


@app.get("/contact/{contact_id}/", response_model=None, tags=["Contact"])
async def get_contact(contact_id: int, database: Session = Depends(get_db)) -> Contact:
    db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    tag_ids = database.query(contact_tag.c.tags).filter(contact_tag.c.tagged_contacts == db_contact.id).all()
    opportunity_ids = database.query(opportunity_contact.c.opportunities).filter(opportunity_contact.c.contacts == db_contact.id).all()
    generated_emails_ids = database.query(GeneratedEmail.id).filter(GeneratedEmail.contact_id == db_contact.id).all()
    interactions_ids = database.query(Interaction.id).filter(Interaction.contact_id == db_contact.id).all()
    score_history_ids = database.query(ScoreHistory.id).filter(ScoreHistory.contact_id == db_contact.id).all()
    tasks_ids = database.query(Task.id).filter(Task.contact_id == db_contact.id).all()
    enrichment_logs_ids = database.query(EnrichmentLog.id).filter(EnrichmentLog.contact_id == db_contact.id).all()
    response_data = {
        "contact": db_contact,
        "tag_ids": [x[0] for x in tag_ids],
        "opportunity_ids": [x[0] for x in opportunity_ids],
        "generated_emails_ids": [x[0] for x in generated_emails_ids],        "interactions_ids": [x[0] for x in interactions_ids],        "score_history_ids": [x[0] for x in score_history_ids],        "tasks_ids": [x[0] for x in tasks_ids],        "enrichment_logs_ids": [x[0] for x in enrichment_logs_ids]}
    return response_data



@app.post("/contact/", response_model=None, tags=["Contact"])
async def create_contact(contact_data: ContactCreate, database: Session = Depends(get_db)) -> Contact:

    if contact_data.created_by is not None:
        db_created_by = database.query(User).filter(User.id == contact_data.created_by).first()
        if not db_created_by:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")
    if contact_data.company :
        db_company = database.query(Company).filter(Company.id == contact_data.company).first()
        if not db_company:
            raise HTTPException(status_code=400, detail="Company not found")
    if contact_data.tags:
        for id in contact_data.tags:
            # Entity already validated before creation
            db_tag = database.query(Tag).filter(Tag.id == id).first()
            if not db_tag:
                raise HTTPException(status_code=404, detail=f"Tag with ID {id} not found")
    if contact_data.opportunities:
        for id in contact_data.opportunities:
            # Entity already validated before creation
            db_opportunity = database.query(Opportunity).filter(Opportunity.id == id).first()
            if not db_opportunity:
                raise HTTPException(status_code=404, detail=f"Opportunity with ID {id} not found")

    db_contact = Contact(
        first_name=contact_data.first_name,        phone=contact_data.phone,        lead_score=contact_data.lead_score,        notes=contact_data.notes,        job_title=contact_data.job_title,        created_at=contact_data.created_at,        profile_picture_url=contact_data.profile_picture_url,        is_enriched=contact_data.is_enriched,        updated_at=contact_data.updated_at,        email=contact_data.email,        id=contact_data.id,        last_name=contact_data.last_name,        linkedin_url=contact_data.linkedin_url,        lead_score_level=contact_data.lead_score_level.value,        created_by_id=contact_data.created_by,        company_id=contact_data.company        )

    database.add(db_contact)
    database.commit()
    database.refresh(db_contact)

    if contact_data.generated_emails:
        # Validate that all GeneratedEmail IDs exist
        for generatedemail_id in contact_data.generated_emails:
            db_generatedemail = database.query(GeneratedEmail).filter(GeneratedEmail.id == generatedemail_id).first()
            if not db_generatedemail:
                raise HTTPException(status_code=400, detail=f"GeneratedEmail with id {generatedemail_id} not found")

        # Update the related entities with the new foreign key
        database.query(GeneratedEmail).filter(GeneratedEmail.id.in_(contact_data.generated_emails)).update(
            {GeneratedEmail.contact_id: db_contact.id}, synchronize_session=False
        )
        database.commit()
    if contact_data.interactions:
        # Validate that all Interaction IDs exist
        for interaction_id in contact_data.interactions:
            db_interaction = database.query(Interaction).filter(Interaction.id == interaction_id).first()
            if not db_interaction:
                raise HTTPException(status_code=400, detail=f"Interaction with id {interaction_id} not found")

        # Update the related entities with the new foreign key
        database.query(Interaction).filter(Interaction.id.in_(contact_data.interactions)).update(
            {Interaction.contact_id: db_contact.id}, synchronize_session=False
        )
        database.commit()
    if contact_data.score_history:
        # Validate that all ScoreHistory IDs exist
        for scorehistory_id in contact_data.score_history:
            db_scorehistory = database.query(ScoreHistory).filter(ScoreHistory.id == scorehistory_id).first()
            if not db_scorehistory:
                raise HTTPException(status_code=400, detail=f"ScoreHistory with id {scorehistory_id} not found")

        # Update the related entities with the new foreign key
        database.query(ScoreHistory).filter(ScoreHistory.id.in_(contact_data.score_history)).update(
            {ScoreHistory.contact_id: db_contact.id}, synchronize_session=False
        )
        database.commit()
    if contact_data.tasks:
        # Validate that all Task IDs exist
        for task_id in contact_data.tasks:
            db_task = database.query(Task).filter(Task.id == task_id).first()
            if not db_task:
                raise HTTPException(status_code=400, detail=f"Task with id {task_id} not found")

        # Update the related entities with the new foreign key
        database.query(Task).filter(Task.id.in_(contact_data.tasks)).update(
            {Task.contact_id: db_contact.id}, synchronize_session=False
        )
        database.commit()
    if contact_data.enrichment_logs:
        # Validate that all EnrichmentLog IDs exist
        for enrichmentlog_id in contact_data.enrichment_logs:
            db_enrichmentlog = database.query(EnrichmentLog).filter(EnrichmentLog.id == enrichmentlog_id).first()
            if not db_enrichmentlog:
                raise HTTPException(status_code=400, detail=f"EnrichmentLog with id {enrichmentlog_id} not found")

        # Update the related entities with the new foreign key
        database.query(EnrichmentLog).filter(EnrichmentLog.id.in_(contact_data.enrichment_logs)).update(
            {EnrichmentLog.contact_id: db_contact.id}, synchronize_session=False
        )
        database.commit()

    if contact_data.tags:
        for id in contact_data.tags:
            # Entity already validated before creation
            db_tag = database.query(Tag).filter(Tag.id == id).first()
            # Create the association
            association = contact_tag.insert().values(tagged_contacts=db_contact.id, tags=db_tag.id)
            database.execute(association)
            database.commit()
    if contact_data.opportunities:
        for id in contact_data.opportunities:
            # Entity already validated before creation
            db_opportunity = database.query(Opportunity).filter(Opportunity.id == id).first()
            # Create the association
            association = opportunity_contact.insert().values(contacts=db_contact.id, opportunities=db_opportunity.id)
            database.execute(association)
            database.commit()


    tag_ids = database.query(contact_tag.c.tags).filter(contact_tag.c.tagged_contacts == db_contact.id).all()
    opportunity_ids = database.query(opportunity_contact.c.opportunities).filter(opportunity_contact.c.contacts == db_contact.id).all()
    generated_emails_ids = database.query(GeneratedEmail.id).filter(GeneratedEmail.contact_id == db_contact.id).all()
    interactions_ids = database.query(Interaction.id).filter(Interaction.contact_id == db_contact.id).all()
    score_history_ids = database.query(ScoreHistory.id).filter(ScoreHistory.contact_id == db_contact.id).all()
    tasks_ids = database.query(Task.id).filter(Task.contact_id == db_contact.id).all()
    enrichment_logs_ids = database.query(EnrichmentLog.id).filter(EnrichmentLog.contact_id == db_contact.id).all()
    response_data = {
        "contact": db_contact,
        "tag_ids": [x[0] for x in tag_ids],
        "opportunity_ids": [x[0] for x in opportunity_ids],
        "generated_emails_ids": [x[0] for x in generated_emails_ids],        "interactions_ids": [x[0] for x in interactions_ids],        "score_history_ids": [x[0] for x in score_history_ids],        "tasks_ids": [x[0] for x in tasks_ids],        "enrichment_logs_ids": [x[0] for x in enrichment_logs_ids]    }
    return response_data


@app.post("/contact/bulk/", response_model=None, tags=["Contact"])
async def bulk_create_contact(items: list[ContactCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Contact entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.created_by:
                raise ValueError("User ID is required")

            db_contact = Contact(
                first_name=item_data.first_name,                phone=item_data.phone,                lead_score=item_data.lead_score,                notes=item_data.notes,                job_title=item_data.job_title,                created_at=item_data.created_at,                profile_picture_url=item_data.profile_picture_url,                is_enriched=item_data.is_enriched,                updated_at=item_data.updated_at,                email=item_data.email,                id=item_data.id,                last_name=item_data.last_name,                linkedin_url=item_data.linkedin_url,                lead_score_level=item_data.lead_score_level.value,                created_by_id=item_data.created_by,                company_id=item_data.company            )
            database.add(db_contact)
            database.flush()  # Get ID without committing
            created_items.append(db_contact.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Contact entities"
    }


@app.delete("/contact/bulk/", response_model=None, tags=["Contact"])
async def bulk_delete_contact(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Contact entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_contact = database.query(Contact).filter(Contact.id == item_id).first()
        if db_contact:
            database.delete(db_contact)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Contact entities"
    }

@app.put("/contact/{contact_id}/", response_model=None, tags=["Contact"])
async def update_contact(contact_id: int, contact_data: ContactCreate, database: Session = Depends(get_db)) -> Contact:
    db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    setattr(db_contact, 'first_name', contact_data.first_name)
    setattr(db_contact, 'phone', contact_data.phone)
    setattr(db_contact, 'lead_score', contact_data.lead_score)
    setattr(db_contact, 'notes', contact_data.notes)
    setattr(db_contact, 'job_title', contact_data.job_title)
    setattr(db_contact, 'created_at', contact_data.created_at)
    setattr(db_contact, 'profile_picture_url', contact_data.profile_picture_url)
    setattr(db_contact, 'is_enriched', contact_data.is_enriched)
    setattr(db_contact, 'updated_at', contact_data.updated_at)
    setattr(db_contact, 'email', contact_data.email)
    setattr(db_contact, 'id', contact_data.id)
    setattr(db_contact, 'last_name', contact_data.last_name)
    setattr(db_contact, 'linkedin_url', contact_data.linkedin_url)
    setattr(db_contact, 'lead_score_level', contact_data.lead_score_level.value)
    if contact_data.created_by is not None:
        db_created_by = database.query(User).filter(User.id == contact_data.created_by).first()
        if not db_created_by:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_contact, 'created_by_id', contact_data.created_by)
    if contact_data.company is not None:
        db_company = database.query(Company).filter(Company.id == contact_data.company).first()
        if not db_company:
            raise HTTPException(status_code=400, detail="Company not found")
        setattr(db_contact, 'company_id', contact_data.company)
    else:
        setattr(db_contact, 'company_id', None)
    if contact_data.generated_emails is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(GeneratedEmail).filter(GeneratedEmail.contact_id == db_contact.id).update(
            {GeneratedEmail.contact_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if contact_data.generated_emails:
            # Validate that all IDs exist
            for generatedemail_id in contact_data.generated_emails:
                db_generatedemail = database.query(GeneratedEmail).filter(GeneratedEmail.id == generatedemail_id).first()
                if not db_generatedemail:
                    raise HTTPException(status_code=400, detail=f"GeneratedEmail with id {generatedemail_id} not found")

            # Update the related entities with the new foreign key
            database.query(GeneratedEmail).filter(GeneratedEmail.id.in_(contact_data.generated_emails)).update(
                {GeneratedEmail.contact_id: db_contact.id}, synchronize_session=False
            )
    if contact_data.interactions is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Interaction).filter(Interaction.contact_id == db_contact.id).update(
            {Interaction.contact_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if contact_data.interactions:
            # Validate that all IDs exist
            for interaction_id in contact_data.interactions:
                db_interaction = database.query(Interaction).filter(Interaction.id == interaction_id).first()
                if not db_interaction:
                    raise HTTPException(status_code=400, detail=f"Interaction with id {interaction_id} not found")

            # Update the related entities with the new foreign key
            database.query(Interaction).filter(Interaction.id.in_(contact_data.interactions)).update(
                {Interaction.contact_id: db_contact.id}, synchronize_session=False
            )
    if contact_data.score_history is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(ScoreHistory).filter(ScoreHistory.contact_id == db_contact.id).update(
            {ScoreHistory.contact_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if contact_data.score_history:
            # Validate that all IDs exist
            for scorehistory_id in contact_data.score_history:
                db_scorehistory = database.query(ScoreHistory).filter(ScoreHistory.id == scorehistory_id).first()
                if not db_scorehistory:
                    raise HTTPException(status_code=400, detail=f"ScoreHistory with id {scorehistory_id} not found")

            # Update the related entities with the new foreign key
            database.query(ScoreHistory).filter(ScoreHistory.id.in_(contact_data.score_history)).update(
                {ScoreHistory.contact_id: db_contact.id}, synchronize_session=False
            )
    if contact_data.tasks is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Task).filter(Task.contact_id == db_contact.id).update(
            {Task.contact_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if contact_data.tasks:
            # Validate that all IDs exist
            for task_id in contact_data.tasks:
                db_task = database.query(Task).filter(Task.id == task_id).first()
                if not db_task:
                    raise HTTPException(status_code=400, detail=f"Task with id {task_id} not found")

            # Update the related entities with the new foreign key
            database.query(Task).filter(Task.id.in_(contact_data.tasks)).update(
                {Task.contact_id: db_contact.id}, synchronize_session=False
            )
    if contact_data.enrichment_logs is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(EnrichmentLog).filter(EnrichmentLog.contact_id == db_contact.id).update(
            {EnrichmentLog.contact_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if contact_data.enrichment_logs:
            # Validate that all IDs exist
            for enrichmentlog_id in contact_data.enrichment_logs:
                db_enrichmentlog = database.query(EnrichmentLog).filter(EnrichmentLog.id == enrichmentlog_id).first()
                if not db_enrichmentlog:
                    raise HTTPException(status_code=400, detail=f"EnrichmentLog with id {enrichmentlog_id} not found")

            # Update the related entities with the new foreign key
            database.query(EnrichmentLog).filter(EnrichmentLog.id.in_(contact_data.enrichment_logs)).update(
                {EnrichmentLog.contact_id: db_contact.id}, synchronize_session=False
            )
    existing_tag_ids = [assoc.tags for assoc in database.execute(
        contact_tag.select().where(contact_tag.c.tagged_contacts == db_contact.id))]

    tags_to_remove = set(existing_tag_ids) - set(contact_data.tags)
    for tag_id in tags_to_remove:
        association = contact_tag.delete().where(
            (contact_tag.c.tagged_contacts == db_contact.id) & (contact_tag.c.tags == tag_id))
        database.execute(association)

    new_tag_ids = set(contact_data.tags) - set(existing_tag_ids)
    for tag_id in new_tag_ids:
        db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
        if db_tag is None:
            raise HTTPException(status_code=404, detail=f"Tag with ID {tag_id} not found")
        association = contact_tag.insert().values(tags=db_tag.id, tagged_contacts=db_contact.id)
        database.execute(association)
    existing_opportunity_ids = [assoc.opportunities for assoc in database.execute(
        opportunity_contact.select().where(opportunity_contact.c.contacts == db_contact.id))]

    opportunitys_to_remove = set(existing_opportunity_ids) - set(contact_data.opportunities)
    for opportunity_id in opportunitys_to_remove:
        association = opportunity_contact.delete().where(
            (opportunity_contact.c.contacts == db_contact.id) & (opportunity_contact.c.opportunities == opportunity_id))
        database.execute(association)

    new_opportunity_ids = set(contact_data.opportunities) - set(existing_opportunity_ids)
    for opportunity_id in new_opportunity_ids:
        db_opportunity = database.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
        if db_opportunity is None:
            raise HTTPException(status_code=404, detail=f"Opportunity with ID {opportunity_id} not found")
        association = opportunity_contact.insert().values(opportunities=db_opportunity.id, contacts=db_contact.id)
        database.execute(association)
    database.commit()
    database.refresh(db_contact)

    tag_ids = database.query(contact_tag.c.tags).filter(contact_tag.c.tagged_contacts == db_contact.id).all()
    opportunity_ids = database.query(opportunity_contact.c.opportunities).filter(opportunity_contact.c.contacts == db_contact.id).all()
    generated_emails_ids = database.query(GeneratedEmail.id).filter(GeneratedEmail.contact_id == db_contact.id).all()
    interactions_ids = database.query(Interaction.id).filter(Interaction.contact_id == db_contact.id).all()
    score_history_ids = database.query(ScoreHistory.id).filter(ScoreHistory.contact_id == db_contact.id).all()
    tasks_ids = database.query(Task.id).filter(Task.contact_id == db_contact.id).all()
    enrichment_logs_ids = database.query(EnrichmentLog.id).filter(EnrichmentLog.contact_id == db_contact.id).all()
    response_data = {
        "contact": db_contact,
        "tag_ids": [x[0] for x in tag_ids],
        "opportunity_ids": [x[0] for x in opportunity_ids],
        "generated_emails_ids": [x[0] for x in generated_emails_ids],        "interactions_ids": [x[0] for x in interactions_ids],        "score_history_ids": [x[0] for x in score_history_ids],        "tasks_ids": [x[0] for x in tasks_ids],        "enrichment_logs_ids": [x[0] for x in enrichment_logs_ids]    }
    return response_data


@app.delete("/contact/{contact_id}/", response_model=None, tags=["Contact"])
async def delete_contact(contact_id: int, database: Session = Depends(get_db)):
    db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    database.delete(db_contact)
    database.commit()
    return db_contact

@app.post("/contact/{contact_id}/tags/{tag_id}/", response_model=None, tags=["Contact Relationships"])
async def add_tags_to_contact(contact_id: int, tag_id: int, database: Session = Depends(get_db)):
    """Add a Tag to this Contact's tags relationship"""
    db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Check if relationship already exists
    existing = database.query(contact_tag).filter(
        (contact_tag.c.tagged_contacts == contact_id) &
        (contact_tag.c.tags == tag_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = contact_tag.insert().values(tagged_contacts=contact_id, tags=tag_id)
    database.execute(association)
    database.commit()

    return {"message": "Tag added to tags successfully"}


@app.delete("/contact/{contact_id}/tags/{tag_id}/", response_model=None, tags=["Contact Relationships"])
async def remove_tags_from_contact(contact_id: int, tag_id: int, database: Session = Depends(get_db)):
    """Remove a Tag from this Contact's tags relationship"""
    db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    # Check if relationship exists
    existing = database.query(contact_tag).filter(
        (contact_tag.c.tagged_contacts == contact_id) &
        (contact_tag.c.tags == tag_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = contact_tag.delete().where(
        (contact_tag.c.tagged_contacts == contact_id) &
        (contact_tag.c.tags == tag_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Tag removed from tags successfully"}


@app.get("/contact/{contact_id}/tags/", response_model=None, tags=["Contact Relationships"])
async def get_tags_of_contact(contact_id: int, database: Session = Depends(get_db)):
    """Get all Tag entities related to this Contact through tags"""
    db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    tag_ids = database.query(contact_tag.c.tags).filter(contact_tag.c.tagged_contacts == contact_id).all()
    tag_list = database.query(Tag).filter(Tag.id.in_([id[0] for id in tag_ids])).all()

    return {
        "contact_id": contact_id,
        "tags_count": len(tag_list),
        "tags": tag_list
    }

@app.post("/contact/{contact_id}/opportunities/{opportunity_id}/", response_model=None, tags=["Contact Relationships"])
async def add_opportunities_to_contact(contact_id: int, opportunity_id: int, database: Session = Depends(get_db)):
    """Add a Opportunity to this Contact's opportunities relationship"""
    db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    db_opportunity = database.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    # Check if relationship already exists
    existing = database.query(opportunity_contact).filter(
        (opportunity_contact.c.contacts == contact_id) &
        (opportunity_contact.c.opportunities == opportunity_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = opportunity_contact.insert().values(contacts=contact_id, opportunities=opportunity_id)
    database.execute(association)
    database.commit()

    return {"message": "Opportunity added to opportunities successfully"}


@app.delete("/contact/{contact_id}/opportunities/{opportunity_id}/", response_model=None, tags=["Contact Relationships"])
async def remove_opportunities_from_contact(contact_id: int, opportunity_id: int, database: Session = Depends(get_db)):
    """Remove a Opportunity from this Contact's opportunities relationship"""
    db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    # Check if relationship exists
    existing = database.query(opportunity_contact).filter(
        (opportunity_contact.c.contacts == contact_id) &
        (opportunity_contact.c.opportunities == opportunity_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = opportunity_contact.delete().where(
        (opportunity_contact.c.contacts == contact_id) &
        (opportunity_contact.c.opportunities == opportunity_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Opportunity removed from opportunities successfully"}


@app.get("/contact/{contact_id}/opportunities/", response_model=None, tags=["Contact Relationships"])
async def get_opportunities_of_contact(contact_id: int, database: Session = Depends(get_db)):
    """Get all Opportunity entities related to this Contact through opportunities"""
    db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    opportunity_ids = database.query(opportunity_contact.c.opportunities).filter(opportunity_contact.c.contacts == contact_id).all()
    opportunity_list = database.query(Opportunity).filter(Opportunity.id.in_([id[0] for id in opportunity_ids])).all()

    return {
        "contact_id": contact_id,
        "opportunities_count": len(opportunity_list),
        "opportunities": opportunity_list
    }





############################################
#
#   Opportunity functions
#
############################################

@app.get("/opportunity/", response_model=None, tags=["Opportunity"])
def get_all_opportunity(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Opportunity)
        query = query.options(joinedload(Opportunity.owner))
        query = query.options(joinedload(Opportunity.company))
        opportunity_list = query.all()

        # Serialize with relationships included
        result = []
        for opportunity_item in opportunity_list:
            item_dict = opportunity_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if opportunity_item.owner:
                related_obj = opportunity_item.owner
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['owner'] = related_dict
            else:
                item_dict['owner'] = None
            if opportunity_item.company:
                related_obj = opportunity_item.company
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['company'] = related_dict
            else:
                item_dict['company'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            contact_list = database.query(Contact).join(opportunity_contact, Contact.id == opportunity_contact.c.contacts).filter(opportunity_contact.c.opportunities == opportunity_item.id).all()
            item_dict['contacts'] = []
            for contact_obj in contact_list:
                contact_dict = contact_obj.__dict__.copy()
                contact_dict.pop('_sa_instance_state', None)
                item_dict['contacts'].append(contact_dict)
            task_list = database.query(Task).filter(Task.opportunity_id == opportunity_item.id).all()
            item_dict['tasks'] = []
            for task_obj in task_list:
                task_dict = task_obj.__dict__.copy()
                task_dict.pop('_sa_instance_state', None)
                item_dict['tasks'].append(task_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Opportunity).all()


@app.get("/opportunity/count/", response_model=None, tags=["Opportunity"])
def get_count_opportunity(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Opportunity entities"""
    count = database.query(Opportunity).count()
    return {"count": count}


@app.get("/opportunity/paginated/", response_model=None, tags=["Opportunity"])
def get_paginated_opportunity(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Opportunity entities"""
    total = database.query(Opportunity).count()
    opportunity_list = database.query(Opportunity).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": opportunity_list
        }

    result = []
    for opportunity_item in opportunity_list:
        contact_ids = database.query(opportunity_contact.c.contacts).filter(opportunity_contact.c.opportunities == opportunity_item.id).all()
        tasks_ids = database.query(Task.id).filter(Task.opportunity_id == opportunity_item.id).all()
        item_data = {
            "opportunity": opportunity_item,
            "contact_ids": [x[0] for x in contact_ids],
            "tasks_ids": [x[0] for x in tasks_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/opportunity/search/", response_model=None, tags=["Opportunity"])
def search_opportunity(
    database: Session = Depends(get_db)
) -> list:
    """Search Opportunity entities by attributes"""
    query = database.query(Opportunity)


    results = query.all()
    return results


@app.get("/opportunity/{opportunity_id}/", response_model=None, tags=["Opportunity"])
async def get_opportunity(opportunity_id: int, database: Session = Depends(get_db)) -> Opportunity:
    db_opportunity = database.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    contact_ids = database.query(opportunity_contact.c.contacts).filter(opportunity_contact.c.opportunities == db_opportunity.id).all()
    tasks_ids = database.query(Task.id).filter(Task.opportunity_id == db_opportunity.id).all()
    response_data = {
        "opportunity": db_opportunity,
        "contact_ids": [x[0] for x in contact_ids],
        "tasks_ids": [x[0] for x in tasks_ids]}
    return response_data



@app.post("/opportunity/", response_model=None, tags=["Opportunity"])
async def create_opportunity(opportunity_data: OpportunityCreate, database: Session = Depends(get_db)) -> Opportunity:

    if opportunity_data.owner is not None:
        db_owner = database.query(User).filter(User.id == opportunity_data.owner).first()
        if not db_owner:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")
    if opportunity_data.company :
        db_company = database.query(Company).filter(Company.id == opportunity_data.company).first()
        if not db_company:
            raise HTTPException(status_code=400, detail="Company not found")
    if not opportunity_data.contacts or len(opportunity_data.contacts) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Contact(s) required")
    if opportunity_data.contacts:
        for id in opportunity_data.contacts:
            # Entity already validated before creation
            db_contact = database.query(Contact).filter(Contact.id == id).first()
            if not db_contact:
                raise HTTPException(status_code=404, detail=f"Contact with ID {id} not found")

    db_opportunity = Opportunity(
        updated_at=opportunity_data.updated_at,        id=opportunity_data.id,        created_at=opportunity_data.created_at,        value=opportunity_data.value,        stage=opportunity_data.stage.value,        expected_close_date=opportunity_data.expected_close_date,        closed_at=opportunity_data.closed_at,        description=opportunity_data.description,        probability=opportunity_data.probability,        title=opportunity_data.title,        owner_id=opportunity_data.owner,        company_id=opportunity_data.company        )

    database.add(db_opportunity)
    database.commit()
    database.refresh(db_opportunity)

    if opportunity_data.tasks:
        # Validate that all Task IDs exist
        for task_id in opportunity_data.tasks:
            db_task = database.query(Task).filter(Task.id == task_id).first()
            if not db_task:
                raise HTTPException(status_code=400, detail=f"Task with id {task_id} not found")

        # Update the related entities with the new foreign key
        database.query(Task).filter(Task.id.in_(opportunity_data.tasks)).update(
            {Task.opportunity_id: db_opportunity.id}, synchronize_session=False
        )
        database.commit()

    if opportunity_data.contacts:
        for id in opportunity_data.contacts:
            # Entity already validated before creation
            db_contact = database.query(Contact).filter(Contact.id == id).first()
            # Create the association
            association = opportunity_contact.insert().values(opportunities=db_opportunity.id, contacts=db_contact.id)
            database.execute(association)
            database.commit()


    contact_ids = database.query(opportunity_contact.c.contacts).filter(opportunity_contact.c.opportunities == db_opportunity.id).all()
    tasks_ids = database.query(Task.id).filter(Task.opportunity_id == db_opportunity.id).all()
    response_data = {
        "opportunity": db_opportunity,
        "contact_ids": [x[0] for x in contact_ids],
        "tasks_ids": [x[0] for x in tasks_ids]    }
    return response_data


@app.post("/opportunity/bulk/", response_model=None, tags=["Opportunity"])
async def bulk_create_opportunity(items: list[OpportunityCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Opportunity entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.owner:
                raise ValueError("User ID is required")

            db_opportunity = Opportunity(
                updated_at=item_data.updated_at,                id=item_data.id,                created_at=item_data.created_at,                value=item_data.value,                stage=item_data.stage.value,                expected_close_date=item_data.expected_close_date,                closed_at=item_data.closed_at,                description=item_data.description,                probability=item_data.probability,                title=item_data.title,                owner_id=item_data.owner,                company_id=item_data.company            )
            database.add(db_opportunity)
            database.flush()  # Get ID without committing
            created_items.append(db_opportunity.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Opportunity entities"
    }


@app.delete("/opportunity/bulk/", response_model=None, tags=["Opportunity"])
async def bulk_delete_opportunity(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Opportunity entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_opportunity = database.query(Opportunity).filter(Opportunity.id == item_id).first()
        if db_opportunity:
            database.delete(db_opportunity)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Opportunity entities"
    }

@app.put("/opportunity/{opportunity_id}/", response_model=None, tags=["Opportunity"])
async def update_opportunity(opportunity_id: int, opportunity_data: OpportunityCreate, database: Session = Depends(get_db)) -> Opportunity:
    db_opportunity = database.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    setattr(db_opportunity, 'updated_at', opportunity_data.updated_at)
    setattr(db_opportunity, 'id', opportunity_data.id)
    setattr(db_opportunity, 'created_at', opportunity_data.created_at)
    setattr(db_opportunity, 'value', opportunity_data.value)
    setattr(db_opportunity, 'stage', opportunity_data.stage.value)
    setattr(db_opportunity, 'expected_close_date', opportunity_data.expected_close_date)
    setattr(db_opportunity, 'closed_at', opportunity_data.closed_at)
    setattr(db_opportunity, 'description', opportunity_data.description)
    setattr(db_opportunity, 'probability', opportunity_data.probability)
    setattr(db_opportunity, 'title', opportunity_data.title)
    if opportunity_data.owner is not None:
        db_owner = database.query(User).filter(User.id == opportunity_data.owner).first()
        if not db_owner:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_opportunity, 'owner_id', opportunity_data.owner)
    if opportunity_data.company is not None:
        db_company = database.query(Company).filter(Company.id == opportunity_data.company).first()
        if not db_company:
            raise HTTPException(status_code=400, detail="Company not found")
        setattr(db_opportunity, 'company_id', opportunity_data.company)
    else:
        setattr(db_opportunity, 'company_id', None)
    if opportunity_data.tasks is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Task).filter(Task.opportunity_id == db_opportunity.id).update(
            {Task.opportunity_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if opportunity_data.tasks:
            # Validate that all IDs exist
            for task_id in opportunity_data.tasks:
                db_task = database.query(Task).filter(Task.id == task_id).first()
                if not db_task:
                    raise HTTPException(status_code=400, detail=f"Task with id {task_id} not found")

            # Update the related entities with the new foreign key
            database.query(Task).filter(Task.id.in_(opportunity_data.tasks)).update(
                {Task.opportunity_id: db_opportunity.id}, synchronize_session=False
            )
    existing_contact_ids = [assoc.contacts for assoc in database.execute(
        opportunity_contact.select().where(opportunity_contact.c.opportunities == db_opportunity.id))]

    contacts_to_remove = set(existing_contact_ids) - set(opportunity_data.contacts)
    for contact_id in contacts_to_remove:
        association = opportunity_contact.delete().where(
            (opportunity_contact.c.opportunities == db_opportunity.id) & (opportunity_contact.c.contacts == contact_id))
        database.execute(association)

    new_contact_ids = set(opportunity_data.contacts) - set(existing_contact_ids)
    for contact_id in new_contact_ids:
        db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
        if db_contact is None:
            raise HTTPException(status_code=404, detail=f"Contact with ID {contact_id} not found")
        association = opportunity_contact.insert().values(contacts=db_contact.id, opportunities=db_opportunity.id)
        database.execute(association)
    database.commit()
    database.refresh(db_opportunity)

    contact_ids = database.query(opportunity_contact.c.contacts).filter(opportunity_contact.c.opportunities == db_opportunity.id).all()
    tasks_ids = database.query(Task.id).filter(Task.opportunity_id == db_opportunity.id).all()
    response_data = {
        "opportunity": db_opportunity,
        "contact_ids": [x[0] for x in contact_ids],
        "tasks_ids": [x[0] for x in tasks_ids]    }
    return response_data


@app.delete("/opportunity/{opportunity_id}/", response_model=None, tags=["Opportunity"])
async def delete_opportunity(opportunity_id: int, database: Session = Depends(get_db)):
    db_opportunity = database.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    database.delete(db_opportunity)
    database.commit()
    return db_opportunity

@app.post("/opportunity/{opportunity_id}/contacts/{contact_id}/", response_model=None, tags=["Opportunity Relationships"])
async def add_contacts_to_opportunity(opportunity_id: int, contact_id: int, database: Session = Depends(get_db)):
    """Add a Contact to this Opportunity's contacts relationship"""
    db_opportunity = database.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    # Check if relationship already exists
    existing = database.query(opportunity_contact).filter(
        (opportunity_contact.c.opportunities == opportunity_id) &
        (opportunity_contact.c.contacts == contact_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = opportunity_contact.insert().values(opportunities=opportunity_id, contacts=contact_id)
    database.execute(association)
    database.commit()

    return {"message": "Contact added to contacts successfully"}


@app.delete("/opportunity/{opportunity_id}/contacts/{contact_id}/", response_model=None, tags=["Opportunity Relationships"])
async def remove_contacts_from_opportunity(opportunity_id: int, contact_id: int, database: Session = Depends(get_db)):
    """Remove a Contact from this Opportunity's contacts relationship"""
    db_opportunity = database.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    # Check if relationship exists
    existing = database.query(opportunity_contact).filter(
        (opportunity_contact.c.opportunities == opportunity_id) &
        (opportunity_contact.c.contacts == contact_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = opportunity_contact.delete().where(
        (opportunity_contact.c.opportunities == opportunity_id) &
        (opportunity_contact.c.contacts == contact_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Contact removed from contacts successfully"}


@app.get("/opportunity/{opportunity_id}/contacts/", response_model=None, tags=["Opportunity Relationships"])
async def get_contacts_of_opportunity(opportunity_id: int, database: Session = Depends(get_db)):
    """Get all Contact entities related to this Opportunity through contacts"""
    db_opportunity = database.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    contact_ids = database.query(opportunity_contact.c.contacts).filter(opportunity_contact.c.opportunities == opportunity_id).all()
    contact_list = database.query(Contact).filter(Contact.id.in_([id[0] for id in contact_ids])).all()

    return {
        "opportunity_id": opportunity_id,
        "contacts_count": len(contact_list),
        "contacts": contact_list
    }





############################################
#
#   Interaction functions
#
############################################

@app.get("/interaction/", response_model=None, tags=["Interaction"])
def get_all_interaction(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Interaction)
        query = query.options(joinedload(Interaction.performed_by))
        query = query.options(joinedload(Interaction.contact))
        interaction_list = query.all()

        # Serialize with relationships included
        result = []
        for interaction_item in interaction_list:
            item_dict = interaction_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if interaction_item.performed_by:
                related_obj = interaction_item.performed_by
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['performed_by'] = related_dict
            else:
                item_dict['performed_by'] = None
            if interaction_item.contact:
                related_obj = interaction_item.contact
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['contact'] = related_dict
            else:
                item_dict['contact'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Interaction).all()


@app.get("/interaction/count/", response_model=None, tags=["Interaction"])
def get_count_interaction(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Interaction entities"""
    count = database.query(Interaction).count()
    return {"count": count}


@app.get("/interaction/paginated/", response_model=None, tags=["Interaction"])
def get_paginated_interaction(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Interaction entities"""
    total = database.query(Interaction).count()
    interaction_list = database.query(Interaction).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": interaction_list
    }


@app.get("/interaction/search/", response_model=None, tags=["Interaction"])
def search_interaction(
    database: Session = Depends(get_db)
) -> list:
    """Search Interaction entities by attributes"""
    query = database.query(Interaction)


    results = query.all()
    return results


@app.get("/interaction/{interaction_id}/", response_model=None, tags=["Interaction"])
async def get_interaction(interaction_id: int, database: Session = Depends(get_db)) -> Interaction:
    db_interaction = database.query(Interaction).filter(Interaction.id == interaction_id).first()
    if db_interaction is None:
        raise HTTPException(status_code=404, detail="Interaction not found")

    response_data = {
        "interaction": db_interaction,
}
    return response_data



@app.post("/interaction/", response_model=None, tags=["Interaction"])
async def create_interaction(interaction_data: InteractionCreate, database: Session = Depends(get_db)) -> Interaction:

    if interaction_data.performed_by is not None:
        db_performed_by = database.query(User).filter(User.id == interaction_data.performed_by).first()
        if not db_performed_by:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")
    if interaction_data.contact is not None:
        db_contact = database.query(Contact).filter(Contact.id == interaction_data.contact).first()
        if not db_contact:
            raise HTTPException(status_code=400, detail="Contact not found")
    else:
        raise HTTPException(status_code=400, detail="Contact ID is required")

    db_interaction = Interaction(
        occurred_at=interaction_data.occurred_at,        subject=interaction_data.subject,        id=interaction_data.id,        type=interaction_data.type.value,        content=interaction_data.content,        created_at=interaction_data.created_at,        direction=interaction_data.direction.value,        performed_by_id=interaction_data.performed_by,        contact_id=interaction_data.contact        )

    database.add(db_interaction)
    database.commit()
    database.refresh(db_interaction)




    return db_interaction


@app.post("/interaction/bulk/", response_model=None, tags=["Interaction"])
async def bulk_create_interaction(items: list[InteractionCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Interaction entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.performed_by:
                raise ValueError("User ID is required")
            if not item_data.contact:
                raise ValueError("Contact ID is required")

            db_interaction = Interaction(
                occurred_at=item_data.occurred_at,                subject=item_data.subject,                id=item_data.id,                type=item_data.type.value,                content=item_data.content,                created_at=item_data.created_at,                direction=item_data.direction.value,                performed_by_id=item_data.performed_by,                contact_id=item_data.contact            )
            database.add(db_interaction)
            database.flush()  # Get ID without committing
            created_items.append(db_interaction.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Interaction entities"
    }


@app.delete("/interaction/bulk/", response_model=None, tags=["Interaction"])
async def bulk_delete_interaction(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Interaction entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_interaction = database.query(Interaction).filter(Interaction.id == item_id).first()
        if db_interaction:
            database.delete(db_interaction)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Interaction entities"
    }

@app.put("/interaction/{interaction_id}/", response_model=None, tags=["Interaction"])
async def update_interaction(interaction_id: int, interaction_data: InteractionCreate, database: Session = Depends(get_db)) -> Interaction:
    db_interaction = database.query(Interaction).filter(Interaction.id == interaction_id).first()
    if db_interaction is None:
        raise HTTPException(status_code=404, detail="Interaction not found")

    setattr(db_interaction, 'occurred_at', interaction_data.occurred_at)
    setattr(db_interaction, 'subject', interaction_data.subject)
    setattr(db_interaction, 'id', interaction_data.id)
    setattr(db_interaction, 'type', interaction_data.type.value)
    setattr(db_interaction, 'content', interaction_data.content)
    setattr(db_interaction, 'created_at', interaction_data.created_at)
    setattr(db_interaction, 'direction', interaction_data.direction.value)
    if interaction_data.performed_by is not None:
        db_performed_by = database.query(User).filter(User.id == interaction_data.performed_by).first()
        if not db_performed_by:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_interaction, 'performed_by_id', interaction_data.performed_by)
    if interaction_data.contact is not None:
        db_contact = database.query(Contact).filter(Contact.id == interaction_data.contact).first()
        if not db_contact:
            raise HTTPException(status_code=400, detail="Contact not found")
        setattr(db_interaction, 'contact_id', interaction_data.contact)
    database.commit()
    database.refresh(db_interaction)

    return db_interaction


@app.delete("/interaction/{interaction_id}/", response_model=None, tags=["Interaction"])
async def delete_interaction(interaction_id: int, database: Session = Depends(get_db)):
    db_interaction = database.query(Interaction).filter(Interaction.id == interaction_id).first()
    if db_interaction is None:
        raise HTTPException(status_code=404, detail="Interaction not found")
    database.delete(db_interaction)
    database.commit()
    return db_interaction





############################################
#
#   Tag functions
#
############################################

@app.get("/tag/", response_model=None, tags=["Tag"])
def get_all_tag(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Tag)
        tag_list = query.all()

        # Serialize with relationships included
        result = []
        for tag_item in tag_list:
            item_dict = tag_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            contact_list = database.query(Contact).join(contact_tag, Contact.id == contact_tag.c.tagged_contacts).filter(contact_tag.c.tags == tag_item.id).all()
            item_dict['tagged_contacts'] = []
            for contact_obj in contact_list:
                contact_dict = contact_obj.__dict__.copy()
                contact_dict.pop('_sa_instance_state', None)
                item_dict['tagged_contacts'].append(contact_dict)
            company_list = database.query(Company).join(company_tag, Company.id == company_tag.c.tagged_companies).filter(company_tag.c.tags == tag_item.id).all()
            item_dict['tagged_companies'] = []
            for company_obj in company_list:
                company_dict = company_obj.__dict__.copy()
                company_dict.pop('_sa_instance_state', None)
                item_dict['tagged_companies'].append(company_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Tag).all()


@app.get("/tag/count/", response_model=None, tags=["Tag"])
def get_count_tag(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Tag entities"""
    count = database.query(Tag).count()
    return {"count": count}


@app.get("/tag/paginated/", response_model=None, tags=["Tag"])
def get_paginated_tag(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Tag entities"""
    total = database.query(Tag).count()
    tag_list = database.query(Tag).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": tag_list
        }

    result = []
    for tag_item in tag_list:
        contact_ids = database.query(contact_tag.c.tagged_contacts).filter(contact_tag.c.tags == tag_item.id).all()
        company_ids = database.query(company_tag.c.tagged_companies).filter(company_tag.c.tags == tag_item.id).all()
        item_data = {
            "tag": tag_item,
            "contact_ids": [x[0] for x in contact_ids],
            "company_ids": [x[0] for x in company_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/tag/search/", response_model=None, tags=["Tag"])
def search_tag(
    database: Session = Depends(get_db)
) -> list:
    """Search Tag entities by attributes"""
    query = database.query(Tag)


    results = query.all()
    return results


@app.get("/tag/{tag_id}/", response_model=None, tags=["Tag"])
async def get_tag(tag_id: int, database: Session = Depends(get_db)) -> Tag:
    db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    contact_ids = database.query(contact_tag.c.tagged_contacts).filter(contact_tag.c.tags == db_tag.id).all()
    company_ids = database.query(company_tag.c.tagged_companies).filter(company_tag.c.tags == db_tag.id).all()
    response_data = {
        "tag": db_tag,
        "contact_ids": [x[0] for x in contact_ids],
        "company_ids": [x[0] for x in company_ids],
}
    return response_data



@app.post("/tag/", response_model=None, tags=["Tag"])
async def create_tag(tag_data: TagCreate, database: Session = Depends(get_db)) -> Tag:

    if tag_data.tagged_contacts:
        for id in tag_data.tagged_contacts:
            # Entity already validated before creation
            db_contact = database.query(Contact).filter(Contact.id == id).first()
            if not db_contact:
                raise HTTPException(status_code=404, detail=f"Contact with ID {id} not found")
    if tag_data.tagged_companies:
        for id in tag_data.tagged_companies:
            # Entity already validated before creation
            db_company = database.query(Company).filter(Company.id == id).first()
            if not db_company:
                raise HTTPException(status_code=404, detail=f"Company with ID {id} not found")

    db_tag = Tag(
        id=tag_data.id,        name=tag_data.name,        color=tag_data.color        )

    database.add(db_tag)
    database.commit()
    database.refresh(db_tag)


    if tag_data.tagged_contacts:
        for id in tag_data.tagged_contacts:
            # Entity already validated before creation
            db_contact = database.query(Contact).filter(Contact.id == id).first()
            # Create the association
            association = contact_tag.insert().values(tags=db_tag.id, tagged_contacts=db_contact.id)
            database.execute(association)
            database.commit()
    if tag_data.tagged_companies:
        for id in tag_data.tagged_companies:
            # Entity already validated before creation
            db_company = database.query(Company).filter(Company.id == id).first()
            # Create the association
            association = company_tag.insert().values(tags=db_tag.id, tagged_companies=db_company.id)
            database.execute(association)
            database.commit()


    contact_ids = database.query(contact_tag.c.tagged_contacts).filter(contact_tag.c.tags == db_tag.id).all()
    company_ids = database.query(company_tag.c.tagged_companies).filter(company_tag.c.tags == db_tag.id).all()
    response_data = {
        "tag": db_tag,
        "contact_ids": [x[0] for x in contact_ids],
        "company_ids": [x[0] for x in company_ids],
    }
    return response_data


@app.post("/tag/bulk/", response_model=None, tags=["Tag"])
async def bulk_create_tag(items: list[TagCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Tag entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_tag = Tag(
                id=item_data.id,                name=item_data.name,                color=item_data.color            )
            database.add(db_tag)
            database.flush()  # Get ID without committing
            created_items.append(db_tag.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Tag entities"
    }


@app.delete("/tag/bulk/", response_model=None, tags=["Tag"])
async def bulk_delete_tag(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Tag entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_tag = database.query(Tag).filter(Tag.id == item_id).first()
        if db_tag:
            database.delete(db_tag)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Tag entities"
    }

@app.put("/tag/{tag_id}/", response_model=None, tags=["Tag"])
async def update_tag(tag_id: int, tag_data: TagCreate, database: Session = Depends(get_db)) -> Tag:
    db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    setattr(db_tag, 'id', tag_data.id)
    setattr(db_tag, 'name', tag_data.name)
    setattr(db_tag, 'color', tag_data.color)
    existing_contact_ids = [assoc.tagged_contacts for assoc in database.execute(
        contact_tag.select().where(contact_tag.c.tags == db_tag.id))]

    contacts_to_remove = set(existing_contact_ids) - set(tag_data.tagged_contacts)
    for contact_id in contacts_to_remove:
        association = contact_tag.delete().where(
            (contact_tag.c.tags == db_tag.id) & (contact_tag.c.tagged_contacts == contact_id))
        database.execute(association)

    new_contact_ids = set(tag_data.tagged_contacts) - set(existing_contact_ids)
    for contact_id in new_contact_ids:
        db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
        if db_contact is None:
            raise HTTPException(status_code=404, detail=f"Contact with ID {contact_id} not found")
        association = contact_tag.insert().values(tagged_contacts=db_contact.id, tags=db_tag.id)
        database.execute(association)
    existing_company_ids = [assoc.tagged_companies for assoc in database.execute(
        company_tag.select().where(company_tag.c.tags == db_tag.id))]

    companys_to_remove = set(existing_company_ids) - set(tag_data.tagged_companies)
    for company_id in companys_to_remove:
        association = company_tag.delete().where(
            (company_tag.c.tags == db_tag.id) & (company_tag.c.tagged_companies == company_id))
        database.execute(association)

    new_company_ids = set(tag_data.tagged_companies) - set(existing_company_ids)
    for company_id in new_company_ids:
        db_company = database.query(Company).filter(Company.id == company_id).first()
        if db_company is None:
            raise HTTPException(status_code=404, detail=f"Company with ID {company_id} not found")
        association = company_tag.insert().values(tagged_companies=db_company.id, tags=db_tag.id)
        database.execute(association)
    database.commit()
    database.refresh(db_tag)

    contact_ids = database.query(contact_tag.c.tagged_contacts).filter(contact_tag.c.tags == db_tag.id).all()
    company_ids = database.query(company_tag.c.tagged_companies).filter(company_tag.c.tags == db_tag.id).all()
    response_data = {
        "tag": db_tag,
        "contact_ids": [x[0] for x in contact_ids],
        "company_ids": [x[0] for x in company_ids],
    }
    return response_data


@app.delete("/tag/{tag_id}/", response_model=None, tags=["Tag"])
async def delete_tag(tag_id: int, database: Session = Depends(get_db)):
    db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    database.delete(db_tag)
    database.commit()
    return db_tag

@app.post("/tag/{tag_id}/tagged_contacts/{contact_id}/", response_model=None, tags=["Tag Relationships"])
async def add_tagged_contacts_to_tag(tag_id: int, contact_id: int, database: Session = Depends(get_db)):
    """Add a Contact to this Tag's tagged_contacts relationship"""
    db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    db_contact = database.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    # Check if relationship already exists
    existing = database.query(contact_tag).filter(
        (contact_tag.c.tags == tag_id) &
        (contact_tag.c.tagged_contacts == contact_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = contact_tag.insert().values(tags=tag_id, tagged_contacts=contact_id)
    database.execute(association)
    database.commit()

    return {"message": "Contact added to tagged_contacts successfully"}


@app.delete("/tag/{tag_id}/tagged_contacts/{contact_id}/", response_model=None, tags=["Tag Relationships"])
async def remove_tagged_contacts_from_tag(tag_id: int, contact_id: int, database: Session = Depends(get_db)):
    """Remove a Contact from this Tag's tagged_contacts relationship"""
    db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Check if relationship exists
    existing = database.query(contact_tag).filter(
        (contact_tag.c.tags == tag_id) &
        (contact_tag.c.tagged_contacts == contact_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = contact_tag.delete().where(
        (contact_tag.c.tags == tag_id) &
        (contact_tag.c.tagged_contacts == contact_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Contact removed from tagged_contacts successfully"}


@app.get("/tag/{tag_id}/tagged_contacts/", response_model=None, tags=["Tag Relationships"])
async def get_tagged_contacts_of_tag(tag_id: int, database: Session = Depends(get_db)):
    """Get all Contact entities related to this Tag through tagged_contacts"""
    db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    contact_ids = database.query(contact_tag.c.tagged_contacts).filter(contact_tag.c.tags == tag_id).all()
    contact_list = database.query(Contact).filter(Contact.id.in_([id[0] for id in contact_ids])).all()

    return {
        "tag_id": tag_id,
        "tagged_contacts_count": len(contact_list),
        "tagged_contacts": contact_list
    }

@app.post("/tag/{tag_id}/tagged_companies/{company_id}/", response_model=None, tags=["Tag Relationships"])
async def add_tagged_companies_to_tag(tag_id: int, company_id: int, database: Session = Depends(get_db)):
    """Add a Company to this Tag's tagged_companies relationship"""
    db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    db_company = database.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    # Check if relationship already exists
    existing = database.query(company_tag).filter(
        (company_tag.c.tags == tag_id) &
        (company_tag.c.tagged_companies == company_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = company_tag.insert().values(tags=tag_id, tagged_companies=company_id)
    database.execute(association)
    database.commit()

    return {"message": "Company added to tagged_companies successfully"}


@app.delete("/tag/{tag_id}/tagged_companies/{company_id}/", response_model=None, tags=["Tag Relationships"])
async def remove_tagged_companies_from_tag(tag_id: int, company_id: int, database: Session = Depends(get_db)):
    """Remove a Company from this Tag's tagged_companies relationship"""
    db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Check if relationship exists
    existing = database.query(company_tag).filter(
        (company_tag.c.tags == tag_id) &
        (company_tag.c.tagged_companies == company_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = company_tag.delete().where(
        (company_tag.c.tags == tag_id) &
        (company_tag.c.tagged_companies == company_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Company removed from tagged_companies successfully"}


@app.get("/tag/{tag_id}/tagged_companies/", response_model=None, tags=["Tag Relationships"])
async def get_tagged_companies_of_tag(tag_id: int, database: Session = Depends(get_db)):
    """Get all Company entities related to this Tag through tagged_companies"""
    db_tag = database.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    company_ids = database.query(company_tag.c.tagged_companies).filter(company_tag.c.tags == tag_id).all()
    company_list = database.query(Company).filter(Company.id.in_([id[0] for id in company_ids])).all()

    return {
        "tag_id": tag_id,
        "tagged_companies_count": len(company_list),
        "tagged_companies": company_list
    }







############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



