from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.booking import Booking
from app.schemas.booking import BookingCreate
from app.models.session import Session as SessionModel

def create_booking(db: Session, booking_data: BookingCreate, user_id: int) -> Booking:
	session = db.query(SessionModel).filter(SessionModel.id == booking_data.session_id).first()
	
	if not session:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сеанс не найден")

	if session.start_time < datetime.now():
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Сеанс уже прошёл")

	booking = Booking(**booking_data.model_dump(), user_id=user_id)
	db.add(booking)
	db.commit()
	db.refresh(booking)
	return booking


def get_my_bookings(db: Session, user_id: int):
	return db.query(Booking).filter(Booking.user_id == user_id, Booking.is_active == True).all()


def delete_booking(db: Session, booking_id: int, user_id: int) -> Booking:
	booking = db.query(Booking).filter(Booking.id==booking_id).first()
	if not booking:
		return None
	if booking.user_id != user_id:
		return None
	booking.is_active = False
	db.commit()
	return booking