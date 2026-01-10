from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone
from app.core import settings

engine = create_engine(url=settings.postgres.get_database_url_sync, echo=True)
session_maker = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False, autocommit=False)

def get_current_time() -> datetime:
    dt = datetime.now(tz=timezone.utc)
    return dt

class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData()

    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=get_current_time)