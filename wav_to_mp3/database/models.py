from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import BYTEA, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wav_to_mp3.database.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    access_token: Mapped[UUID] = mapped_column(UUID, unique=True)
    audios: Mapped[List["Audio"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(name={self.name!r}, id={self.id!r})"


class Audio(Base):
    __tablename__ = "audios"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    file: Mapped[BYTEA] = mapped_column(BYTEA)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="audios")

    def __repr__(self):
        return f"Audio(id={self.id!r}, user_id={self.user_id!r})"
