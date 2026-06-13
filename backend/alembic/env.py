from logging.config import fileConfig
from pathlib import Path
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv


# Alembic config object
config = context.config

# Set up logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Make backend/ importable so `from app...` works
backend_path = Path(__file__).resolve().parents[1]
project_root = backend_path.parent

if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))


# Load .env from project root
load_dotenv(project_root / ".env")


# Import Base and models so Alembic can see SQLAlchemy tables
from app.database import Base
from app import models


# This is what enables Alembic autogenerate
target_metadata = Base.metadata


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")

    if database_url is None:
        raise RuntimeError("DATABASE_URL is not set")

    return database_url


def run_migrations_offline() -> None:
    """Run migrations without a live database connection."""
    url = get_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with a live database connection."""
    database_url = get_database_url()

    config.set_main_option("sqlalchemy.url", database_url)

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