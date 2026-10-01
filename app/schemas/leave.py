from datetime import date

from pydantic import BaseModel, ConfigDict


class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str | None = None


class LeaveResponse(BaseModel):
    id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str | None
    status: str

    model_config = ConfigDict(from_attributes=True)


class LeaveStatusUpdate(BaseModel):
    status: str