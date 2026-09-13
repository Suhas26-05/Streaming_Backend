import sys
import urllib.parse
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import create_engine, pool

# --- Make `app.*` importable ------------------------------------------------
# The rest of the codebase imports things like `from app.core.database import
# ...` which only works when the `src` folder (not the repo root) is on
# sys.path. Alembic runs with the repo root as the working directory, so we
# add `src` to sys.path ourselves before importing anything from `app`.
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from app.core.config import (  # noqa: E402
    DB_DATABASE,
    DB_DRIVER,
    DB_PASSWORD,
    DB_SERVER,
    DB_USERNAME,
)
from app.models.base import Base  # noqa: E402

# Import every model module so its tables register on Base.metadata before
# autogenerate compares metadata against the database.
from app.models import admin, user  # noqa: E402,F401

# this is the Alembic Config object, which provides access to values within
# the .ini file in use.
config = context.config

# Build the DB URL from the same env vars the app itself uses, instead of
# hardcoding/duplicating it in alembic.ini.
# NOTE: we deliberately do NOT push this into config.set_main_option() /
# alembic.ini. The url-encoded ODBC string contains "%" characters (from
# quote_plus), and alembic.ini is read by configparser, which treats "%" as
# interpolation syntax and raises ValueError. Instead we build the engine
# directly with this URL, bypassing the ini file entirely.
_connection_string = (
    f"DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};"
    f"UID={DB_USERNAME};PWD={DB_PASSWORD};TrustServerCertificate=yes;"
)
_params = urllib.parse.quote_plus(_connection_string)
DB_URL = f"mssql+pyodbc:///?odbc_connect={_params}"

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(DB_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
