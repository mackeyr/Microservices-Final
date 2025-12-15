from sqlalchemy.orm import Session
from . import models, schemas
from .kafka_producer import send_fact_created_event

def create_fact(db: Session, fact: schemas.FactCreate):
    obj = models.Fact(text=fact.text, source=fact.source)
    db.add(obj)
    db.commit()
    db.refresh(obj)

    send_fact_created_event(obj)

    return obj


def get_random_fact(db: Session):
    return db.query(models.Fact).order_by(models.func.random()).first()

def get_popular_facts(db: Session, limit: int = 10):
    return (
        db.query(models.Fact)
        .order_by(models.Fact.views.desc())
        .limit(limit)
        .all()
    )

def record_usage(db: Session, endpoint: str, method: str, status_code: int, api_key: str | None):
    entry = models.UsageStat(
        endpoint=endpoint,
        method=method,
        status_code=status_code,
        api_key=api_key
    )
    db.add(entry)
    db.commit()

def get_stats(db: Session):
    return db.query(models.UsageStat).all()

def get_api_key(db: Session, key: str):
    return db.query(models.APIKey).filter(models.APIKey.key == key).first()
