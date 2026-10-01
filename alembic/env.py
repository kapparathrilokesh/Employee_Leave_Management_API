from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from dotenv import load_dotenv

from alembic import context

from app.database import Base

# Import all models so Alembic can detect them
from app.models.department import Department
from app.models.employee import Employee
from app.models.leave_request import LeaveRequest


# Load environment variables from .env
load_dotenv()

config = context.config

# Get DATABASE_URL from .env
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is not set in .env")

# Set database URL for Alembic
config.set_main_option(
    "sqlalchemy.url",
    database_url.replace("%", "%%")
)


# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# SQLAlchemy metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()