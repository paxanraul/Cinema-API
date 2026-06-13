from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate

def create_session(db: Session, session_data: SessionCreate) -> SessionModel:
	session = SessionModel(**session_data.model_dump())
	db.add(session)
	db.commit()
	db.refresh(session)
	return session


def get_session(db: Session):
	return db.query(SessionModel).all()