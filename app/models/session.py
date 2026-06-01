from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app.db.base import Base


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    movie: Mapped["Movie"] = relationship(back_populates="sessions") # type: ignore
    hall: Mapped["Hall"] = relationship(back_populates="sessions") # type: ignore

    bookings: Mapped[list["Booking"]] = relationship(back_populates="session") # type: ignore