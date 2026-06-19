from sqlalchemy import String, Integer, CheckConstraint, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    year: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=False)
    duration_limites: Mapped[int] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    genre: Mapped[str] = mapped_column(nullable=False)
    director: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    sessions: Mapped[list["Session"]] = relationship(back_populates="movie")

    __table_args__ = (
        CheckConstraint('year >= 1888 AND year <= 2100', name='check_year_range'),
        CheckConstraint('rating >= 0 AND rating <= 10', name='check_rating_range')
    )