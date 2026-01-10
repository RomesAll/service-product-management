from ..db.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Column
from sqlalchemy.dialects.postgresql import UUID

class UsersOrm(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, autoincrement=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    active: Mapped[bool] = mapped_column(default=False)
    password: Mapped[bytes]