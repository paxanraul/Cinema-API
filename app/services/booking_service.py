from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.schemas.booking import BookingCreate

def create_booking(db: Session, booking_data: BookingCreate, user_id: int) -> Booking:
	booking = Booking(**booking_data.model_dump(), user_id=user_id)
	db.add(booking)
	db.commit()
	db.refresh(booking)
	return booking


def get_my_bookings(db: Session, user_id: int):
	return db.query(Booking).filter(Booking.user_id == user_id, Booking.is_active == True).all()


def delete_booking(db: Session, booking_id: int) -> Booking:
	booking = db.query(Booking).filter(Booking.id==booking_id).first()
	if not booking:
		return None
	booking.is_active = False
	db.commit()
	return booking