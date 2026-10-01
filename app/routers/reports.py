from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.services.report_service import get_leave_summary


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/leave-summary")
def leave_summary(
    db: Session = Depends(get_db)
):
    return get_leave_summary(db)