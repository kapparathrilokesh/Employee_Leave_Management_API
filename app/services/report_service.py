from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.leave_request import LeaveRequest


def get_leave_summary(db: Session):
    result = db.query(
        LeaveRequest.status,
        func.count(LeaveRequest.id).label("count")
    ).group_by(
        LeaveRequest.status
    ).all()

    return [
        {
            "status": status,
            "count": count
        }
        for status, count in result
    ]