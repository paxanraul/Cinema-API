from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.schemas.movie import MovieCreate

def create_movie(db: Session, movie_data: MovieCreate) -> Movie:
	movie = Movie(**movie_data.model_dump())
	db.add(movie)
	db.commit()
	db.refresh(movie)
	return movie


def get_all_movies(db: Session):
	return db.query(Movie).filter(Movie.is_active==True).all()


def update_movie(db: Session, movie_id: int, movie_data: MovieCreate) -> Movie:
	movie = db.query(Movie).filter(Movie.id == movie_id).first()
	if not movie:
		return {"Error": "It's not a movie."}
	for key, value in movie_data.model_dump().items():
		setattr(movie, key, value)
	db.commit()
	db.refresh(movie)
	return movie


def delete_movie(db: Session, movie_id: int) -> Movie:
	movie = db.query(Movie).filter(Movie.id == movie_id).first()
	if not movie:
		return None
	movie.is_active = False
	db.commit()
	return movie
