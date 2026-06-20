from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.models.movie import Movie
from app.models.hall import Hall
from app.models.session import Session as SessionModel


def run_seed(db: Session) -> None:
    if db.query(User).first():
        return

    user = User(
        first_name="Demo",
        last_name="User",
        patronymic=None,
        email="demo@demo.com",
        hash_password=hash_password("password123"),
        role="user",
    )
    db.add(user)

    movie = Movie(
        name="Inception",
        year=2010,
        description="Sci-fi about dreams within dreams",
        duration_limites=148,
        rating=8.8,
        genre="Sci-Fi",
        director="Christopher Nolan",
    )
    db.add(movie)

    hall = Hall(name="Зал 1", capacity=100, location="Этаж 1")
    db.add(hall)

    db.flush()

    session = SessionModel(
        movie_id=movie.id,
        hall_id=hall.id,
        start_time=datetime.now(timezone.utc) + timedelta(days=1),
    )
    db.add(session)

    db.commit()
