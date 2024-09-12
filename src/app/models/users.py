from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UserOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    login: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)  # right??
    project_id: Mapped[int] = mapped_column(nullable=False)
    env: Mapped[str] = mapped_column(String(100), nullable=False)  # right??
    domain: Mapped[str] = mapped_column(String(100), nullable=False)  # right??
    locktime: Mapped[Optional[datetime]] = mapped_column(nullable=True)  # right??