from sqlalchemy.orm import Session
from app.models.hall import Hall
from app.schemas.hall import HallCreate

def create_hall(db: Session, hall_data: HallCreate) -> Hall: 
	hall = Hall(**hall_data.model_dump())
	db.add(hall)
	db.commit()
	db.refresh(hall)
	return hall


def get_all_halls(db: Session):
	return db.query(Hall).filter(Hall.is_active == True).all()


def update_hall(db: Session, hall_id: int, hall_data: HallCreate) -> Hall:
	hall = db.query(Hall).filter(Hall.id == hall_id).first() 
	if not hall:
		return None
	for key, value in hall_data.model_dump().items():
		setattr(hall, key, value)
	db.commit()
	db.refresh(hall)
	return hall


def delete_hall(db: Session, hall_id: int) -> Hall:
	hall = db.query(Hall).filter(Hall.id == hall_id).first()
	if not hall:
		return None
	hall.is_active = False
	db.commit()
	return hall