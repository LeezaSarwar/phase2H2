import asyncio
from logging.config import fileConfig
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel

from alembic import context

# Import models to register them with SQLModel
from app.models import Task, User
from app.config import get_settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def convert_database_url(url: str) -> str:
    """Convert database URL for asyncpg compatibility."""
    url = url.replace("postgresql://", "postgresql+asyncpg://")
    url = url.replace("postgres://", "postgresql+asyncpg://")

    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    # Remove incompatible parameters
    query_params.pop('sslmode', None)
    query_params.pop('channel_binding', None)

    new_query = urlencode(query_params, doseq=True)
    new_parsed = parsed._replace(query=new_query)
    return urlunparse(new_parsed)


settings = get_settings()
database_url = convert_database_url(settings.database_url)

config.set_main_option("sqlalchemy.url", database_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args={"ssl": "require"},
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
