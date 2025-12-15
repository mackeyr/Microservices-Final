from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ffuser:ffpass@db:5432/funfacts")

engine = create_engine(
    DATABASE_URL,
    pool_size=20,       
    max_overflow=30,    
    pool_timeout=30,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
