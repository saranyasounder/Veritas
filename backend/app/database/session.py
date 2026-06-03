from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# create database engine using connection string from environment
# engine manages the connection pool to PostgreSQL
engine = create_engine(settings.database_url)

# sessionmaker creates a factory for database sessions
# each session represents one unit of work with the database
# autocommit=False means we control when to commit transactions
# autoflush=False means changes aren't written until we explicitly flush
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    FastAPI dependency that manages database session lifecycle.
    
    Creates a new session for each request and closes it when done.
    Used with Depends() in route functions:
        def my_route(db: Session = Depends(get_db))
    
    Yields:
        Session: active database session
        
    Note:
        Session is always closed in the finally block
        even if the request raises an exception
    """
    db = SessionLocal()
    try:
        # yield gives the session to the route
        # execution pauses here until the route finishes
        yield db
    finally:
        # always close the session after the request ends
        # prevents connection leaks in the database pool
        db.close()