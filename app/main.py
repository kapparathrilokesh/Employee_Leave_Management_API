from fastapi import FastAPI

from app.database import Base, engine

# Import models so SQLAlchemy knows about them
from app.models.department import Department
from app.models.employee import Employee
from app.models.leave_request import LeaveRequest

# Import routers
from app.routers import departments, employees, leaves, auth, reports


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Employee Leave Management API",
    description="API for managing employees, departments, and leave requests",
    version="1.0.0"
)


# Register routers
app.include_router(departments.router)
app.include_router(employees.router)
app.include_router(leaves.router)
app.include_router(auth.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {
        "message": "Employee Leave Management API is running"
    }