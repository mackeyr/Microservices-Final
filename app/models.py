from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Fact(Base):
    __tablename__ = "facts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    source = Column(String, nullable=True)
    views = Column(Integer, default=0)
    score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    role = Column(String, default="user")  # "user" or "admin"


class UsageStat(Base):
    __tablename__ = "usage_stats"

    id = Column(Integer, primary_key=True)
    endpoint = Column(String)
    method = Column(String)
    status_code = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    api_key = Column(String, nullable=True)
