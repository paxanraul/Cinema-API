from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.hall import HallCreate, HallResponse
from app.services.hall_service import create_hall, get_all_halls, delete_hall, update_hall
from app.dependencies.auth import get_current_user
from app.db.session import get_db


router = APIRouter(
	prefix="/halls",
	tags=["Halls"]
)


@router.get("/all_halls", response_model=list[HallResponse])
def get_halls(
	db: Session = Depends(get_db),
	current_user: User = Depends(get_current_user)
):
	halls = get_all_halls(db)
	return halls


@router.post("/create_hall", status_code=status.HTTP_201_CREATED, response_model=HallResponse)
def add_hall(
	hall_data: HallCreate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	create = create_hall(db, hall_data)
	return create


@router.patch("/{hall_id}", response_model=HallResponse)
def patch_movie(
	hall_id: int,
	hall_data: HallCreate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	hall = update_hall(db, hall_id, hall_data)
	if not hall:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Зал не найден"
		)
	return hall


@router.delete("/{hall_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_hall(
	hall_id: int,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	hall = delete_hall(db, hall_id)
	if not hall:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Зал не найден"
		)