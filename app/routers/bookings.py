from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.schemas.booking import BookingCreate, BookingResponse
from app.models.booking import Booking
from app.services.booking_service import create_booking, delete_booking, get_my_bookings
from app.models.user import User


router = APIRouter(
	prefix="/bookings",
	tags=["bookings"]
)

@router.get("/all_my_bookings", response_model=list[BookingResponse])
def get_bookings(
	db: Session = Depends(get_db),
	current_user: User = Depends(get_current_user)
):
	bookings = get_my_bookings(db, current_user.id)
	return bookings


@router.post("/create_booking", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def add_booking(
	booking_data: BookingCreate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	bookings = create_booking(db, booking_data, current_user.id)
	return bookings


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_booking(
	booking_id: int,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	booking = delete_booking(db, booking_id, current_user.id)
	if not booking:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Билет не найден"
		)