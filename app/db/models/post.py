from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.types import TEXT, TIMESTAMP
from sqlalchemy.sql import func

from app.db import Base, User


class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    text: Mapped[str] = mapped_column(TEXT())
    public_date: Mapped[datetime] = mapped_column(TIMESTAMP(), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    user: Mapped[User] = relationship()