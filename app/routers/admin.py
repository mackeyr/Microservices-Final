from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from ..auth import require_admin

router = APIRouter(prefix="/admin")

@router.get("/stats", dependencies=[Depends(require_admin)])
def get_admin_stats(db: Session = Depends(get_db)):
    total_facts = db.query(crud.models.Fact).count()
    top_facts = db.query(crud.models.Fact).order_by(crud.models.Fact.views.desc()).limit(5).all()
    recent_facts = db.query(crud.models.Fact).order_by(crud.models.Fact.created_at.desc()).limit(5).all()
    total_usage = db.query(crud.models.UsageStat).count()
    
    return {
        "total_facts": total_facts,
        "top_facts": [{"text": f.text, "views": f.views} for f in top_facts],
        "recent_facts": [{"text": f.text, "created_at": f.created_at} for f in recent_facts],
        "total_usage_requests": total_usage
    }
