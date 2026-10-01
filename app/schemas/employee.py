from pydantic import BaseModel, ConfigDict, EmailStr


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    department_id: int


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department_id: int

    model_config = ConfigDict(from_attributes=True)