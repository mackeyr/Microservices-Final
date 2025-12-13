from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import require_admin
from ..crud import get_stats

router = APIRouter(prefix="/admin")

@router.get("/stats")
def admin_stats(db: Session = Depends(get_db), admin = Depends(require_admin)):
    return get_stats(db)
