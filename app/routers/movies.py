from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.movie import Movie
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.schemas.movie import MovieCreate, MovieResponse
from app.services.movie_service import (
    create_movie, get_all_movies, update_movie, delete_movie
    )


router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

@router.get("/all_movies", response_model=list[MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    movies = get_all_movies(db)
    return movies


@router.post("/create_movie", status_code=status.HTTP_201_CREATED, response_model=MovieResponse)
def add_movie(
    movie_data: MovieCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    create = create_movie(db, movie_data)
    return create	


@router.patch("/{movie_id}", response_model=MovieResponse)
def patch_movie(
    movie_id: int,
    movie_data: MovieCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    movie = update_movie(db, movie_id, movie_data)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фильм не найден"
        )
    return movie

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_movie(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    movie = delete_movie(db, movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фильм не найден"
        )