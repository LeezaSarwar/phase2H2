from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from app.config import get_settings


settings = get_settings()


def convert_database_url(url: str) -> str:
    """Convert database URL for asyncpg compatibility."""
    # Replace driver
    url = url.replace("postgresql://", "postgresql+asyncpg://")
    url = url.replace("postgres://", "postgresql+asyncpg://")

    # Parse URL and remove incompatible parameters
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    # Remove sslmode - we'll handle SSL via connect_args instead
    query_params.pop('sslmode', None)
    query_params.pop('channel_binding', None)

    # Rebuild query string
    new_query = urlencode(query_params, doseq=True)

    # Rebuild URL
    new_parsed = parsed._replace(query=new_query)
    return urlunparse(new_parsed)


database_url = convert_database_url(settings.database_url)

engine = create_async_engine(
    database_url,
    echo=False,
    pool_pre_ping=True,  # Test connections before using
    pool_size=5,  # Number of connections to maintain
    max_overflow=10,  # Max additional connections
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_timeout=30,  # Timeout for getting connection from pool
    connect_args={
        "ssl": "require",
        "timeout": 10,  # Connection timeout in seconds
        "command_timeout": 10,  # Command timeout in seconds
    },
)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides a database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
