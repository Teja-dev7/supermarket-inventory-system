import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file")

# Create the SQLAlchemy engine
# pool_pre_ping checks connections before handing them out from the pool (ideal for cloud DBs like Supabase)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db():
    """FastAPI dependency to yield database sessions per request and ensure cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
