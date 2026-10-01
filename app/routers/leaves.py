from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.employee import Employee
from app.models.leave_request import LeaveRequest
from app.schemas.leave import LeaveCreate, LeaveResponse, LeaveStatusUpdate
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/leaves",
    tags=["Leaves"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=LeaveResponse)
def create_leave(
    leave: LeaveCreate,
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(
        Employee.id == leave.employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if leave.end_date < leave.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date"
        )

    new_leave = LeaveRequest(
        employee_id=leave.employee_id,
        leave_type=leave.leave_type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status="Pending"
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return new_leave


@router.get("/", response_model=list[LeaveResponse])
def get_leaves(
    db: Session = Depends(get_db)
):
    return db.query(LeaveRequest).all()


@router.get("/{leave_id}", response_model=LeaveResponse)
def get_leave(
    leave_id: int,
    db: Session = Depends(get_db)
):
    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    return leave


@router.put("/{leave_id}", response_model=LeaveResponse)
def update_leave(
    leave_id: int,
    leave_data: LeaveCreate,
    db: Session = Depends(get_db)
):
    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    employee = db.query(Employee).filter(
        Employee.id == leave_data.employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if leave_data.end_date < leave_data.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date"
        )

    leave.employee_id = leave_data.employee_id
    leave.leave_type = leave_data.leave_type
    leave.start_date = leave_data.start_date
    leave.end_date = leave_data.end_date
    leave.reason = leave_data.reason

    db.commit()
    db.refresh(leave)

    return leave

@router.put("/{leave_id}/status", response_model=LeaveResponse)
def update_leave_status(
    leave_id: int,
    status_data: LeaveStatusUpdate,
    db: Session = Depends(get_db)
):
    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    if status_data.status not in ["Approved", "Rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Approved or Rejected"
        )

    leave.status = status_data.status

    db.commit()
    db.refresh(leave)

    return leave


@router.delete("/{leave_id}")
def delete_leave(
    leave_id: int,
    db: Session = Depends(get_db)
):
    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    db.delete(leave)
    db.commit()

    return {
        "message": "Leave request deleted successfully"
    }